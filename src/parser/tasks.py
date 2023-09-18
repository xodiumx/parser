from parser.settings import VIMOS_PRODUCTS_URL, VIMOS_PRODUCTS_LIMIT

import requests
from multiprocessing import Process

from parser.spiders.petrovich import PetrovichSpiderSPB
from parser.spiders.stroydacha import StroydachaSpiderSPB
from parser.spiders.saturn import SaturnSpiderSPB
# from parser.spiders.leroy import LeroySpiderSpbFirst
from parser.settings import CUSTOM_SETTINGS

from core.db_utils import create_db_objects
from db.connect import get_session
from db.tables import vimos_products
from core.celery import celery_app
from scrapy import Spider, signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from elastic.tasks import delete_indices_in_elastic_search


def run_scrapy_spiders(spider: Spider) -> None:
    """Cоздание и запуск Crawler-a."""
    name = spider()
    crawler = Crawler(spider, settings={
        **get_project_settings(), 
        **CUSTOM_SETTINGS[str(name)]
    })
    # crawler.settings = CUSTOM_SETTINGS[str(name)]
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.crawl()
    reactor.run()


@celery_app.task
def run_scraper_task() -> None:
    """Запуск всех spider-ов в нескольких процессах."""
    petrovich = Process(target=run_scrapy_spiders, args=(PetrovichSpiderSPB,))
    stroy_ud = Process(target=run_scrapy_spiders, args=(StroydachaSpiderSPB,))
    saturn = Process(target=run_scrapy_spiders, args=(SaturnSpiderSPB,))
    # leroy = Process(target=run_scrapy_spiders, args=(LeroySpiderSpbFirst,))
    
    petrovich.start()
    stroy_ud.start()
    saturn.start()
    # leroy.start()

    petrovich.join()
    stroy_ud.join()
    saturn.join()
    # leroy.join()

    add_vimos_products_in_db.delay()


@celery_app.task
def add_vimos_products_in_db() -> str:

    db_session = next(get_session())
    
    endpoint = f'{VIMOS_PRODUCTS_URL}?limit={VIMOS_PRODUCTS_LIMIT}'
    response = requests.get(endpoint).json()

    vimos_data = [
        product for product in response if product['price'] != '0.00'
    ]
    vimos_data = [
        {
            'name': product['product_name'],
            'gcode': product['gcode'],
            'price': float(product['price']),
            'currency': 'Руб.',
            'category': product['category_name'],
            'measurement': product['units'],
        }
        for product in vimos_data
    ]
    try:
        create_db_objects(vimos_products, vimos_data, db_session)

        delete_indices_in_elastic_search.delay()
        return 'Данные в таблице vimos_products успешно созданы'
    
    except Exception as err:

        delete_indices_in_elastic_search.delay()
        return f'Ошибка при заполнении таблицы vimos_products {err}'
