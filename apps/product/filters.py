from django_filters import rest_framework as filters

from apps.product import ImageSizes
from apps.product.models import ProductImage


class ImageFilter(filters.FilterSet):
    product_url = filters.CharFilter(
        field_name='product__scrap_url', label='Scrap URL')
    size = filters.ChoiceFilter(
        choices=ImageSizes.CHOICES, method='filter_size', label="Size")

    class Meta:
        model = ProductImage
        fields = []

    def filter_size(self, queryset, name, value):
        # not needed to filter queryset based on this size value
        return queryset
