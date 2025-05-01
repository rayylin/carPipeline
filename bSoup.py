from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Load the dynamic site
    url = "https://finder.porsche.com/us/en-US/search?int_ref=carsales&int_medium=email&int_position=show_details&position=10001%2C40.75368539999999%2C-73.9991637%2C50&order=closest&int_id=savedsearch"
    page.goto(url)

    # Wait for vehicle cards to load
    page.wait_for_selector('.VehicleCard_card__')

    # Get page content
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    # Extract data
    cars = soup.select('.VehicleCard_card__')
    for car in cars:
        print(car.get_text(strip=True))

    browser.close()