import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


BOT_NAME = 'parser'

SPIDER_MODULES = ['parser.spiders']
NEWSPIDER_MODULE = "parser.spiders"


# FAKEUSERAGENT_PROVIDERS = [
#     'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
#     'scrapy_fake_useragent.providers.FakerProvider',  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
#     'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Fall back to USER_AGENT value
# ]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"

# TODO: For saturn False
# Obey robots.txt rules 
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
   "Accept-Language": "en",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "parser.middlewares.ParserSpiderMiddleware": 543,
    # Splash
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "parser.middlewares.ParserDownloaderMiddleware": 543,

    # Fake user agents
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    #'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    
    # Proxies
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,

    # Spash for dynamically loading content
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "parser.pipelines.StroyudachaParserPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = 'utf-8'


# Database connection

DATABASE = {
   'DB_HOST':  os.getenv('DB_HOST'),
   'DB_PORT':  os.getenv('DB_PORT'),
   'DB_NAME':  os.getenv('DB_NAME'),
   'DB_USER':  os.getenv('DB_USER'),
   'DB_PASS':  os.getenv('DB_PASS'),
}

# PROXIES LIST

# ROTATING_PROXY_LIST = [
#     '',
#     '',
#     '',
#     '',
#     '',
# ]
PROXY_FILE_NAME = 'TxtProxy.txt'
ROTATING_PROXY_LIST_PATH = f'{PROXY_FILE_NAME}'

# SCRAPEOPS API 

API_KEY_SCRAPEOPS = os.getenv('API_KEY_SCRAPEOPS')
USER_AGENTS_ENDPOINT = 'http://headers.scrapeops.io/v1/user-agents?api_key='


# CONSTANTS

STROY_UDACHA_CONST = {
    'site': 'stroyudacha',
    'xpath_category': '//li[contains(@class, "level1")]/a/@href',
    'xpath_sub_category': '//a[@class="group_item"]/@href',
    'xpath_sub_sub_category': '//a[@class="group_item"]/@href',
    'xpath_pagination': '//div[@class="products_count"]/span/text()',
    'xpath_name': '//div[@class="name"]/a/text()',
    'xpath_category_name': '//h1/text()',
    'xpath_measurement': '//div[@class="product_count"]/div/text()',
    'xpath_cart_price': '',
    'xpath_price': '//div[@class="price_container"]//span[@class="price_number"]/text()',
    'xpath_url': '//div[@class="name"]/a/@href',
    'xpath_gcode': '//div[@class="site_code"]/a/span/text()',
    'page_items_amount': 16,
}

PETROVICH_CONST = {
    'site': 'petrovich',
    'data_list': '//div[@class="product-list"]/div/div',
    'xpath_category': '//p[contains(@class, "section-catalog-list-item")]/a/@href',
    'xpath_sub_category': '',
    'xpath_sub_sub_category': '',
    'xpath_pagination': '//p[contains(@data-test, "products-counter")]/text()',
    'xpath_name': './/span[contains(@data-test, "product-title")]/text()',
    'xpath_category_name': '//h1[@class="categories-title"]/text()',
    'xpath_measurement': './/div[@class="card-catalog-wide-price-block"]/div[1]/div[1]/p/text()',
    'xpath_cart_price': './/p[contains(@data-test, "product-gold-price")]/text()',
    'xpath_price': './/p[contains(@data-test, "product-retail-price")]/text()',
    'xpath_url': './/div[@class="card-catalog-wide-body"]/div[1]/a/@href',
    'xpath_gcode': './/p[@data-test="product-code"]/text()',
    'page_items_amount': 20,
}

