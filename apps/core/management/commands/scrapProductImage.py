from django.core.management import BaseCommand

from apps.product.utils import scrap_products


class Command(BaseCommand):
    help = 'Scrap product image from url'

    def handle(self, *args, **kwargs):
        scrap_products.run()
