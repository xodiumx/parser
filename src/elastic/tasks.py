from crawls.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from core.celery import celery_app
from core.db_utils import create_db_objects, get_todays_data
from db.connect import get_session
from db.tables import (petrovich_products, saturn_products,
                       stroyudacha_products, vimos_products)
from db.tables_analytics import (petrovich_analytics, saturn_analytics,
                                 stroyudacha_analytics)
from reports.tasks import send_reports

from .services import (calculate_diffs_of_prices, find_same_products,
                       get_search_data, get_vimos_products, result_formatting)

ANALYTICS_TABLES = {
    'petrovich': petrovich_analytics,
    'stroyudacha': stroyudacha_analytics,
    'saturn': saturn_analytics,
}


@celery_app.task
def delete_indices_in_elastic_search() -> None:
    """
    Функиця отчистки индексов в elasticsearch
    - Каждый день индексы создаются по новой и заполняются новыми данными.
    """
    es_connection = Elasticsearch([
        {
        'host': ELASTICSEARCH_HOST, 
        'port': ELASTICSEARCH_PORT, 
        'scheme': 'http'
        }
    ])
    indices = (
        'vimos_products', 
        'petrovich_products', 
        'stroyudacha_products', 
        'saturn_products',
    )
    for ind in indices:
        try:
            es_connection.indices.delete(index=ind)
            print(f'Индекс {ind} успешно удален.')
        except Exception as e:
            print(f'Ошибка при удалении индекса {ind}: {e}')

    # create_indices_in_elasticsearch.delay()
    return 'Индексы успешно удалены.'


@celery_app.task
def create_indices_in_elasticsearch() -> str:
    """Создание индексов в elasticsearch."""
    
    es_connection = Elasticsearch([
        {
        'host': ELASTICSEARCH_HOST, 
        'port': ELASTICSEARCH_PORT, 
        'scheme': 'http'
        }
    ])
    index_names = (
        f'{petrovich_products}', f'{saturn_products}', 
        f'{stroyudacha_products}', f'{vimos_products}'
    )
    index_settings = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 1
        },
        'mappings': {
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'text'},
                'price': {'type': 'float'},
                'currency': {'type': 'text'},
                'gcode': {'type': 'text'},
                'url': {'type': 'text'},
                'category': {'type': 'text'},
            }
        }
    }
    for name in index_names:
        es_connection.indices.create(index=name, body=index_settings)

    # create_documents_in_indices.delay()
    return 'Индексы успешно созданы.'


@celery_app.task
def create_documents_in_indices() -> str:
    """В индексах создаются документами с данными взятыми из db."""

    vimos_data = get_vimos_products()
    tables = (
        petrovich_products, stroyudacha_products, saturn_products,
    )
    db_session = next(get_session())
    es_connection = Elasticsearch([
        {
        'host': ELASTICSEARCH_HOST, 
        'port': ELASTICSEARCH_PORT, 
        'scheme': 'http'
        }
    ])

    # TODO: change int to constant
    for table in tables:
        data = get_todays_data(table, db_session)
        data = [
            {
                'id': product[0],
                'name': product[1],
                'price': product[3],
            }
            for product in data
        ]
        bulk(es_connection, data, index=f'{table}')
    bulk(es_connection, vimos_data, index=f'{vimos_products}')

    # search_same_products.delay()
    return 'Документы в индексах elasticsearch созданы.'


@celery_app.task
def search_same_products() -> str:
    """
    - Функция сопостовления имен у vimos и конкурентов
    - Определяется более длинный и короткий список товаров
    - Поиск идет по короткому
    - Формируется data для поиска
    - find_same_products - осуществляется не точный поиск продуктов по name
    - calculate_diffs_of_prices - вычисляются показатели разности цен
    - result_formatting - формируется список объектов для сохранения в бд
    - create_db_objects - создаются объекты, таблица берется из const ANALYTICS
    """
    db_session = next(get_session())
    vimos_data = get_vimos_products()
    competitors = (petrovich_products, stroyudacha_products, saturn_products)

    for table in competitors:
        
        longest_table = table
        shortest_table = vimos_products

        shorter_data = vimos_data
        competitor_data = get_todays_data(table, db_session)

        if len(vimos_data) > len(competitor_data):
            shorter_data = competitor_data
            # TODO: change vimos_products on flag
            longest_table = vimos_products
            shortest_table = table

        search_data = get_search_data(shortest_table, shorter_data)

        search_result = find_same_products(
            longest_table, shortest_table, search_data
        )
        diffs = calculate_diffs_of_prices(
            longest_table, shortest_table, search_result)
        product_list = result_formatting(diffs, table)

        competitor= f'{table}'.split('_')[0]
        create_db_objects(
            ANALYTICS_TABLES[competitor], product_list, db_session
        )
    # send_reports.delay()
    return 'Формирование аналитических таблиц завершено.'
