from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as cmService
from selenium.webdriver.chrome.options import Options as cmOptions
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
from basics.start_driver import start_driver

password = getpass.getpass("Enter your password: ")

class LoginAutomation:

    def login_with_button_click(self):

        # Initialize driver
        driver = start_driver()
        try:
            # Navigate to your login page
            driver.get("https://portal.mut.ac.ke")
            driver.maximize_window()

            # Fill login credentials first
            self.fill_login_credentials(driver)

            # Method 1: Click by exact class combination
            try:
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button.btn.btn-color.btn-md.primary-btn.text-decoration-none"))
                )
                login_button.click()
                print("Login button clicked using exact class combination")
                driver.get("https://portal.mut.ac.ke/Academic/Reports?isresult=true")
                current_url = driver.current_url
                print(f"navigating to url: {current_url}")
            except Exception as e:
                print(f"Method 1 failed: {e}")
                driver.close()

            # Wait for login to complete and verify
            self.verify_login_success(driver)

        finally:
            time.sleep(500000000)
            driver.quit()

    def fill_login_credentials(self, driver):
        """Fill in the login form fields"""
        credentials = {
            "exampleFormControlInput1": "sc200/0601/2022",
            "password": password,
        }

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "RememberMe"))
        ).click()

        for field_id, value in credentials.items():
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, field_id))
                )
                element.clear()
                element.send_keys(value)
                print(f"Filled {field_id} field")
            except Exception as e:
                print(f"Could not fill {field_id}: {e}")

    def verify_login_success(self, driver):
        """Verify that login was successful"""
        try:
            # Wait for URL change or specific element that appears after login
            WebDriverWait(driver, 10).until(
                lambda driver: driver.current_url != "https://portal.mut.ac.ke/Home/StudentDashboard"
            )
            print("Login successful - URL changed")
        except:
            try:
                # Look for logout button or user profile element
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".logout, .profile, .user-avatar, [href*='logout']"))
                )
                print("Login successful - User elements found")
            except Exception as e:
                print(f"Login status uncertain: {e}")


# Usage examples:
login_auto = LoginAutomation()

# Method 1: Simple login with button click
login_auto.login_with_button_click()

# login_auto.alternative_login_methods()
# login_auto.smart_login_detection()
# login_auto.verify_login_success()