import time

from scrapy import Request, Spider
from scrapy.http.response.html import HtmlResponse

from core.db_utils import create_db_objects
from core.utils import (get_pagination, get_price,
                        get_random_user_agent)
from db.connect import get_session
from db.tables import leroy_products
from scrapy import Request, Spider
from crawls.settings import LEROY_CONST

import undetected_chromedriver as uc 
# from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LeroySpiderBase(Spider):

    name = 'leroy'
    allowed_domains = ['spb.leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/']

    def __init__(self):

        self.options = uc.ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument(f'User-Agent="{get_random_user_agent()}"')
        self.driver = uc.Chrome(
            options=self.options
        )
        self.db_session = next(get_session())
        
    def __get_categories_urls(self) -> list[str]:
        """
        """
        categories = self.driver.find_elements(
            By.XPATH, LEROY_CONST['xpath_category'])
        return [
            category.get_attribute('href') for category in categories
        ]

    def start_requests(self) -> None:
        """Начало запросов."""
        
        self.driver.get('https://leroymerlin.ru/catalogue/')

        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, LEROY_CONST['xpath_category'])
                )
            )
        # TODO: all categoris
        categories_urls = self.__get_categories_urls()[2:4]

        for url in categories_urls:

            self.driver.get(url)
            counter = 1
            pagination = int(self.driver.find_element(
                By.XPATH, LEROY_CONST['xpath_pagination']).text)

            while counter != pagination:

                product_list = []
                data_list = self.driver.find_elements(
                    By.XPATH, LEROY_CONST['xpath_data_list'])

                for element in data_list:
                        
                    product_name = element.find_element(
                        By.XPATH, LEROY_CONST['xpath_name']).text
                    product_category = self.driver.find_element(
                        By.XPATH, LEROY_CONST['xpath_category_name']).text

                    try:
                        product_price = element.find_element(
                            By.XPATH, LEROY_CONST['xpath_price']).text
                        product_price = get_price(product_price)
                    except Exception:
                        try:
                            product_price = element.find_element(
                                By.XPATH, LEROY_CONST['xpath_best_price']).text
                            product_price = get_price(product_price)
                        except Exception:
                            product_price = None

                    try:
                        product_measurement = element.find_element(
                            By.XPATH, LEROY_CONST['xpath_measurement']).text
                    except Exception:
                        try:
                            product_measurement = element.find_element(
                                By.XPATH, LEROY_CONST['xpath_best_measurement']
                            ).text
                        except Exception:
                            product_measurement = None
                            
                    product_url = element.find_element(
                        By.XPATH, LEROY_CONST['xpath_url']
                    ).get_attribute('href') 
                        
                    product = {
                        'name': product_name,
                        'category': product_category,
                        'price': product_price,
                        'currency': 'Руб.',
                        'measurement': product_measurement,
                            'url': product_url,
                    }
                    product_list.append(product)

                create_db_objects(
                    leroy_products, product_list, self.db_session
                )

                next_page_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, LEROY_CONST['xpath_next_page'])
                        )
                    )
                next_page_button.click()
                counter += 1
                time.sleep(6)

        self.driver.quit()
