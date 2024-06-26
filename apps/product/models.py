from django.db import models
from versatileimagefield.fields import VersatileImageField

from apps.core.models import TimeStamp


class Product(TimeStamp):
    """ Product model. This model is used to store the products. """
    scrap_url = models.URLField(max_length=300, unique=True, db_index=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'products'

    def __str__(self):
        return self.scrap_url

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, scrap_url=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.scrap_url)


class ProductImage(TimeStamp):
    """ ProductImage model. This model is used to store the images of the products. """

    def get_image_upload_path(self, filename):
        """ This function is used to get the path of the image. """
        return f'catalog/product/{self.product.id}/{filename}'

    # This field will be used to save the original URL of this image
    scrap_url = models.URLField(max_length=300)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images')
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    image = VersatileImageField(
        upload_to=get_image_upload_path,
        width_field='width',
        height_field='height'
    )
    position = models.PositiveIntegerField(
        'Position',
        default=1,
    )

    class Meta:
        ordering = ('position',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        unique_together = ('product', 'scrap_url')
        db_table = 'product_images'

    def __str__(self):
        return self.image.name

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, image=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.image)

    def create_thumbnail(self, width, height):
        """ This function is used to create the thumbnail of the image. """
        return self.image.thumbnail[f'{width}x{height}']
