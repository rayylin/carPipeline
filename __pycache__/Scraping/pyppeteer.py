import asyncio
from pyppeteer import launch
import json

async def scrape_porsche_finder():
    # Launch the browser
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    
    # Navigate to the website
    url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
    print("Loading page...")
    await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})
    
    # Wait for the content to load
    await page.waitForSelector('[data-testid="vehicle-tile"]', {'timeout': 60000})
    print("Page loaded successfully!")
    
    # Give the page a moment to fully render
    await asyncio.sleep(3)
    
    # Extract data
    cars_data = await page.evaluate('''() => {
        const cars = [];
        const carElements = document.querySelectorAll('[data-testid="vehicle-tile"]');
        
        carElements.forEach(car => {
            const titleEl = car.querySelector('[data-testid="vehicle-title"]');
            const priceEl = car.querySelector('[data-testid="vehicle-price"]');
            const detailsEl = car.querySelector('[data-testid="vehicle-summary"]');
            
            cars.push({
                title: titleEl ? titleEl.textContent.trim() : 'N/A',
                price: priceEl ? priceEl.textContent.trim() : 'N/A',
                details: detailsEl ? detailsEl.textContent.trim() : 'N/A'
            });
        });
        
        return cars;
    }''')
    
    print(f"Found {len(cars_data)} vehicles")
    print(json.dumps(cars_data, indent=2))
    
    await browser.close()
    return cars_data

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(scrape_porsche_finder())