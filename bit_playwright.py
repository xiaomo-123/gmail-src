from bit_api import *
import time
import asyncio
from playwright.async_api import async_playwright, Playwright



async def run(playwright: Playwright):
  # browser_ids = getBrowserIds()
  # browser_id=browser_ids[1]  
  browser_id = createBrowser()   
  update_proxy_for_single_window(browser_id) 
  res = openBrowser(browser_id)
  ws = res['data']['ws']
  print("ws address ==>>> ", ws)

  chromium = playwright.chromium
  browser = await chromium.connect_over_cdp(ws)
  default_context = browser.contexts[0]

  print('new page and goto IP query API')

  page = await default_context.new_page()
  await page.goto('https://api.ipify.org?format=json')

  time.sleep(100)

  print('clsoe page and browser')
  await page.close()

  time.sleep(2)
  closeBrowser(browser_id)

async def main():
    async with async_playwright() as playwright:
      await run(playwright)

asyncio.run(main())