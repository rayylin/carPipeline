from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set to True after debugging
    context = browser.new_context()
    page = context.new_page()

    # Collect JSON data
    def handle_response(response):
        if "application/json" in response.headers.get("content-type", ""):
            print(f"\n[JSON] {response.url}")
            try:
                data = response.json()
                # Look for structure with car listings
                print(json.dumps(data, indent=2)[:2000])
            except Exception as e:
                print(f"Error parsing JSON: {e}")

    page.on("response", handle_response)

    # Load the search page
    url = "https://finder.porsche.com/us/en-US/search?int_ref=carsales&int_medium=email&int_position=show_details&position=10001%2C40.75368539999999%2C-73.9991637%2C50&order=closest&int_id=savedsearch"
    page.goto(url)

    # Optional: Scroll to trigger more data
    page.mouse.wheel(0, 8000)
    page.wait_for_timeout(10000)

    browser.close()