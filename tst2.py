from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import random
import time


def scrap_fora():
    print('Scraping Fora started')
    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
  #  option.add_argument("--disable-notifications")
    option.add_argument('--disable-blink-features=AutomationControlled')

    url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.maximize_window()  # For maximizing window
    driver.get(url)
    time.sleep(150)


scrap_fora()
