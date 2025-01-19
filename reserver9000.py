import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from win10toast import ToastNotifier

class ParkingMonitor:
    def __init__(self):
        self.toaster = ToastNotifier()
        self.chrome_options = Options()

    def check_parking(self, target_aria_label):
        driver = None
        try:
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get('https://reservenski.parkbrightonresort.com/select-parking')

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"div[aria-label='{target_aria_label}']")))
            time.sleep(5)  # Adjust wait time if needed

            target_element = driver.find_element(By.CSS_SELECTOR, f"div[aria-label='{target_aria_label}']")

            style = target_element.get_attribute('style')
            if "background-color: rgba(49, 200, 25, 0.2)" in style:
                self.toaster.show_toast(
                    "Brighton Parking Alert",
                    f"Parking spot for {target_aria_label} might be available!",
                    duration=10,
                    icon_path=None
                )
                print(f"Parking spot for {target_aria_label} might be available!")
            else:
                self.toaster.show_toast(
                    "Brighton Parking Alert",
                    f"No parking spot available for {target_aria_label}!",
                    duration=10,
                    icon_path=None
                )
                print(f"Parking spot not available for {target_aria_label}.")

        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            if driver:
                driver.quit()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py 'Target Aria Label'")
        sys.exit(1)

    target_aria_label = sys.argv[1]
    monitor = ParkingMonitor()

    while True:
        monitor.check_parking(target_aria_label)
        print(f"Waiting for 1 minute to retry...")
        time.sleep(60)  # Retry every 1 minute

if __name__ == "__main__":
    main()