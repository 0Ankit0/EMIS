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
            df = pd.read_excel(input_file)
            
            # Ensure required columns exist
            if 'Exam Roll Number' not in df.columns or 'Date of Birth' not in df.columns:
                raise ValueError("Excel file must contain 'Exam Roll Number' and 'Date of Birth' columns")

            # Add columns for results if they don't exist
            if 'SGPA' not in df.columns:
                df['SGPA'] = ''
            if 'Result' not in df.columns:
                df['Result'] = ''

            url = "http://exam.pu.edu.np:9094/"

            for index, row in df.iterrows():
                roll_no = str(row['Exam Roll Number'])
                dob = str(row['Date of Birth'])

                print(f"Processing {roll_no}, {dob}")

                await page.goto(url)

                # Fill the form
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

                await page.fill('#Symbol_Number', roll_no)

                try:
                    dob_date = pd.to_datetime(dob)
                    dob_formatted = dob_date.strftime('%Y-%m-%d')
                    await page.fill('#DOB', dob_formatted)
                except:
                    print(f"Error parsing DOB: {dob}")
                    continue

                # Click Submit
                await page.click('input[type="submit"]')
                
                # Wait for delay to allow user to see
                await page.wait_for_timeout(delay * 1000)
                
                # Placeholder for result extraction (since we don't have selectors)
                # In a real scenario, we would scrape the result here.
                
            
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
