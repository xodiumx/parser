from math import ceil
from crawls.settings import API_KEY_SCRAPEOPS, USER_AGENTS_ENDPOINT
from random import randint

import requests
from scrapy.http.response.html import HtmlResponse

api_key: str = API_KEY_SCRAPEOPS
user_agent_endpoint: str = USER_AGENTS_ENDPOINT


def get_random_user_agent() -> str:
    """Функция получения рандомного USER-AGENT-a."""
    user_agent_list: dict = requests.get(
        url=f'{user_agent_endpoint}{api_key}').json().get('result')
    return user_agent_list[randint(0, len(user_agent_list) - 1)]


def get_price(price: str) -> int:
    """Преобразование спаршеной строки(цены) в число."""
    if not price:
        return None
    if '\xa0' in price:
        price = price.replace('\xa0', '')
    if '\nÄ\nруб.' in price:
        price = price.replace('\nÄ\nруб.', '')
    if ',' in price:
        price = price.replace(',', '.')
    if ' ' in price:
        price = ''.join(map(str, price.split()))
    return float(price)


res = 0


def get_pagination(response: HtmlResponse, const: dict) -> int:
    """
    - достаем число и приводим его к int-у
    - делим на количество товаров на одной странице
    - округляем вверх
    """
    site = const['site']
    xpath = const['xpath_pagination']
    items = const['page_items_amount']

    if site == 'stroyudacha':
        return ceil(int(
            response.xpath(xpath).getall()[0].split(' ')[0]) / items)
    if site == 'petrovich':
        return ceil(int(response.xpath(xpath).getall()[1]) / items)
    if site == 'saturn':
        return int(response.xpath(xpath).getall()[0])


def get_list_of_products(
        product_names: list[str],
        product_prices: list[float],
        product_urls: list[str],
        product_category: str,
        product_cart_prices: list[float],
        product_measurements: list[str],
        product_gcodes: list[str],
    ) -> list[dict]:
    """функция получения списка товаров на текущей странице."""
    if product_cart_prices:
        return [{
            'name': name,
            'gcode': gcode,
            'category': product_category,
            'price': price,
            'cart_price': cart_price,
            'measurement': measurement,
            'currency': 'Руб.',
            'url': url
        } for name, price, url, cart_price, measurement, gcode in zip(
            product_names, product_prices, product_urls,
            product_cart_prices, product_measurements, product_gcodes
        )
        ]
    return [{
        'name': name,
        'gcode': gcode,
        'category': product_category,
        'price': price,
        'measurement': measurement,
        'currency': 'Руб.',
        'url': url
    } for name, price, url, measurement, gcode in zip(
        product_names, product_prices, product_urls,
        product_measurements, product_gcodes
    )
    ]
