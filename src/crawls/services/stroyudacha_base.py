from scrapy import Spider
from core.db_utils import create_db_objects
from core.utils import (get_list_of_products, get_pagination, get_price,
                        get_random_user_agent)
from db.connect import get_session
from db.tables import stroyudacha_products
from scrapy import Request
from scrapy.http.response.html import HtmlResponse
from crawls.settings import STROY_UDACHA_CONST



class StroyudachaSpiderBase(Spider):

    name = 'stroydacha'
    allowed_domains = ['stroyudacha.ru']
    start_urls = ['https://stroyudacha.ru/']

    # Async db_session
    # from db.connect import get_async_session
    # self.db_session = get_async_session()
    # self.db_session = await self.db_session.__anext__()

    # Sync db_session
    db_session = next(get_session())

    def __str__(self) -> str:
        return self.__class__.__name__

    def __get_categories_urls(self, response: HtmlResponse) -> list[str]:
        """
        Метод получения урлов, всех категорий.
        url: https://stroyudacha.ru/
        """
        return response.xpath(STROY_UDACHA_CONST['xpath_category']).getall()
    
    def __get_subcategories_urls(self, response: HtmlResponse) -> list[str]:
        """
        Метод получения урлов, всех подкатегорий.
        url: https://stroyudacha.ru/groups/<category_name>/
        """
        return response.xpath(
            STROY_UDACHA_CONST['xpath_sub_category']).getall()
    
    def __get_sub_sub_categories_urls(
            self, response: HtmlResponse) -> list[str]:
        """
        Метод получения урлов, всех под-подкатегорий.
        url: https://stroyudacha.ru/groups/<sub_category_name>/
        """
        return response.xpath(
            STROY_UDACHA_CONST['xpath_sub_sub_category']).getall()

    def __get_pagination_amount(self, response: HtmlResponse) -> int:
        """
        Метод получения количества страниц в текущей категории.
        url: https://petrovich.ru/groups/<name_of_category>/
        """
        return get_pagination(response, STROY_UDACHA_CONST)

    def start_requests(self) -> None:
        """Начало запросов."""
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                headers={'User-Agent': get_random_user_agent()})

    def parse(self, response: HtmlResponse) -> None:
        """Парсинг всех категорий на стартовой странице."""
        categories_urls = self.__get_categories_urls(response)
        
        for url in categories_urls:
            yield Request(
                url=url,
                callback=self.parse_category
            )

    def parse_category(self, response: HtmlResponse) -> None:
        """Парсинг подкатегориий на странице категорий."""
        sub_categories_urls = self.__get_subcategories_urls(response)

        for url in sub_categories_urls:
            yield Request(
                url=url,
                callback=self.parse_sub_category
            )

    def parse_sub_category(self, response: HtmlResponse) -> None:
        """
        Парсинг под-подкатегорий на странцие под категорий (если они есть).
        """
        sub_sub_categories_urls = self.__get_sub_sub_categories_urls(response)

        if not sub_sub_categories_urls:
            yield Request(
                url=response.url,
                callback=self.parse_paginated_pages
            )
        
        for url in sub_sub_categories_urls:
            yield Request(
                url=url,
                callback=self.parse_paginated_pages
            )

    def parse_paginated_pages(self, response: HtmlResponse) -> None:
        """
        Парсинг пагинированных товаров
        - Товары добавляются на страницу, поэтому парсим все объекты
          с последней страницы пагинации.
        """
        pagination = self.__get_pagination_amount(response)

        yield Request(
            url=f'{response.url}/?page={pagination}',
            callback=self.parse_items
        )

    def parse_items(self, response: HtmlResponse) -> None:
        """
        Парсинг товаров со страницы
        Atributes:
            - product_names: list[names[str]]
            - product_prices: list[prices[float]]
            - product_urls: list[urls[str]]
            - product_category: str
            - product_measurements: list[str]
        """
        product_names = response.xpath(
            STROY_UDACHA_CONST['xpath_name']).getall()
        
        product_category = response.xpath(
            STROY_UDACHA_CONST['xpath_category_name']
        ).get()

        product_prices = response.xpath(
            STROY_UDACHA_CONST['xpath_price']).getall()
        product_prices = map(get_price, product_prices)

        product_measurements = response.xpath(
            STROY_UDACHA_CONST['xpath_measurement']
        ).getall()

        product_urls = response.xpath(STROY_UDACHA_CONST['xpath_url']).getall()

        product_gcodes = response.xpath(
            STROY_UDACHA_CONST['xpath_gcode']).getall()

        products = get_list_of_products(
            product_names, product_prices, product_urls, product_category,
            None, product_measurements, product_gcodes
        )
        
        create_db_objects(stroyudacha_products, products, self.db_session)
