from rest_framework import serializers

from apps.core.utils import build_absoulate_uri, generate_product_image_thumbnail
from apps.product.models import ProductImage


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'position', 'created_at')

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = generate_product_image_thumbnail(obj, request.GET)
        return build_absoulate_uri(request, image_url)
