from .local_data import LocalDB
from .image_data import ImageDB
ImageManager = ImageDB()

__all__ = [
    'LocalDB',
    'ImageManager'
]