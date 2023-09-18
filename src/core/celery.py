from __future__ import absolute_import

from parser.settings import (CELERY_BROKER, CELERY_RESULT_BACKEND,
                             CELERYD_MAX_TASKS_PER_CHILD)

from celery import Celery
from celery.schedules import crontab

packages = ('parser', 'elastic', 'reports',)

celery_app = Celery('vimos_parser')
celery_app.conf.broker_url = CELERY_BROKER
celery_app.conf.result_backend = CELERY_RESULT_BACKEND
celery_app.conf.worker_max_tasks_per_child = CELERYD_MAX_TASKS_PER_CHILD

celery_app.autodiscover_tasks(packages=packages, force=True)


celery_app.conf.beat_schedule = {
    'parsing': {
        'task': 'parser.tasks.run_scraper_task',
        # 'schedule': crontab(minute=0, hour=4),
        'schedule': crontab(minute='*/1'),
    },
    # 'vimos_products': {
    #     'task': 'parser.tasks.add_vimos_products_in_db',
    #     'schedule': crontab(minute=0, hour=4),
    #     # 'schedule': crontab(minute='*/1'),
    # },
    # 'delete_elastic_indices': {
    #     'task': 'elastic.tasks.delete_indices_in_elastic_search',
    #     'schedule': crontab(minute=39, hour=12),
    #     # 'schedule': crontab(minute='*/1'),
    # },
    # 'create_elastic_indices': {
    #     'task': 'elastic.tasks.create_indices_in_elsatic_search',
    #     'schedule': crontab(minute=54, hour=11),
    #     # 'schedule': crontab(minute='*/1'),
    # },
    # 'create_elastic_documents': {
    #     'task': 'elastic.tasks.create_documents_in_indices',
    #     'schedule': crontab(minute=55, hour=11),
    #     # 'schedule': crontab(minute='*/1'),
    # },
    # 'elastic_search_products': {
    #     'task': 'elastic.tasks.search_same_products',
    #     'schedule': crontab(minute=56, hour=11),
    #     # 'schedule': crontab(minute='*/1'),
    # },
    # 'email_reports': {
    #     'task': 'reports.tasks.send_reports',
    #     'schedule': crontab(minute=59, hour=11),
    #     # 'schedule': crontab(minute='*/1'),
    # },
}

celery_app.conf.timezone = 'UTC'
