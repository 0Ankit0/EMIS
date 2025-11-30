import asyncio
import os
import io
import pandas as pd
from playwright.async_api import async_playwright
from django.conf import settings

async def process_exam_results(input_file, params, delay=1):
    """
    Process the exam results using Playwright.
    input_file: bytes or file-like object containing the Excel file
    params: dict containing result_type, year, session, semester, program
    delay: float (seconds)
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

            # Add columns for results if they don't exist
            result_columns = ['Student Name', 'Registration Number', 'Semester', 'Level', 
                            'Faculty', 'Program', 'College Name', 'SGPA', 'Status']
            for col in result_columns:
                if col not in df.columns:
                    df[col] = ''

            url = "https://exam.pu.edu.np:9094/"

            for index, row in df.iterrows():
                # Skip rows where Exam Roll No. is empty or NaN
                if pd.isna(row['Exam Roll No.']) or str(row['Exam Roll No.']).strip() == '':
                    continue
                    
                roll_no = str(row['Exam Roll No.']).strip()
                
                # Get date of birth
                if pd.isna(row['Date of Birth']):
                    print(f"Skipping {roll_no}: No date of birth")
                    continue
                    
                dob = row['Date of Birth']

                print(f"Processing {roll_no}, {dob}")

                # Try to navigate with retries
                max_retries = 3
                retry_delay = 2
                for attempt in range(max_retries):
                    try:
                        await page.goto(url, timeout=30000)  # 30 second timeout
                        break  # Success, exit retry loop
                    except Exception as nav_error:
                        if attempt < max_retries - 1:
                            print(f"Connection error (attempt {attempt + 1}/{max_retries}): {nav_error}")
                            print(f"Retrying in {retry_delay} seconds...")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                        else:
                            print(f"Failed to connect after {max_retries} attempts: {nav_error}")
                            df.at[index, 'Status'] = f'Error: Connection failed'
                            continue

                # Fill the form with error handling
                try:
                    if params.get('result_type'):
                        await page.select_option('#Exam_Type', value=params['result_type'])
                    if params.get('year'):
                        await page.select_option('#Year', value=str(params['year']))
                    if params.get('session'):
                        await page.select_option('#Academic_System', value=params['session'])
                    if params.get('semester'):
                        await page.select_option('#Semester', value=params['semester'])
                    if params.get('program'):
                        await page.select_option('#Program', value=params['program'])
                except Exception as e:
                    print(f"Error selecting dropdown options: {e}")
                    # Try to get available options for debugging
                    try:
                        exam_types = await page.locator('#Exam_Type option').all_text_contents()
                        years = await page.locator('#Year option').all_text_contents()
                        sessions = await page.locator('#Academic_System option').all_text_contents()
                        semesters = await page.locator('#Semester option').all_text_contents()
                        programs = await page.locator('#Program option').all_text_contents()
                        
                        error_msg = f"""
Dropdown selection error. Available options:
- Exam Types: {exam_types}
- Years: {years}
- Sessions: {sessions}
- Semesters: {semesters}
- Programs: {programs}

Your values:
- Result Type: {params.get('result_type')}
- Year: {params.get('year')}
- Session: {params.get('session')}
- Semester: {params.get('semester')}
- Program: {params.get('program')}
"""
                        print(error_msg)
                        raise ValueError(error_msg)
                    except:
                        raise e

                await page.fill('#Symbol_Number', roll_no)

                try:
                    # Handle date of birth - could be datetime object or string
                    if isinstance(dob, pd.Timestamp):
                        dob_formatted = dob.strftime('%Y-%m-%d')
                    else:
                        dob_date = pd.to_datetime(dob)
                        dob_formatted = dob_date.strftime('%Y-%m-%d')
                    await page.fill('#DOB', dob_formatted)
                except Exception as e:
                    print(f"Error parsing DOB for {roll_no}: {dob} - {e}")
                    df.at[index, 'Status'] = f'Error: Invalid DOB format'
                    continue

                # Click Submit
                await page.click('input[type="submit"]')
                
                # Wait for result page to load
                await page.wait_for_timeout(delay * 1000)
                
                try:
                    # Extract student details from the result page
                    student_name_elem = await page.locator('span:has-text("Student Name:")').text_content()
                    if student_name_elem:
                        student_name = student_name_elem.replace('Student Name:', '').strip()
                        df.loc[index, 'Student Name'] = student_name
                    
                    reg_number_elem = await page.locator('span:has-text("Registration Number:")').text_content()
                    if reg_number_elem:
                        registration_number = reg_number_elem.replace('Registration Number:', '').strip()
                        df.loc[index, 'Registration Number'] = registration_number
                    
                    semester_elem = await page.locator('span:has-text("Semester:")').text_content()
                    if semester_elem:
                        semester = semester_elem.split('(')[0].replace('Semester:', '').strip()
                        df.loc[index, 'Semester'] = semester
                    
                    level_elem = await page.locator('span:has-text("Level:")').text_content()
                    if level_elem:
                        level = level_elem.replace('Level:', '').strip()
                        df.loc[index, 'Level'] = level
                    
                    faculty_elem = await page.locator('span:has-text("Faculty:")').text_content()
                    if faculty_elem:
                        faculty = faculty_elem.replace('Faculty:', '').strip()
                        df.loc[index, 'Faculty'] = faculty
                    
                    program_elem = await page.locator('span:has-text("Program:")').text_content()
                    if program_elem:
                        program = program_elem.replace('Program:', '').strip()
                        df.loc[index, 'Program'] = program
                    
                    college_elem = await page.locator('span:has-text("College Name:")').text_content()
                    if college_elem:
                        college_name = college_elem.replace('College Name:', '').strip()
                        df.loc[index, 'College Name'] = college_name
                    
                    # Extract SGPA from the table
                    sgpa_elem = await page.locator('td:has-text("SGPA =")').text_content()
                    if sgpa_elem:
                        sgpa = sgpa_elem.replace('SGPA =', '').replace('SGPA=', '').strip()
                        df.loc[index, 'SGPA'] = sgpa
                    
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
                                df.loc[index, title] = grade
                    
                    df.loc[index, 'Status'] = 'Success'
                    
                    student_name_display = df.loc[index, 'Student Name'] if 'Student Name' in df.columns else roll_no
                    sgpa_display = df.loc[index, 'SGPA'] if 'SGPA' in df.columns else 'N/A'
                    print(f"Successfully processed {roll_no}: {student_name_display}, SGPA = {sgpa_display}")
                    
                except Exception as e:
                    print(f"Error extracting result for {roll_no}: {e}")
                    df.at[index, 'Status'] = f'Error: {str(e)}'
                    continue
            
            # Save the updated Excel file to memory
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            return output

        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
        finally:
            await browser.close()
