from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

def scrape_porsche_finder():
    print("Setting up Chrome driver...")
    
    # Set up Chrome options
    options = Options()
    
    # Comment out headless mode for debugging - sometimes websites behave differently in headless mode
    # options.add_argument("--headless")
    
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    
    # Add user agent to make it look more like a real browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.115 Safari/537.36")
    
    # Print current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        # Set up driver directly without webdriver_manager
        driver = webdriver.Chrome(options=options)
        
        # Go to the URL
        url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for page to load
        print("Waiting for page load...")
        time.sleep(10)
        
        # See what elements are visible
        print("Current page source length:", len(driver.page_source))
        
        # Try to locate the vehicle tiles with different selectors
        selectors_to_try = [
            "[data-testid='vehicle-tile']",
            ".vehicle-tile",
            ".vehicle-card",
            ".search-results-item",
            "[data-testid*='vehicle']",
            "[class*='vehicle']",
            "[class*='card']"
        ]
        
        vehicle_elements = None
        selector_used = None
        
        for selector in selectors_to_try:
            print(f"Trying selector: {selector}")
            try:
                # First check if there are any matching elements
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Found {len(elements)} elements with selector: {selector}")
                    vehicle_elements = elements
                    selector_used = selector
                    break
            except Exception as e:
                print(f"Error with selector {selector}: {e}")
        
        if not vehicle_elements:
            print("Could not find vehicle elements with any selector.")
            print("Taking screenshot for debugging...")
            driver.save_screenshot("porsche_page.png")
            print(f"Screenshot saved to {os.path.abspath('porsche_page.png')}")
            
            # Let's look at the HTML structure to help debug
            html_sample = driver.page_source[:5000] + "..." if len(driver.page_source) > 5000 else driver.page_source
            with open("porsche_html.txt", "w", encoding="utf-8") as f:
                f.write(html_sample)
            print(f"Sample HTML saved to {os.path.abspath('porsche_html.txt')}")
            
            return []
        
        print(f"Using selector: {selector_used}")
        
        # Try to extract data
        cars_data = []
        for i, car in enumerate(vehicle_elements):
            try:
                print(f"Processing vehicle {i+1}...")
                
                # Let's try to extract text from the entire element if specific data is hard to find
                car_html = car.get_attribute('innerHTML')
                car_text = car.text
                
                # Save this for debugging
                with open(f"car_{i+1}_html.txt", "w", encoding="utf-8") as f:
                    f.write(car_html)
                
                with open(f"car_{i+1}_text.txt", "w", encoding="utf-8") as f:
                    f.write(car_text)
                
                # Try to extract structured data
                car_data = {
                    "full_text": car_text,
                    "position": i+1
                }
                
                # Try different selectors for title, price, etc.
                try:
                    car_data["title"] = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-title']").text
                except:
                    try:
                        car_data["title"] = car.find_element(By.CSS_SELECTOR, "*[class*='title']").text
                    except:
                        car_data["title"] = "Could not extract title"
                
                try:
                    car_data["price"] = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-price']").text
                except:
                    try:
                        car_data["price"] = car.find_element(By.CSS_SELECTOR, "*[class*='price']").text
                    except:
                        car_data["price"] = "Could not extract price"
                
                cars_data.append(car_data)
                print(f"Extracted data for vehicle {i+1}")
                
            except Exception as e:
                print(f"Error processing vehicle {i+1}: {e}")
        
        # Save the extracted data
        with open("porsche_cars_data.json", "w") as f:
            json.dump(cars_data, indent=2, fp=f)
        
        print(f"Data saved to {os.path.abspath('porsche_cars_data.json')}")
        if cars_data:
            print("Sample data:")
            print(json.dumps(cars_data[0], indent=2))
        
        return cars_data
                
    except Exception as e:
        print(f"Main error: {e}")
        return []
    finally:
        try:
            driver.quit()
            print("Driver closed successfully")
        except:
            print("Note: Driver may have already been closed")

if __name__ == "__main__":
    print("Starting Porsche finder scraper...")
    cars = scrape_porsche_finder()
    print(f"Script completed. Found {len(cars)} vehicles.")

# import requests
# import json
# import time

# def scrape_porsche_finder_api():
#     """
#     Use the Porsche finder API directly to get vehicle data.
#     This avoids browser automation issues.
#     """
#     print("Starting API-based scraper...")
    
#     # Headers to mimic a browser
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept': 'application/json',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Origin': 'https://finder.porsche.com',
#         'Referer': 'https://finder.porsche.com/us/en-US/'
#     }
    
#     # The actual API endpoint Porsche uses to load vehicle data
#     api_url = "https://finder.porsche.com/api/inventory/search"
    
#     # Parameters similar to what's in the original URL
#     params = {
#         "zip": "10001",
#         "lat": "40.75368539999999",
#         "lon": "-73.9991637",
#         "radius": "50",
#         "locale": "en-US",
#         "limit": "50",  # Get up to 50 results
#         "page": "1"
#     }
    
#     try:
#         print(f"Sending request to {api_url}...")
#         response = requests.get(api_url, params=params, headers=headers)
        
#         # Check if the request was successful
#         if response.status_code == 200:
#             print("Request successful!")
#             data = response.json()
            
#             # Process the data - this structure may need adjustment based on actual API response
#             if 'results' in data:
#                 vehicles = data['results']
#                 print(f"Found {len(vehicles)} vehicles")
                
#                 processed_vehicles = []
#                 for vehicle in vehicles:
#                     try:
#                         car_info = {
#                             "title": vehicle.get('modelDescription', 'N/A'),
#                             "price": f"${vehicle.get('price', 'N/A')}",
#                             "year": vehicle.get('year', 'N/A'),
#                             "mileage": f"{vehicle.get('mileage', 'N/A')} miles",
#                             "vin": vehicle.get('vin', 'N/A'),
#                             "dealer": vehicle.get('dealer', {}).get('name', 'N/A'),
#                             "location": vehicle.get('dealer', {}).get('city', 'N/A')
#                         }
#                         processed_vehicles.append(car_info)
#                     except Exception as e:
#                         print(f"Error processing vehicle: {e}")
                
#                 # Save the data to a file
#                 with open("porsche_data_api.json", "w") as f:
#                     json.dump(processed_vehicles, indent=2, fp=f)
                
#                 print(f"Data saved to porsche_data_api.json")
#                 print("Sample data:")
#                 print(json.dumps(processed_vehicles[:2], indent=2) if processed_vehicles else "No data found")
                
#                 return processed_vehicles
#             else:
#                 print(f"API response doesn't contain expected 'results' field.")
#                 print(f"Response keys: {list(data.keys())}")
                
#                 # Save the raw response for inspection
#                 with open("porsche_raw_response.json", "w") as f:
#                     json.dump(data, indent=2, fp=f)
#                 print("Saved raw response to porsche_raw_response.json for inspection")
                
#                 return []
#         else:
#             print(f"Request failed with status code: {response.status_code}")
#             print(f"Response: {response.text}")
#             return []
            
#     except Exception as e:
#         print(f"Error: {e}")
#         return []

# if __name__ == "__main__":
#     print("Starting Porsche finder API scraper...")
#     results = scrape_porsche_finder_api()
#     print(f"Script completed. Found {len(results)} vehicles.")