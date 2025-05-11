from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import json
import os

def scrape_porsche_finder():
    print("Setting up Firefox driver...")
    
    # Set up Firefox options
    options = FirefoxOptions()
    options.add_argument("--headless")
    
    try:
        # Set up driver using webdriver_manager
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )
        
        # Go to the URL
        url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Give the page time to load initially
        time.sleep(10)
        
        print("Waiting for vehicle tiles to appear...")
        # Wait for the car listings to load
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='vehicle-tile']"))
        )
        print("Vehicle tiles found!")
        
        # Give extra time for all elements to fully load
        time.sleep(5)
        
        # Get all car listings
        car_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='vehicle-tile']")
        print(f"Found {len(car_elements)} vehicles")
        
        cars_data = []
        for i, car in enumerate(car_elements):
            try:
                print(f"Processing vehicle {i+1}...")
                # Extract data from each car tile
                try:
                    title = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-title']").text
                except Exception as e:
                    print(f"Could not find title: {e}")
                    title = "N/A"
                    
                try:
                    price = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-price']").text
                except Exception as e:
                    print(f"Could not find price: {e}")
                    price = "N/A"
                    
                try:
                    details = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-summary']").text
                except Exception as e:
                    print(f"Could not find details: {e}")
                    details = "N/A"
                
                # Try to get additional details if available
                try:
                    mileage = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-mileage']").text
                except:
                    mileage = "N/A"
                    
                cars_data.append({
                    "title": title,
                    "price": price,
                    "details": details,
                    "mileage": mileage
                })
                print(f"Successfully processed vehicle {i+1}")
            except Exception as e:
                print(f"Error processing vehicle {i+1}: {e}")
        
        # Save data to a JSON file
        with open("porsche_data.json", "w") as f:
            json.dump(cars_data, indent=2, fp=f)
        
        print(f"Data saved to {os.path.abspath('porsche_data.json')}")
        print("Sample data:")
        print(json.dumps(cars_data[:2], indent=2))
        
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
    scrape_porsche_finder()
    print("Script execution completed.")

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import json

def scrape_porsche_finder():
    # Set up Chrome options
    options = uc.ChromeOptions()
    options.headless = True  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Initialize the driver with version_main parameter to match your Chrome version
    driver = uc.Chrome(options=options, version_main=135)  # Specify your Chrome version (135)
    
    # Navigate to the URL
    url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
    print("Loading page...")
    driver.get(url)
    
    try:
        # Wait for the car listings to load
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='vehicle-tile']"))
        )
        print("Page loaded successfully!")
        
        # Give extra time for all elements to fully load
        time.sleep(5)
        
        # Get all car listings
        car_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='vehicle-tile']")
        print(f"Found {len(car_elements)} vehicles")
        
        cars_data = []
        for car in car_elements:
            try:
                # Extract data from each car tile
                title = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-title']").text
                price = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-price']").text
                details = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-summary']").text
                
                cars_data.append({
                    "title": title,
                    "price": price,
                    "details": details
                })
            except Exception as e:
                print(f"Error extracting data from a car listing: {e}")
        
        print(json.dumps(cars_data, indent=2))
        return cars_data
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

# if __name__ == "__main__":
#     scrape_porsche_finder()


# from porsche_scraper import webdriver
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.firefox import GeckoDriverManager
# import time
# import json

# def scrape_porsche_finder():
#     # Set up Firefox options
#     firefox_options = Options()
#     firefox_options.add_argument("--headless")
    
#     # Set up driver
#     driver = webdriver.Firefox(
#         service=Service(GeckoDriverManager().install()),
#         options=firefox_options
#     )
    
#     # Go to the URL
#     url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
#     driver.get(url)
#     print("Loading page...")
    
#     # Wait for the car listings to load
#     try:
#         # Wait for car tiles to appear
#         WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='vehicle-tile']"))
#         )
#         print("Page loaded successfully!")
        
#         # Give extra time for all elements to fully load
#         time.sleep(5)
        
#         # Get all car listings
#         car_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='vehicle-tile']")
#         print(f"Found {len(car_elements)} vehicles")
        
#         cars_data = []
#         for car in car_elements:
#             try:
#                 # Extract data from each car tile
#                 title = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-title']").text
#                 price = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-price']").text
#                 details = car.find_element(By.CSS_SELECTOR, "[data-testid='vehicle-summary']").text
                
#                 cars_data.append({
#                     "title": title,
#                     "price": price,
#                     "details": details
#                 })
#             except Exception as e:
#                 print(f"Error extracting data from a car listing: {e}")
        
#         print(json.dumps(cars_data, indent=2))
#         return cars_data
                
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     scrape_porsche_finder()