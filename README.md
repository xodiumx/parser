# Analytics for vimos

## Доступные функции

Процесс парсинга:
  - Ежедневно в 7 утра запускаются парсеры товаров petrovich, saturn, stroyudacha
  - После парсинга в базу данных перезаписываются товары vimos
  - Затем для сопоставления наименований, обновляются товары в `elasticsearch`
  - Товары у которых score в сравнении больше 20 попадают в аналитическую выборку
  - Дальше происходит вычисление абсолютной и относительной разницы цен этих товаров
  - Потом формируются аналитические таблицы
  - Эти таблицы форматируются в `xlsx` и отправляются в виде отчетов на указанную почту
  - Примеры отчетов находятся в директории `reports/examples`

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
  - Настройка `Airflow` - sensors and clearing

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
# DB_HOST=db_parser
# DB_HOST=localhost
DB_HOST=postgresql
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

## Запуск Airflow

16. Создайте `.env` file в директории `airflow`
```
cd airflow
```
```
AIRFLOW_DB_NAME=airflow
DB_NAME_TWO=parser

POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

AIRFLOW_FERNET_KEY='46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho='
AIRFLOW_SECRET_KEY='a25mQ1FHTUh3MnFRSk5KMEIyVVU2YmN0VGRyYTVXY08='
AIRFLOW_EXECUTOR=CeleryExecutor

AIRFLOW_DATABASE_NAME=airflow
AIRFLOW_DATABASE_USERNAME=postgres
AIRFLOW_DATABASE_PASSWORD=admin

AIRFLOW_USERNAME=admin
AIRFLOW_PASSWORD=admin
AIRFLOW_LOAD_EXAMPLES=no
AIRFLOW_EMAIL=admin@example.com

AIRFLOW_WEBSERVER_HOST=airflow
AIRFLOW_WEBSERVER_PORT=8080
```
17. Выполните команду:
```
docker-compose up -d
```
## Пример работы и доустпные эндпоинты

`DAG-и` находятся в директории `src/dags`

Проект работает в двух версиях:
 1. Таски запускаются цепочкой используя `celery` + `redis`
 2. Таски запускаются в `Airflow`

В `airflow` настроен один `DAG` в котором выполняются задачи:
<img width="1492" alt="dag" src="https://github.com/xodiumx/parser/assets/111197771/75e63f2c-5141-42fb-aaaa-357d77fd02a9">

- Изначально база заполняется данными за текущий день
- Затем происходит отчистка данных в базе elasticsearch для обновления данных
- Далее создаются индексы `elasticsearch`
- В этих индексах создаются документы, которые содержат информацию о товарах за текущий день
- Потом наименования товаров vimos сравниваются с наименованиями товаров конкурентов
- Далее на полученных сравнениях формируются аналитические таблицы, с вычислениями показателей отклонений цены товаров
- И в конце данные таблицы форматируются в `xlsx` формат и отправляются на почту в виде отчетов

Ниже представлена конечная схема `ETL` - процесса в виде `DAG`
<img width="1509" alt="dag_tasks" src="https://github.com/xodiumx/parser/assets/111197771/1a24fdd8-149a-4f09-bdd6-21c2da9f2d73">

#### `Airflow` доступен по `endpoint-у` - `localhost:8080`
#### `pgAdmin` доступен по `endpoint-у` - `localhost:5050`
