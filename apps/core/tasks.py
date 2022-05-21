from celery import shared_task

from apps.product.utils import scrap_products


@shared_task
def scrap_product_images():
    scrap_products.run()
