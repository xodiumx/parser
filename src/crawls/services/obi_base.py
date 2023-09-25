from time import sleep
from random import choice

from crawls.settings import OBI_CONST

from scrapy import Spider

from core.utils import get_random_user_agent
from db.connect import get_session

# import undetected_chromedriver as uc
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ObiSpiderBase(Spider):
    name = 'obi'
    allowed_domains = ['obi.ru']
    start_urls = ['https://obi.ru/']

    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument(f'User-Agent="{get_random_user_agent()}"')
        self.driver = webdriver.Chrome(
            options=self.options
        )
        self.db_session = next(get_session())

    # TODO: raspisat
    def __get_all_categories(self, categories) -> list[str]:
        
        all_categories = []
        # TODO: add proxies
        prxoies = []

        for url in categories:
            self.driver.proxy = {'http': f'http://{choice(self.proxies)}'}
            self.driver.get(url)

            sleep(2)
            try:
                self.driver.find_element(
                    By.XPATH, OBI_CONST['xpath_data_list']
                )
                all_categories.append(url)
            except Exception:
                sub_sub_categories = self.driver.find_elements(
                    By.XPATH, OBI_CONST['xpath_sub_sub_category']
                )
                sub_sub_categories = {
                    url.get_attribute('href') for url in sub_sub_categories
                }
                all_categories.extend(sub_sub_categories)
                print(sub_sub_categories)
        return all_categories
            

    # TODO: raspisat
    def __get_sub_categories(self, categories) -> list[str]:
        """Функция получения подкатегорий."""
        sub_categories = []

        for category in categories[:OBI_CONST['count_categories']]:
            category.click()
            urls = self.driver.find_elements(
                By.XPATH, OBI_CONST['xpath_sub_category']
            )
            urls = [url.get_attribute('href') for url in urls]
            sub_categories.extend(urls)
            sleep(2)
        return sub_categories


    def __get_categories_urls(self) -> None:
        """Функция получения всех категорий"""
        self.driver.get('https://obi.ru')

        catalog = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, OBI_CONST['xpath_catalog_button'])
            )
        )
        catalog.click()
        sleep(2)

        categories = self.driver.find_elements(
            By.XPATH, OBI_CONST['xpath_category']
        )
        sub_categories = self.__get_sub_categories(categories)
        all_categories_urls = self.__get_all_categories(sub_categories)
        

    def start_requests(self) -> None:
        """Начало запросов."""
        # self.driver.get('https://obi.ru/')
        # TODO: cookies city
        categories = self.__get_categories_urls()
        self.driver.quit()
