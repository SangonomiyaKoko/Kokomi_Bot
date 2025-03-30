import os
from PIL import ImageFont

from ..config import ASSETS_DIR


class FontManager:
    """管理字体加载和缓存，提供字体回退机制"""

    DEFAULT_FONT = ImageFont.load_default()  # 默认字体，防止字体加载失败

    def __init__(self):
        # 预定义字体路径
        self.font_paths = {
            1: os.path.join(ASSETS_DIR, "fonts", "SHSCN.ttf"),
            2: os.path.join(ASSETS_DIR, "fonts", "NZBZ.ttf"),
            # 如需要，在这里添加自己想要的字符
        }

        # 字体缓存，避免重复加载
        self.font_cache = {1: {}, 2: {}}

    def get_font(self, index: int, size: int) -> ImageFont.FreeTypeFont:
        """获取指定索引和大小的字体对象，如果加载失败，则返回默认字体。

        参数:
            index (int): 字体索引。
            size (int): 字体大小。

        返回:
            ImageFont.FreeTypeFont: 加载成功的字体对象，或使用默认字体。
        """
        if size not in self.font_cache[index]:
            try:
                self.font_cache[index][size] = ImageFont.truetype(self.font_paths[index], size)
            except (OSError, IOError):
                # 如果加载失败，使用默认字体并匹配 size
                self.font_cache[index][size] = ImageFont.truetype(self.DEFAULT_FONT, size)

        return self.font_cache[index][size]


# 全局字体管理器实例
font_manager = FontManager()
