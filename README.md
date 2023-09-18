# Vimos-Python

## Развернуть superset через docker

1. Перейдите в директорию
```
cd Vimos-Python
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
git clone gitlab@gitlab.grokhotov.ru:positron-it/vimos-python.git
```
10. Перейдите в директорию 
```
cd parser
```
11. Создайте `.env` file
```
DB_NAME=parser
DB_HOST=db_parser
DB_PORT=5432
DB_USER=postgres
DB_PASS=admin

API_KEY_SCRAPEOPS=40a6733242c0-c5dsac-46e3-96de-346753277e0edbc

POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin

CELERY_BROKER=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

FLOWER_USER=admin
FLOWER_PASSWORD=admin
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
docker-compose up -d
```

## Roadmap
 - Доработка парсеров saturn, leroy, obi
 - Расчет показателей после парсинга
 - Отправка информации о изменении цены на почту
 - Запуск парсеров в 7:00
 - Настройка superset 
 - Другие.

## Authors and acknowledgment - [Team Positron](https://www.positron-it.ru/)
