# Analytics for vimos

## Доступные функции

Процесс парсинга:
  - Ежедневно в 7 утра запускаются парсеры товаров petrovich, saturn, stroyudacha
  - После парсинга в базу данных перезаписываются товары vimos
  - Затем для сопоставления наименований, обновляются товары в `elasticsearch`
  - Товары у которых score в сравнении больше 20 попадают в аналитическую выборку
  - Дальше происходит вычисление абсолютной и относительной разницы цен этих товаров
  - Потом формируются аналитические таблицы
  - Эти таблицы форматируются в `xlsx` формат и отправляются в виде отчетов на указанную почту

Вывод в superset:
  - Есть возможность приконектить базу данных к аналитической платформе `Apache Superset`
  - В ней есть функционал создания `dataset`-a
  - А также построения `chart`-ов, `dashboard`-ов для аналитики данных.

## TODO List
  - Доработка парсеров leroy и obi
  - Масштабирование парсеров на различные магазины
  - Настройка `selenium` в `docker`
  - Построение аналитических `dashboard`-ов
  - Настройка `CI/CD`

## Развернуть superset через docker

1. Перейдите в директорию
```
cd parser
```
2. Склонируйте репозиторий
```
git clone https://github.com/apache/superset.git
```
3. Перейдите в директорию
```
cd superset
```
4. В начале файла `docker-compose-non-dev.yml` изменить строку на:
```
x-superset-image: &superset-image apache/superset:2.1.0
```
5. В файле `docker-compose-non-dev.yml` необходимо проставить для каждого контейнера
```
networks:
  - own_network
```
5. У контейнера `superset` необходимо добавить в `networks`
```
- parser_network
```
6. В конце файла `docker-compose-non-dev.yml` добавить
```
networks:
  parser_network:
  own_network:
```
7. В директории `superset/docker/pythonpath_dev` в файле `superset_config.py` добавить
```
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "ru": {"flag": "ru", "name": "Russian"},
}
```
8. Выполните команды
```
docker-compose -f docker-compose-non-dev.yml pull
docker-compose -f docker-compose-non-dev.yml up
```

## Развернуть проект через docker
9. Склонируйте репозиторий
```
git clone git@github.com:xodiumx/parser.git
```
10. Перейдите в директорию 
```
cd src
```
11. Создайте `.env` file
```
DB_NAME=parser
DB_HOST=db_parser
# DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=admin

API_KEY_SCRAPEOPS=40arfsdfdsfds-c23458c-46dsae3-96ddsae-9dsac

POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin

CELERY_BROKER=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

FLOWER_USER=admin
FLOWER_PASSWORD=admin

ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200

SMTP_HOST=smtp.mail.ru
SMTP_PORT=465
SMTP_USERNAME=<your@mail.com>
SMTP_PASSWORD=<password>
SENDER_EMAIL=<your@mail.com>
RECEIVER_EMAIL=<your@mail.com>

VIMOS_PRODUCTS_URL=<api_for_get_products>
VIMOS_PRODUCTS_PAGES=<pagiantion>
VIMOS_PRODUCTS_LIMIT=<limit>
```
12. Создайте `TxtProxy.txt` file
```
Ваши proxy в формате:
<name:password@ip:port>
```
13. Скачайте chromedriver и поместите в текущую директорию
```
https://chromedriver.chromium.org/downloads
```
14. В директории `parser/docker/postgres` создайте `.env` file
```
DB_NAME=parser
```
15. Выполните команду:
```
docker-compose -f docker-compose-dev.yml up -d --build
```

## Пример работы и доустпные эндпоинты
