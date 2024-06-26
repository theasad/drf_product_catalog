from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.product.filters import ImageFilter, ImageSizeFilter
from apps.product.models import ProductImage
from apps.product.serializers import ImageSerializer


class ImageListView(ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    filter_class = ImageFilter

    def get_queryset(self):
        if product_url := self.request.GET.get('product_url'):
            return super().get_queryset()
        return super().get_queryset().none()


class ImageDetailView(RetrieveAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
