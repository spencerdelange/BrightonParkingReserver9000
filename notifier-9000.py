import time
from playwright.sync_api import sync_playwright
from win10toast_click import ToastNotifier

def main():
    default_date = "Friday, February 28, 2025"
    default_url = "https://reservenski.parkbrightonresort.com/select-parking"
    timeout = 2

    print("Enter the parking reservation URL")
    url = input(f"e.g. \"{default_url}\" or press Enter for default: ")
    if not url:
        url = default_url

    print("Enter the date to reserve")
    date = input(f"e.g. \"{default_date}\": ")
    if not date:
        date = default_date

    print(f"URL: {url}")
    print(f"Checking for availability on {date}")

    while True:
        try:
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
                        icon_path="",
                    )
                    print(f"✅ Parking spot for {date} might be available!")
                else:
                    print(f"❌ Parking spot not currently available for {date}.")
                browser.close()
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Retrying in {timeout} seconds...")
        time.sleep(timeout)

if __name__ == "__main__":
    main()