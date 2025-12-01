import asyncio
import os
import io
import pandas as pd
from playwright.async_api import async_playwright
from django.conf import settings

async def process_exam_results(input_file, params, delay=1, autofill=True):
    """
    Process the exam results using Playwright.
    input_file: bytes or file-like object containing the Excel file
    params: dict containing result_type, year, session, semester, program
    delay: float (seconds) - delay between processing each row
    autofill: bool - if True, extract and fill data automatically; if False, only navigate and wait
    Returns: io.BytesIO object containing the processed Excel file
    """
    async with async_playwright() as p:
        # Launch browser - headed so user can see
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Load Excel file from memory
            # The template has headers in row 3 (0-indexed row 3)
            df = pd.read_excel(io.BytesIO(input_file), header=3)
            
            # Ensure required columns exist
            if 'Exam Roll No.' not in df.columns:
                raise ValueError("Excel file must contain 'Exam Roll No.' column")
            
            # Check if Date of Birth is split into DD/MM/YYYY columns
            # In the template, these are: 'Date of Birth' (DD), 'Unnamed: 4' (MM), 'Unnamed: 5' (YYYY)
            if 'Date of Birth' in df.columns and 'Unnamed: 4' in df.columns and 'Unnamed: 5' in df.columns:
                # Split format - combine them
                # First, rename for clarity
                df = df.rename(columns={
                    'Date of Birth': 'DD',
                    'Unnamed: 4': 'MM',
                    'Unnamed: 5': 'YYYY'
                })
                
                # Combine into a single Date of Birth column
                df['Date of Birth'] = pd.to_datetime(
                    df['YYYY'].astype(str).str.strip() + '-' + 
                    df['MM'].astype(str).str.strip().str.zfill(2) + '-' + 
                    df['DD'].astype(str).str.strip().str.zfill(2),
                    format='%Y-%m-%d',
                    errors='coerce'
                )
            elif 'Date of Birth' not in df.columns:
                raise ValueError("Excel file must contain date columns")

            # Add SGPA column if it doesn't exist (course columns will be added dynamically)
            if 'SGPA' not in df.columns:
                df['SGPA'] = ''

            url = "https://exam.pu.edu.np:9094/"

            # Navigate to the page once
            max_retries = 3
            retry_delay = 2
            for attempt in range(max_retries):
                try:
                    await page.goto(url, timeout=30000)  # 30 second timeout
                    break  # Success, exit retry loop
                except Exception as nav_error:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        raise Exception("Failed to connect to exam portal")

            # Helper function to select from Select2 dropdown
            async def select_select2(selector, value):
                """Select an option from a Select2 dropdown by clicking and typing"""
                try:
                    # Click on the Select2 container to open dropdown
                    select2_container = f"{selector} + .select2-container"
                    await page.click(select2_container)
                    await page.wait_for_timeout(300)  # Wait for dropdown to open
                    
                    # Type the value in the search box
                    search_input = '.select2-search__field'
                    await page.fill(search_input, value)
                    await page.wait_for_timeout(300)  # Wait for filtering
                    
                    # Click the first result
                    result = '.select2-results__option--highlighted, .select2-results__option:first-child'
                    await page.click(result)
                    await page.wait_for_timeout(300)  # Wait for selection
                except Exception as e:
                    # Fallback: try standard select if Select2 fails
                    await page.select_option(selector, value=value)
            
            # Set form values once (they remain the same for all rows)
            try:
                # Result Type - standard select
                if params.get('result_type'):
                    await page.select_option('#Exam_Type', value=params['result_type'])
                
                # Year - Select2
                if params.get('year'):
                    await select_select2('#Year', str(params['year']))
                
                # Academic Session - standard select
                if params.get('session'):
                    await page.select_option('#Academic_System', value=params['session'])

                # Wait for Semester dropdown to appear/become enabled after selecting Year and Academic Session
                if params.get('year') or params.get('session'):
                    try:
                        # Wait up to 2 seconds for the Semester dropdown to be enabled/visible
                        await page.wait_for_timeout(2000)
                    except Exception:
                        pass

                # Semester - standard select
                if params.get('semester'):
                    await page.select_option('#Semester', value=params['semester'])
                
                # Program - Select2
                if params.get('program'):
                    await select_select2('#Program', params['program'])
            except Exception as e:
                raise e

            # Process each row - only fill Exam Roll Number and Date of Birth
            for index, row in df.iterrows():
                # Skip rows where Exam Roll No. is empty or NaN
                exam_roll = row.get('Exam Roll No.')
                
                # More strict validation
                if pd.isna(exam_roll):
                    continue
                
                # Convert to string and validate
                roll_no = str(exam_roll).strip()
                
                # Skip if empty string or contains only whitespace
                if not roll_no or roll_no == '' or roll_no == 'nan':
                    continue
                
                # Skip if it looks like a float representation (e.g., "24032282.0")
                # We want actual roll numbers without decimal points
                if '.' in roll_no:
                    # Remove trailing .0 if present
                    roll_no = roll_no.rstrip('0').rstrip('.')
                
                # Get date of birth
                if pd.isna(row['Date of Birth']):
                    continue
                    
                dob = row['Date of Birth']

                # Clear and fill only Exam Roll Number
                await page.fill('#Symbol_Number', '')
                await page.fill('#Symbol_Number', roll_no)

                # Clear and fill Date of Birth
                try:
                    # Handle date of birth - could be datetime object or string
                    if isinstance(dob, pd.Timestamp):
                        dob_formatted = dob.strftime('%Y-%m-%d')
                    else:
                        dob_date = pd.to_datetime(dob)
                        dob_formatted = dob_date.strftime('%Y-%m-%d')
                    await page.fill('#DOB', '')
                    await page.fill('#DOB', dob_formatted)
                except Exception as e:
                    df.at[index, 'Status'] = f'Error: Invalid DOB format'
                    continue

                # Click Submit
                await page.click('input[type="submit"]')
                
                # Wait for result page to load
                await page.wait_for_timeout(delay * 1000)
                
                # Only extract data if autofill is True
                if autofill:
                    try:
                        # Extract SGPA from the table
                        sgpa_elem = await page.locator('td:has-text("SGPA =")').text_content()
                        if sgpa_elem:
                            sgpa = sgpa_elem.replace('SGPA =', '').replace('SGPA=', '').strip()
                            df.at[index, 'SGPA'] = sgpa
                        
                        # Extract course details from table
                        course_rows = await page.locator('table.table tbody tr').all()
                        
                        # Process each course row (skip the last 2 rows: Total and empty row)
                        for course_row in course_rows[:-2]:
                            cells = await course_row.locator('td').all()
                            if len(cells) >= 5:
                                code = await cells[1].text_content()
                                title = await cells[2].text_content()
                                credit = await cells[3].text_content()
                                grade = await cells[4].text_content()
                                
                                if code and title:
                                    code = code.strip()
                                    title = title.strip()
                                    credit = credit.strip() if credit else ''
                                    grade = grade.strip() if grade else ''
                                    
                                    # Check if this course title exists as a column in the Excel
                                    # If not, create a new column with the course title
                                    if title not in df.columns:
                                        df[title] = ''
                                    
                                    # Store the grade in the appropriate course column
                                    df.at[index, title] = grade
                        
                    except Exception as e:
                        pass

            
            # Save the updated Excel file to memory
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            return output

        except Exception as e:
            raise e
        finally:
            await browser.close()
