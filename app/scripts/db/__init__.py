from .local_data import UserLocalDB
from .image_data import ImageDB
UserLocalManager = UserLocalDB()
ImageManager = ImageDB()

__all__ = [
    'UserLocalManager',
    'ImageManager'
]