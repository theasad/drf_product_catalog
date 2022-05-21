from django.contrib import admin

from apps.product.models import Product, ProductImage

admin.site.register(Product)
admin.site.register(ProductImage)
