import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_catalog.settings')

app = Celery('product_catalog')

CELERY_TIMEZONE = settings.TIME_ZONE

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Configure periodic tasks using crontab syntax
app.conf.beat_schedule = {
    'scrap-product-images': {
        'task': 'apps.core.tasks.scrap_product_images',
        'schedule': crontab(minute='*/1'),
    }
}
