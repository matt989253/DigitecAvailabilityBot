import time
import json
import sys

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================================================================================== #

def checkAvailability(url, wait, headless, driver):
    driver.get(url) # Open url

    availabilityElement = driver.find_element(By.CSS_SELECTOR, ".Z14t") # Get availability element
    titleElement = driver.find_element(By.CSS_SELECTOR, ".productHeaderTitle__Title-gtvrqo-0") # Get title element
    
    availability = availabilityElement.text
    name = titleElement.text

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    print(now + " - " + name + " - " + availability, flush=True)
    
    driver.quit() # quit driver


# ================================================================================== #

url = sys.argv[1] # product url
wait = int(sys.argv[2]) # time to wait in secconds
headless = json.loads(sys.argv[3].lower()) # Whether to run driver in headless mode or not

options = webdriver.FirefoxOptions()
options.headless = headless

try:
    while True:
        driver = webdriver.Firefox(executable_path=r"./geckodriver.exe", options = options)
        checkAvailability(url, wait, headless, driver)
        time.sleep(wait)
finally:
    driver.quit() # quit driver
# ================================================================================== #