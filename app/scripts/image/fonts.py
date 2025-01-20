import os

from PIL import ImageFont

from ..config import ASSETS_DIR

class FontManager:
    def __init__(self):
        self.font_path = {
            1: os.path.join(ASSETS_DIR, 'fonts', 'SHSCN.ttf'),
            2: os.path.join(ASSETS_DIR, 'fonts', 'NZBZ.ttf')
        }
        self.font_cache = {
            1: {},
            2: {}
        }

    def get_font(self, index: int, size: int) -> ImageFont.FreeTypeFont:
        if size not in self.font_cache[index]:
            self.font_cache[index][size] = ImageFont.truetype(self.font_path[index], size)
        return self.font_cache[index][size]

font_manager = FontManager()