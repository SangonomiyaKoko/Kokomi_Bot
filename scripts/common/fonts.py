from PIL import ImageFont

class FontManager:
    def __init__(self, font_path: str):
        self.font_path = font_path
        self.font_cache = {}

    def get_font(self, size: int) -> ImageFont.FreeTypeFont:
        if size not in self.font_cache:
            self.font_cache[size] = ImageFont.truetype(self.font_path, size)
        return self.font_cache[size]