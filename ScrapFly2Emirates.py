from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime


class ScrapEmirates:
    def __init__(self):
        self.departure_user, self.arrival_user, self.date_departure_user, self.month_difference = self.user_data()
        self.flight_information = []    # Список для вывода результата
        self.scrap()                    # запуск функции скрапинга сайта
        self.show_result()              # Вывод результата на экран

    def scrap(self):
        option = webdriver.ChromeOptions()
        option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')

        url = 'https://fly2.emirates.com/CAB/IBE/SearchAvailability.aspx'
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        driver.maximize_window()  # For maximizing window
        driver.get(url)

        # прохожу всплывающую страницу
        time.sleep(2)
        try:
            button_accept = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            button_accept.click()
        except NoSuchElementException:
            pass
        time.sleep(1)
        button_new_search = driver.find_element(By.XPATH, '//*[@id="column2"]/div[2]/a')
        button_new_search.click()
        time.sleep(3)

        # Выбираю поле One way (галочка билеты в одну сторону)
        driver.find_element(By.XPATH, '//*[@id="ctl00_c_CtWNW_ltOneway"]').click()

        # Заполняю поле откуда вылет
        departure_airport = driver.find_element(By.XPATH, '//*[@id="ctl00_c_CtWNW_ddlFrom-suggest"]')
        departure_airport.send_keys(self.departure_user)

        # заполняю поле куда прилёт
        arrival_airport = driver.find_element(By.XPATH, '//*[@id="ctl00_c_CtWNW_ddlTo-suggest"]')
        arrival_airport.send_keys(self.arrival_user)

        # клацаю на виджет выбора даты
        departing = driver.find_element(By.XPATH, '//*[@id="txtDepartDate"]')
        departing.click()

        # листаю страницы в таблице выбора даты
        if self.month_difference > 1:
            for i in range(self.month_difference):
                driver.find_element(By.XPATH, '//*[@id="nextMonth"]').click()
                time.sleep(0.3)
        driver.find_element(By.XPATH, f'//*[@id="day-{self.date_departure_user}"]').click()

        # кнопка начать поиск рейсов
        driver.find_element(By.XPATH, '//*[@id="ctl00_c_IBE_PB_FF"]').click()

        for i in range(100):        # Собираю все нужные данные
            x_path = f'//*[@id="ctl00_c_ctlPriceResult_ctl0{i}_IdFlights"]'

            path_price = x_path + '/div[3]/div[2]/div[1]/div'
            path_total_time = x_path + '/div[2]/div/div[1]/div[2]/div[1]/div/div[3]/p/time/span[2]'
            path_departure_time = x_path + '/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/time'
            path_arrival_time = x_path + '/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/time'
            path_departure = x_path + '/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/p'
            path_arrival = x_path + '/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/p'

            try:
                price = driver.find_element(By.XPATH, path_price).text
                total_time = driver.find_element(By.XPATH, path_total_time).text
                departure_time = driver.find_element(By.XPATH, path_departure_time).text
                arrival_time = driver.find_element(By.XPATH, path_arrival_time).text
                departure = driver.find_element(By.XPATH, path_departure).text
                arrival = driver.find_element(By.XPATH, path_arrival).text

                one_flight = {'price': price,
                              'total_time': total_time,
                              'departure_time': departure_time,
                              'arrival_time': arrival_time,
                              'departure': departure,
                              'arrival': arrival}
                self.flight_information.append(one_flight)

            except NoSuchElementException:
                break

    def user_data(self):
        """Функция для получения и обработки вводных данных от юзера"""
        departure_user = input('Enter city and airport of departure (ex. Warsaw (WAW)): ')
        arrival_user = input('Enter the city and airport of arrival (ex. East London (ELS)): ')
        date_departure_user = input('Enter departure date (ex. 27-12-2022): ')  # дата вылета

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
        date_departure_user = f'{day}-{int(date_departure_user[1]) - 1}-{date_departure_user[2]}'
        return departure_user, arrival_user, date_departure_user, month_difference

    def show_result(self):
        if len(self.flight_information) > 0:
            for res in self.flight_information:
                print(res)
        else:
            print('There are no flights offered for the dates or route you selected. Please try a different search')


ScrapEmirates()
