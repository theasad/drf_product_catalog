from typing import Tuple


class ImageSizes(object):
    """
    Image sizes
    """
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'

    CHOICES = (
        (SMALL, 'Small'),
        (MEDIUM, 'Medium'),
        (LARGE, 'Large'),
    )

    # This is a dict of the sizes that are allowed for the image field to create thumbnails.
    # The key is the name of the size, and the value is a tuple of the width and height.
    VERSATILEIMAGEFIELD_SIZES = {
        SMALL: (256,),
        MEDIUM: (1024,),
        LARGE: (2048,),
    }

    @classmethod
    def get_size_by_key(cls, size_key: str) -> Tuple[int, int]:
        """
        Get the size from the name
        """
        return cls.VERSATILEIMAGEFIELD_SIZES[size_key]

    get_all_size_keys = classmethod(
        lambda cls: list(cls.VERSATILEIMAGEFIELD_SIZES.keys()))
