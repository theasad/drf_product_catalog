from django_filters import rest_framework as filters

from apps.product import ImageSizes
from apps.product.models import ProductImage


class ImageSizeFilter(filters.FilterSet):
    size = filters.ChoiceFilter(
        choices=ImageSizes.CHOICES, method='filter_size', label="Size")

    def filter_size(self, queryset, name, value):
        # not needed to filter queryset based on this size value
        return queryset

    class Meta:
        model = ProductImage
        fields = []


class ImageFilter(ImageSizeFilter):
    product_url = filters.CharFilter(
        field_name='product__scrap_url', label='Product URL')

    class Meta:
        model = ProductImage
        fields = []
