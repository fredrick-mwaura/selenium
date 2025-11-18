import time

from selenium.webdriver.support.wait import WebDriverWait

from basics.start_driver import start_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ElementByState():
    driver = start_driver()

    def d_enable_display(self):
        self.driver.get("https://www.w3schools.com/howto/howto_js_toggle_hide_show.asp")
        elem = self.driver.find_element(By.XPATH, "//div[@id='myDIV']").is_displayed()

        print(elem)
        time.sleep(2)
        el = self.driver.find_element(By.XPATH, "//div[@id='myDIV']").click()
        print(el)

    def d_is_displayed_yatra(self):
        self.driver.get("https://www.yatra.com/hotels")
        self.driver.find_element(By.XPATH, "//label[normalize-space()='Traveller and Hotel']").click()
        self.driver.find_element(By.XPATH, "//div[@class='hotel_passegerBox dflex relative']//div[3]//div[1]//div[1]//span[2]")
        elem = self.driver.find_element(By.XPATH, "//select[@class='ageselect']").is_displayed()
        print(elem)

    """
    handling check boxes
    """
    def d_checkboxes(self):
        self.driver.get("https://portal.mut.ac.ke")
        print(f"current url: {self.driver.current_url}")
        checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "RememberMe"))
        )
        checkbox.click()
        print("checked")

        time.sleep(10)

p = ElementByState()

# p.d_enable_display()
# p.d_is_displayed_yatra()
p.d_checkboxes()
