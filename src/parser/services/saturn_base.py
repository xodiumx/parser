from parser.settings import SATURN_CONST

from scrapy import Spider
from core.db_utils import create_db_objects
from core.utils import (get_pagination, get_price,
                        get_random_user_agent)
from db.connect import get_session
from db.tables import saturn_products
from scrapy import Request
from scrapy.http.response.html import HtmlResponse


class SaturnSpiderBase(Spider):
    
    name = "saturn"
    allowed_domains = ["spb.newsaturn.ru"]
    start_urls = ["https://spb.newsaturn.ru"]

    db_session = next(get_session())

    def __str__(self) -> str:
        return self.__class__.__name__

    def __get_categories_urls(self, response: HtmlResponse) -> list[str]:
        """
        Метод получения урлов, всех категорий.
        - Удаляем нулевой элемент, категорию - news
        url: https://spb.newsaturn.ru
        """
        urls = response.xpath(SATURN_CONST['xpath_category']).getall()
        urls.pop(0)
        return urls
    
    def __get_pagination_amount(self, response: HtmlResponse) -> int:
        """
        Метод получения количества страниц в текущей категории.
        url: https://spb.newsaturn.ru/catalog/<name>/
        """
        return get_pagination(response, SATURN_CONST)

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
                url=f'{response.url}{url}',
                callback=self.parse_categories,
                headers={'Connection': 'keep-alive'}
            )

    def parse_categories(self, response: HtmlResponse) -> None:
        """
        Парсинг категорий
        - Проход по страницам пагинации
        """
        pagination = self.__get_pagination_amount(response)

        for page in range(1, pagination):
            yield Request(
                url=f'{response.url}?page={page}',
                callback=self.parse_items,
                headers={'Connection': 'keep-alive'}
            )

    # TODO: add doc-string
    def parse_items(self, response: HtmlResponse) -> None:
        """
        
        """
        product_list = []
        data_list = response.xpath(SATURN_CONST['xpath_data_list'])

        for element in data_list:
            
            product_name = element.xpath(
                SATURN_CONST['xpath_name']).get().strip()
            product_category = response.xpath(
                SATURN_CONST['xpath_category_name']).get().strip()

            try:
                product_cart_price = element.xpath(
                    SATURN_CONST['xpath_cart_price']).get()
                product_cart_price = get_price(product_cart_price)
            except Exception:
                product_cart_price = None

            try:
                product_price = element.xpath(
                    SATURN_CONST['xpath_price']).get()
                product_price = get_price(product_price)
            except Exception:
                product_price = product_cart_price
            
            try:
                product_measurement = element.xpath(
                    SATURN_CONST['xpath_measurement']).get().strip()
            except Exception:
                product_measurement = None
            
            product_url = element.xpath(SATURN_CONST['xpath_url']).get()
            
            product = {
                'name': product_name,
                'category': product_category,
                'price': product_price,
                'cart_price': product_cart_price,
                'currency': 'Руб.',
                'measurement': product_measurement,
                'url': f'{self.start_urls[0]}{product_url}',
            }
            product_list.append(product)

        create_db_objects(saturn_products, product_list, self.db_session)
