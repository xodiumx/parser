from scrapy import Request, Spider
from scrapy.http.response.html import HtmlResponse

from core.db_utils import create_db_objects
from core.utils import (get_pagination, get_price,
                        get_random_user_agent)
from db.connect import get_session
from db.tables import petrovich_products
from scrapy import Request, Spider
from crawls.settings import PETROVICH_CONST


class PetrovichSpiderBase(Spider):
    
    name = 'petrovich'
    allowed_domains = ['petrovich.ru']
    start_urls = ['https://petrovich.ru/catalog/']
    main_url = 'https://petrovich.ru'

    def __str__(self) -> str:
        return self.__class__.__name__

    def __get_categories_urls(self, response: HtmlResponse) -> list[str]:
        """
        Метод получения урлов, всех категорий товаров.
        url: https://petrovich.ru/catalog/
        """
        categories = response.xpath('//section/div[1]')
        categories = categories.xpath(
            PETROVICH_CONST['xpath_category']).getall()
        return [categorie.split('/catalog/')[1] for categorie in categories]
    
    def __get_pagination_amount(self, response: HtmlResponse) -> int:
        """
        Метод получения количества страниц в текущей категории.
        url: https://petrovich.ru/catalog/<id>/
        """
        return get_pagination(response, PETROVICH_CONST)
    
    def start_requests(self) -> None:
        """Начало запросов."""
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                headers={'User-Agent': get_random_user_agent()})
    
    def parse(self, response: HtmlResponse) -> None:
        """
        - Первоначальный запрос на:
          endpoint: https://petrovich.ru/catalog/
        - Получение всех категорий товаров
        - Запросы в цикле к страницам всех категорий
        """
        categories_urls = self.__get_categories_urls(response)

        # Async db_session
        # from db.connect import get_async_session
        # self.db_session = get_async_session()
        # self.db_session = await self.db_session.__anext__()

        # Sync db_session
        self.db_session = next(get_session())

        for url in categories_urls:
            yield Request(
                url=f'{self.start_urls[0]}{url}',
                callback=self.parse_category
            )

    def parse_category(self, response: HtmlResponse) -> None:
        """
        - Получение колличества товаров в данной категории
        - Запрросы в цикле к страницам товаров в данной категории
        """
        pagination = self.__get_pagination_amount(response)
        category_url = response.url

        for page in range(pagination):
            yield Request(
                url=f'{category_url}?p={page}',
                callback=self.parse_paginated_items
            )

    def parse_paginated_items(self, response: HtmlResponse) -> None:
        """
        - Получение информации о товаре на текущей странице
        Attributes:
            - product_names: list[names[str]]
            - product_prices: list[prices[float]]
            - product_urls: list[urls[str]]
            - product_category: str
            - product_cart_pricesL list[prices[float]]
            - product_measurements: list[str]
        """
        products_list = []
        data_list = response.xpath(PETROVICH_CONST['data_list'])
        
        for element in data_list:
            product_name = element.xpath(PETROVICH_CONST['xpath_name']).get()
            product_category = response.xpath(
                PETROVICH_CONST['xpath_category_name']).get()
            
            product_cart_price = element.xpath(
                PETROVICH_CONST['xpath_cart_price']).get()
            product_cart_price = get_price(product_cart_price)

            product_price = element.xpath(PETROVICH_CONST['xpath_price']).get()
            product_price = get_price(product_price)

            if not product_price:
                product_price = product_cart_price

            product_measurement = element.xpath(
                PETROVICH_CONST['xpath_measurement']).get()
            
            product_url = element.xpath(PETROVICH_CONST['xpath_url']).get()
            product_url = f'{self.main_url}{product_url}'

            product_gcode = element.xpath(
                PETROVICH_CONST['xpath_gcode']).get()
            
            product = {
                'name': product_name,
                'gcode': product_gcode,
                'category': product_category,
                'price': product_price,
                'cart_price': product_cart_price,
                'currency': 'Руб.',
                'measurement': product_measurement,
                'url': product_url,
            }
            products_list.append(product)

        create_db_objects(petrovich_products, products_list, self.db_session)
