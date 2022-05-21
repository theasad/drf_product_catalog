
import logging
from typing import List, Tuple

from apps.product import ImageSizes
from apps.product.models import ProductImage

logger = logging.getLogger(__name__)


def get_calculated_image_size(image: ProductImage, size_key) -> Tuple[int, int]:
    """
    Calculate the image size and return it as a tuple
    """
    max_width, max_height = image.width, image.height
    width,  = ImageSizes.get_size_by_key(size_key)

    if width > max_width:
        width = max_width

    # Calculate the height based on the width and the aspect ratio

    wpercent = (width/float(max_width))
    height = int((float(max_height)*float(wpercent)))

    return (width, height)


# @shared_task
def create_thumbnails(image_id: int) -> List:
    """
    Create a set of thumbnail for the image
    """
    for size_key in ImageSizes.get_all_size_keys():
        image = ProductImage.objects.get(id=image_id)
        logger.info(
            f'Creating thumbnail for image {image_id} at size {size_key}')
        width, height = get_calculated_image_size(image, size_key)
        image.create_thumbnail(width, height)