SATURN_CONST = {
    'site': 'saturn',
    'xpath_data_list': '//ul[@class="catalog_Level2__goods_list"]/li',
    'xpath_category': '//div[@class="front_catalog_item"]/a/@href',
    'xpath_category_name': '//div[@class="catalog__breadcrumb__title"]/text()',
    'xpath_sub_category': '',
    'xpath_sub_sub_category': '',
    'xpath_pagination': '//li[@class="pagination__item"][3]/a/text()',
    'xpath_next_page': '//li[@class="pagination__item"][last()]',
    'xpath_name': './/div[@class="goods_card_text  goods_card_text--fl"]/a/text()',
    'xpath_price': './/div[@class="goods_card_price_value "]/span/text()',
    'xpath_cart_price': './/div[@class="goods_card_price_discount_value"]/span/text()',
    'xpath_measurement': './/div[@class="goods_card_price_units"]/span/text()',
    'xpath_url': './/div[@class="goods_card_icon_wrap"]/a/@href',
    'page_items_amount': 20,
}

LEROY_CONST = {
    'site': 'leroy',
    'xpath_data_list': '//div[@data-qa-product]',
    'xpath_category': '//a[@data-qa="subtitle"]',
    'xpath_category_name': '//h1',
    'xpath_sub_category': '',
    'xpath_sub_sub_category': '',
    'xpath_pagination': '//div[@data-qa-pagination]/div[2]/a/span',
    'xpath_next_page': '//a[@data-qa-pagination-item="right"]',
    'xpath_name': './/a[@data-qa="product-name"]/span/span',
    'xpath_price': './/div[@data-qa="product-primary-price"]/span[1]',
    'xpath_best_price': './/div[@data-qa="product-best-price"]/div[2]/div/span[1]',
    'xpath_cart_price': '',
    'xpath_measurement': './/div[@data-qa="product-primary-price"]/span[3]',
    'xpath_best_easurement': './/div[@data-qa="product-best-price"]/div[2]/div/span[2]',
    'xpath_url': './/a',
    'page_items_amount': 25,
}

OBI_CONST = {
    'site': 'obi',
    'xpath_catalog_button': '//div[@id="__next"]/header/div[2]/nav/button',
    'xpath_data_list': '//a[starts-with(@href, "/products")]',
    'xpath_category': '//div[@id="__next"]/header/div[3]/div/div/ul/li',
    'xpath_category_name': '',
    'xpath_sub_category': '//div[@id="__next"]/header/div[3]/div/div/div[3]/ul/li/a',
    'xpath_sub_sub_category': '//section[@aria-label="Category page"]/div/div[2]/div/div/a',
    'xpath_pagination': '',
    'xpath_next_page': '',
    'xpath_name': '',
    'xpath_price': '',
    'xpath_best_price': '',
    'xpath_cart_price': '',
    'xpath_measurement': '',
    'xpath_best_easurement': '',
    'xpath_url': '',
    'page_items_amount': 25,
    'count_categories': 6,
}

# Celery

CELERY_BROKER=os.getenv('CELERY_BROKER')
CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND')
CELERYD_MAX_TASKS_PER_CHILD = 1

# LOGS

LOG_LEVEL = 'ERROR'

# Customize settings for difs spiders
CUSTOM_SETTINGS = {
    'PetrovichSpiderSPB': {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,
    },
    'StroydachaSpiderSPB': {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,
    },
    'SaturnSpiderSPB': {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,
    }
}


# Elasticsearch settings
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT')

ELASTICSEARCH_SEARCH_SCORE = 20 # INT
ELASTICSEARCH_AVAILABLE_DIFF = 1000 # PERCENT

# SMPT settings

SMTP_SETTINGS = {
    'smtp_host': os.getenv('SMTP_HOST'),
    'smtp_port': os.getenv('SMTP_PORT'),
    'smtp_username': os.getenv('SMTP_USERNAME'),
    'smtp_password': os.getenv('SMTP_PASSWORD'),
    'sender_email': os.getenv('SENDER_EMAIL'),
    'receiver_email': os.getenv('RECEIVER_EMAIL'),
}

# API VIMOS

VIMOS_PRODUCTS_URL = os.getenv('VIMOS_PRODUCTS_URL')
VIMOS_PRODUCTS_PAGES = os.getenv('VIMOS_PRODUCTS_PAGES')
VIMOS_PRODUCTS_LIMIT = os.getenv('VIMOS_PRODUCTS_LIMIT')