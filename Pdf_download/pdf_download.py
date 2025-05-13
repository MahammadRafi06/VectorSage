import asyncio
import sys
import csv
import pandas as pd
######################Manually Install playwrit application on the system, otherwise you will get OSError/Runtime Erros############ Use Colab for best exp

df = pd.read_csv('CIDandName.csv') ###This CSV file should have two columns 1. CID and 2. Name of the compound. Use https://pubchem.ncbi.nlm.nih.gov/idexchange/idexchange.cgi
#with UNIIs found in the FDA data to download thsi file. 

lst1 = df['A'].to_list()
lst2 = df['B'].to_list()
lst3=[subs.replace(" ", "_") for subs in lst2]
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from playwright.async_api import async_playwright

async def url_to_pdf(url, output_path):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until='networkidle')
            await page.pdf(
                path=output_path,
                format='A4',
                print_background=True,
                margin={'top': '20px', 'bottom': '20px', 'left': '20px', 'right': '20px'}
            )
            await browser.close()
        print(f"PDF saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
for i in range((len(lst1))):
    url = f'https://pubchem.ncbi.nlm.nih.gov/compound/{i}'
    output_path = f'{lst1[i]}_{lst3[i]}.pdf'
    await url_to_pdf(url, output_path)