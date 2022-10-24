import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime


def scrap():
    departure_user, arrival_user, date_departure_user, month_difference = user_data()

    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
 #   option.add_argument("--disable-notifications")
 #   option.add_argument('--disable-blink-features=AutomationControlled')

    url = 'https://fly2.emirates.com/CAB/IBE/SearchAvailability.aspx'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.maximize_window()  # For maximizing window
    driver.set_page_load_timeout(30)
    driver.get(url)
    time.sleep(1)

    # дохожу до нужной мне страницы
    time.sleep(2)
    try:
        button_accept = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        button_accept.click()
    except:
        pass
    time.sleep(1)
    button_new_search = driver.find_element(By.XPATH, '//*[@id="column2"]/div[2]/a')
    button_new_search.click()
    time.sleep(3)

    while True:
        # Выбираю поле One way
        driver.find_element(By.XPATH, '//*[@id="ctl00_c_CtWNW_ltOneway"]').click()
        time.sleep(3) # time
        # Заполняю поле откуда вылет
        departure_airport = driver.find_element(By.XPATH, '//*[@id="ctl00_c_CtWNW_ddlFrom-suggest"]')
        departure_airport.send_keys(departure_user)
        time.sleep(3) # time
        # заполняю поле куда прилёт
        arrival_airport = driver.find_element(By.XPATH, '//*[@id="ctl00_c_CtWNW_ddlTo-suggest"]')
        arrival_airport.send_keys(arrival_user)
        time.sleep(3) # time

        # выбираю дату
        departing = driver.find_element(By.XPATH, '//*[@id="txtDepartDate"]')
        time.sleep(3) # time
        driver.execute_script("window.scrollTo(0, 175);")
        time.sleep(3) # time
        departing.click()
        time.sleep(3) # time
        # листаю страницы в таблице выбора даты
        if month_difference > 1:
            for i in range(month_difference):
                driver.find_element(By.XPATH, '//*[@id="nextMonth"]').click()
                time.sleep(0.3)
        time.sleep(3) # time
        driver.find_element(By.XPATH, f'//*[@id="day-{date_departure_user}"]').click()
        driver.find_element(By.XPATH, '//*[@id="ctl00_c_IBE_PB_FF"]').click()
        time.sleep(5)

        try:
            driver.find_element(By.XPATH, '//*[@id="column2"]/div[2]/a').click()
        except:
            break

    time.sleep(50)

def user_data():
    departure_user = input('Enter city and airport of departure (ex. Warsaw (WAW)): ')
    arrival_user = input('Enter the city and airport of arrival (ex. East London (ELS)): ')
    date_departure_user = input('Enter departure date (ex. 27-12-2022): ')     # дата вылета

    # высчитываю разницу в месяцах (пригодиться, чтобы накликивать в таблице нужный месяц и год)
    date_departure_user = date_departure_user.split('-')
    user_datatime = datetime.datetime(year=int(date_departure_user[2]),
                                      month=int(date_departure_user[1]),
                                      day=int(date_departure_user[0])).date()

    now_data = datetime.datetime.now().date()
    month_difference = (user_datatime - now_data).days // 30

    # в XPATH используется формат 5-0-2023, по этому обрабатываю числа >10
    day = date_departure_user[0][1] if int(date_departure_user[0]) < 10 else date_departure_user[0]
    # отнимаю от даты юзера 1 месяц (почему-то XPATH на сайте созданы со смещением в один месяц назад: 0-11)
    date_departure_user = f'{day}-{int(date_departure_user[1])-1}-{date_departure_user[2]}'
    return departure_user, arrival_user, date_departure_user, month_difference


scrap()
