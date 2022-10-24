import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime
from fake_useragent import UserAgent


def scrap():
    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')

 #   option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
  #  option.add_argument("--disable-notifications")
    option.add_argument('--disable-blink-features=AutomationControlled')




    url = 'https://fly2.emirates.com/CAB/IBE/SearchAvailability.aspx'
    #url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
  #  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    driver.maximize_window()  # For maximizing window
    driver.set_page_load_timeout(30)
    driver.get(url)
    time.sleep(150)


scrap()
