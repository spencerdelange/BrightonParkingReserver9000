import time
import sys
from playwright.sync_api import sync_playwright
from win10toast_click import ToastNotifier
       
def main():
    if len(sys.argv) != 2:
        print("Usage: python reserver9000.py <date>")
        print("e.g. 'python reserver9000.py Friday, February 21, 2025'")
        sys.exit(1)

    url = "https://reservenski.parkbrightonresort.com/select-parking"
    date = sys.argv[1]
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
 
            page.wait_for_selector(f"div[aria-label='{date}']", timeout=20000)
            print("Got element, waiting so it may load")
            time.sleep(1)
            if "background-color: rgba(49, 200, 25, 0.2)" in page.query_selector(f"div[aria-label='{date}']").get_attribute("style"):
                ToastNotifier().show_toast(
                    "Brighton ParkingReservation  Alert",
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
