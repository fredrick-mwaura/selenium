from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def start_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    # options.add_argument('--headless=new')

    return webdriver.Chrome(options=options)