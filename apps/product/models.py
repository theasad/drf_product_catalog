from versatileimagefield.fields import VersatileImageField
from apps.core.models import TimeStamp
from django.db import models


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

    def get_image_upload_path(instance, filename):
        """ This function is used to get the path of the image. """
        return 'images/%s/%s' % (instance.product.id, filename)

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

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        db_table = 'product_images'

    def __str__(self):
        return self.image.name

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, image=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.image)
