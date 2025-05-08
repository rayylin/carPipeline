from requests_html import HTMLSession
import json
import time

def scrape_porsche_finder():
    session = HTMLSession()
    
    # Go to the URL
    url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
    print("Loading page...")
    
    response = session.get(url)
    
    # Render JavaScript
    response.html.render(sleep=5, timeout=60)
    print("Page rendered with JavaScript!")
    
    # Get all car listings
    car_elements = response.html.find('[data-testid="vehicle-tile"]')
    print(f"Found {len(car_elements)} vehicles")
    
    cars_data = []
    for car in car_elements:
        try:
            title_element = car.find('[data-testid="vehicle-title"]', first=True)
            price_element = car.find('[data-testid="vehicle-price"]', first=True)
            details_element = car.find('[data-testid="vehicle-summary"]', first=True)
            
            title = title_element.text if title_element else 'N/A'
            price = price_element.text if price_element else 'N/A'
            details = details_element.text if details_element else 'N/A'
            
            cars_data.append({
                "title": title,
                "price": price,
                "details": details
            })
        except Exception as e:
            print(f"Error extracting data from a car listing: {e}")
    
    print(json.dumps(cars_data, indent=2))
    session.close()
    return cars_data

if __name__ == "__main__":
    scrape_porsche_finder()