import time
import sys
from playwright.sync_api import sync_playwright
from win10toast_click import ToastNotifier
       
def main():
    if len(sys.argv) < 3:
        print("Usage: python reserver9000.py <date> <parking reservation site>")
        print("e.g. 'python reserver9000.py \"Friday, February 21, 2025\" https://reserve.altaparking.com/select-parking'")
        print("Note: Put the date in quotes if it contains spaces")
        sys.exit(1)
    
    date = sys.argv[1]
    url = sys.argv[2]
    
    print(f"Checking for availability on {date}")
    print(f"URL: {url}")
    
    while True:
        with sync_playwright() as p:
            browser = p.webkit.launch(
                headless=True,
                args=['--disable-gpu']
            )
            page = browser.new_page()
            print("Fetching webpage with Playwright")
            page.goto(url, timeout=30000)
            print("Fetched site, waiting for element")
 
            selector = f"div[aria-label='{date.replace('\'', '\\\'').replace('\"', '\\\"')}']"
            page.wait_for_selector(selector, timeout=20000)
            print("Got element, waiting so it may load")
            time.sleep(1)
            
            element = page.query_selector(selector)
            if element and "background-color: rgba(49, 200, 25, 0.2)" in element.get_attribute("style"):
                ToastNotifier().show_toast(
                    "Parking Reservation Alert",
                    f"Parking spot for {date} might be available.",
                    duration=2,
                )
                print(f"✅ Parking spot for {date} might be available!")
            else:
                print(f"❌ Parking spot not currently available for {date}.")
            browser.close()
        time.sleep(1)
 
if __name__ == "__main__":
    main()