from selenium import webdriver
from selenium.webdriver.chrome.service import Service as cmService
from selenium.webdriver.chrome.options import Options as cmOptions
import time
from webdriver_manager.chrome import ChromeDriverManager


# Chrome options
chrome_options = cmOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Optional: run headless if you don't want the browser to open
# chrome_options.add_argument("--headless=new")

service = cmService("/home/frd/browserdrivers/chromedriver")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=cmService(ChromeDriverManager().install()))



# Load your site
driver.get("https://portal.mut.ac.ke")
driver.maximize_window()

print("Page title: ", driver.title)

# Keep the browser open for a while
time.sleep(1000000)

driver.quit()