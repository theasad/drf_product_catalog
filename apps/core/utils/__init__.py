from apps.product.models import ProductImage

from apps.product.utils import get_calculated_image_size


def build_absoulate_uri(request, location):
    """
    Build an absolute URI from `url`
    """
    return request.build_absolute_uri(location)


def generate_product_image_thumbnail(obj: ProductImage, filter_data=None) -> str:
    """
    Generate a thumbnail image
    """

    size = filter_data.get('size')
    if not size:
        # Return the original image
        return obj.image.url
    w, h = get_calculated_image_size(obj, size)

    return obj.create_thumbnail(width=w, height=h).url
