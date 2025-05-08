from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def scrape_porsche_finder():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    
    # Set up driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Go to the URL
    url = "https://finder.porsche.com/us/en-US/search?position=10001%2C40.75368539999999%2C-73.9991637%2C50"
    driver.get(url)
    print("Loading page...")
    
    # Wait for the car listings to load
    try:
        # Wait for car tiles to appear
        WebDriverWait(driver, 30).until(
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

if __name__ == "__main__":
    scrape_porsche_finder()