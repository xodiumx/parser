from parser.settings import (ELASTICSEARCH_AVAILABLE_DIFF, ELASTICSEARCH_HOST,
                             ELASTICSEARCH_PORT, ELASTICSEARCH_SEARCH_SCORE,
                             VIMOS_PRODUCTS_LIMIT, VIMOS_PRODUCTS_URL)

import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from sqlalchemy.sql.schema import Table

from db.tables import vimos_products


def find_same_products(
        longest_table: str,
        shortest_table: str,
        search_data: list[dict], ) -> list[dict]:
    """
        - Проходимся по товарам короткой таблицы и ищем похожие имена товаров
          в более длинной таблице.
        - В результат попадают найденные товары у которых score > 20
        """
    es_connection = Elasticsearch([
        {
            'host': ELASTICSEARCH_HOST,
            'port': ELASTICSEARCH_PORT,
            'scheme': 'http'
        }
    ])

    result = []
    search = Search(using=es_connection, index=f'{longest_table}')
    for product in search_data:
        name_to_search = product['name']

        if name_to_search:
            search_query = search.query('match', name=name_to_search)
            response = search_query.execute()

        for competitor_product in response:
            compare = {
                f'{shortest_table}': {
                    'name': product['name'],
                    'price': product.get('price', 1)
                },
                f'{longest_table}': {
                    'score': competitor_product.meta.score,
                    'name': competitor_product.name,
                    'price': competitor_product.price
                }
            }
            result.append(compare)
            break
    return [
        item for item in result
        if item[f'{longest_table}']['score'] > ELASTICSEARCH_SEARCH_SCORE
    ]


def calculate_diffs_of_prices(
        longest_table: str,
        shortest_table: str,
        compare: list[dict], ) -> list[dict]:
    """
    Функция вычисления показателей разности цен
    - abs_diff - абсолютная разница цен
    - relative_diff - относительная разница цен
    - available_diff - показатель в процентах, если разница привышает его
                       данные не попадают в выборку (calculation_result).
    """
    available_diff = ELASTICSEARCH_AVAILABLE_DIFF
    calculation_result = []

    for pair in compare:
        try:
            first_price = float(pair[f'{longest_table}'].get('price', 1))
            second_price = float(pair[f'{shortest_table}'].get('price', 1))
        except Exception:
            continue

        if not first_price or not second_price:
            continue

        if first_price > second_price:

            relative_diff = abs(1.0 - (first_price / second_price)) * 100

            if relative_diff > available_diff:
                continue

            pair['relative_diff'] = relative_diff
            pair['abs_diff'] = first_price - second_price

            calculation_result.append(pair)

        elif first_price < second_price:

            relative_diff = abs(1.0 - (second_price / first_price)) * 100

            if relative_diff > available_diff:
                continue

            pair['relative_diff'] = relative_diff
            pair['abs_diff'] = second_price - first_price

            calculation_result.append(pair)

        else:
            pair['relative_diff'] = 0
            pair['abs_diff'] = 0

            calculation_result.append(pair)

    return calculation_result


# TODO: add vimos category
def result_formatting(
        data: list[dict],
        table: str, ) -> list[dict]:
    """
        - Формирования результата вычислений, для сохраненния данных в бд
        - При поиске имен в пары попадает самое близкое имя 
          и оно может повторяться, для этого, 
          в результате оставляем уникальные пары.
    """
    competitor = f'{table}'.split('_')[0]
    names = set()
    result = []
    # TODO: Add category
    for pair in data:
        formatted_pair = {
            'vimos_name': (
                pair['vimos_products'][
                    'name'].replace('"', '').replace("'", '')
            ),
            'vimos_price': pair['vimos_products']['price'],
            f'{competitor}_name': (
                pair[f'{table}'][
                    'name'].replace('"', '').replace("'", '')
            ),
            f'{competitor}_price': pair[f'{table}']['price'],
            'abs_diff': pair['abs_diff'],
            'relative_diff': pair['relative_diff'],
        }
        # TODO: проверить одинаковые имена в результате
        if pair['vimos_products']['name'] not in names:
            names.add(pair['vimos_products']['name'])
            result.append(formatted_pair)
    return result


def get_vimos_products() -> list[dict]:
    """Функция получения товаров vimos."""

    endpoint = f'{VIMOS_PRODUCTS_URL}?limit={VIMOS_PRODUCTS_LIMIT}'
    response = requests.get(endpoint).json()

    result = [product for product in response if product['price'] != '0.00']
    return [
        {
            'name': product['product_name'],
            'price': float(product['price']),
            'category': product['category_name'],
        }
        for product in result
    ]


def get_search_data(
        shortest_table: Table,
        shorter_data: list[dict], ) -> list[dict]:
    """
    Формирование данных для поиска, если vimos_data меньше чем у конкурента
    то используем ее для поиска.
    """
    if shortest_table != vimos_products:
        search_data = [
            {
                'id': product[0],
                'name': product[1],
                'price': product[2],
            }
            for product in shorter_data
        ]
        return search_data
    return shorter_data
