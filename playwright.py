import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_porsche_finder():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Loading page...")
        
        # Navigate to the page
        url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
        await page.goto(url, wait_until="networkidle")
        
        # Wait for the vehicle tiles to load
        await page.wait_for_selector('[data-testid="vehicle-tile"]', timeout=60000)
        print("Page loaded successfully!")
        
        # Give extra time for all content to render
        await asyncio.sleep(3)
        
        # Extract data from each car tile
        cars_data = await page.evaluate('''
            () => {
                const carElements = document.querySelectorAll('[data-testid="vehicle-tile"]');
                return Array.from(carElements).map(car => {
                    const titleElement = car.querySelector('[data-testid="vehicle-title"]');
                    const priceElement = car.querySelector('[data-testid="vehicle-price"]');
                    const detailsElement = car.querySelector('[data-testid="vehicle-summary"]');
                    
                    return {
                        title: titleElement ? titleElement.textContent.trim() : 'N/A',
                        price: priceElement ? priceElement.textContent.trim() : 'N/A',
                        details: detailsElement ? detailsElement.textContent.trim() : 'N/A'
                    };
                });
            }
        ''')
        
        print(f"Found {len(cars_data)} vehicles")
        print(json.dumps(cars_data, indent=2))
        
        await browser.close()
        return cars_data

if __name__ == "__main__":
    asyncio.run(scrape_porsche_finder())