import os
import time
import numpy as np
from contextlib import ContextDecorator
from typing import List, Union, Tuple, Literal

from PIL import Image, ImageFont, ImageDraw

from ..config import OUTPUT_DIR, bot_settings
from ..schemas import JSONResponse
from .fonts import font_manager

    
class TextOperation:
    """封装写入文字的操作，支持指定字体、大小、颜色和优先级"""
    
    def __init__(
        self, 
        text: str, 
        position: Tuple[int, int], 
        font_index: int, 
        font_size: int, 
        color: Tuple[int, int, int], 
        align: Literal["left", "center", "right"] = "left",
        priority: int = 10
    ):
        """
        文字绘制操作

        参数:
            text (str): 要绘制的文字内容
            position (Tuple[int, int]): 文字的基准位置 (x, y)，其含义取决于对齐模式：
                - "left"（默认）: x 为文字的左边界
                - "center": x 为文字的中心
                - "right": x 为文字的右边界
            font_index (int): 字体索引，用于选择不同字体
            font_size (int): 字体大小
            color (Tuple[int, int, int]): 文字颜色 (R, G, B)
            align (Literal["left", "center", "right"], optional): 文字对齐方式，默认 "left"
            priority (int, optional): 操作优先级，数值越小优先级越高。默认 10
        """
        self.text = text
        self.position = position
        self.font_index = font_index
        self.font_size = font_size
        self.color = color
        self.priority = priority
        self.align = align  # 文字对齐方式

class RectangleOperation:
    """封装绘制矩形的操作，支持圆角矩形"""
    
    def __init__(self, position: tuple, size: tuple, color: tuple, corner_radius: int = 0, priority: int = 10):
        """
        初始化矩形操作
        
        参数:
            position (tuple): 矩形的位置 (x, y)
            size (tuple): 矩形的尺寸 (宽, 高)
            color (tuple): 矩形的填充颜色 (R, G, B)
            corner_radius (int, optional): 圆角半径，默认值为 0，即不绘制圆角
            priority (int, optional): 操作的优先级，数字越小优先级越高。默认值为 10
        """
        self.position = position
        self.size = size
        self.color = color
        self.corner_radius = corner_radius
        self.priority = priority

class ImageHandler:
    """封装 Pillow 的常用图片操作方法，包括创建、打开、调整大小和保存图片等"""

    @staticmethod
    def new_image(
        size: Tuple[int, int], 
        color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    ) -> Image.Image:
        """创建新的空白图片，支持 RGB 或 RGBA 模式。

        参数:
            size (Tuple[int, int]): 图片尺寸 (宽, 高)。
            color (Tuple[int, int, int, int]): 背景颜色 (R, G, B) 或 (R, G, B, A)，默认为白色不透明。

        返回:
            Image.Image: 创建的图片对象。
        """
        mode = "RGBA" if len(color) == 4 else "RGB"
        return Image.new(mode, size, color)


    @staticmethod
    def open_image(path: str) -> Image.Image:
        """打开图片文件，如果文件不存在，则返回占位图片。

        参数:
            path (str): 图片文件路径。

        返回:
            Image.Image: 加载的图片对象，如果文件不存在则返回占位图片。
        """
        try:
            return Image.open(path)
        except (FileNotFoundError, OSError):
            return JSONResponse.API_10008_ImageResourceMissing

    @staticmethod
    def resize_image(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """调整图片大小。

        参数:
            img (Image.Image): 需要调整的图片对象。
            size (Tuple[int, int]): 目标尺寸 (宽, 高)。

        返回:
            Image.Image: 调整大小后的图片对象。
        """
        return img.resize(size)
    
    @staticmethod
    def save_image(img: Image.Image) -> dict:
        """保存图片到指定目录，并返回保存的文件路径。

        参数:
            img (Image.Image): 要保存的图片对象。

        返回:
            dict: 包含状态信息和图片路径的字典。
        """
        try:
            file_name = os.path.join(OUTPUT_DIR, f"{int(time.time() * 1000)}." + bot_settings.RETURN_PIC_TYPE)
            img.save(file_name)
            return {
                'status': 'ok',
                'code': 1000,
                'message': 'Success',
                'data': {
                    'img': file_name
                }
            }
        except Image.DecompressionBombError:
            return JSONResponse.API_10009_ImageTooLarge  # 返回图片过大错误
        except Exception:
            return JSONResponse.API_10007_SaveImageFailed  # 其他异常返回通用保存失败错误
        finally:
            img.close()

    @staticmethod
    def composite_paste(
        bg: Image.Image, 
        fg: Image.Image, 
        position: tuple = (0, 0)
    ) -> Image.Image:
        """使用 paste 方法叠加图片（适用于不带透明通道的图片）。

        不带有alpha通道图片叠加，如有会丢失alpha通道的信息
        
        参数:
            bg (Image.Image): 背景图片
            fg (Image.Image): 需要叠加的前景图片
            position (tuple): 叠加的位置，默认为 (0, 0)

        返回:
            Image.Image: 叠加后的图片。
        """
        # 叠加图片
        bg.paste(fg, position)
        return bg

    @staticmethod
    def composite_alpha(
        bg: Image.Image, 
        fg: Image.Image, 
        position: tuple = (0, 0)
    ) -> Image.Image:
        """使用 alpha_composite 方法叠加两张图片（适用于带透明通道的图片）
        
        参数:
            bg (Image.Image): 背景图片
            fg (Image.Image): 需要叠加的前景图片
            position (tuple): 前景图片放置的位置，默认为 (0, 0)

        返回:
            Image.Image: 叠加后的图片
        """
        if fg.mode != 'RGBA':
            # 检查顶图是否有 alpha 通道
            fg.convert("RGBA")
        # 叠加图片
        bg.alpha_composite(fg, position)
        return bg

    @staticmethod
    def composite_numpy(
        bg: Image.Image, 
        fg: Image.Image, 
        position: tuple = (0, 0)
    ) -> Image.Image:
        """使用 NumPy 进行加速叠加（支持带或不带透明通道的图片）。
        
        参数:
            bg (Image.Image): 背景图片。
            fg (Image.Image): 需要叠加的前景图片。
            position (tuple): 叠加的位置，默认为 (0, 0)。

        返回:
            Image.Image: 叠加后的图片。
        """
        # 确保图片为 RGBA
        bg = bg.convert("RGBA")
        fg = fg.convert("RGBA")

        # 转换为 NumPy 数组
        bg_arr = np.array(bg, dtype=np.uint8)
        fg_arr = np.array(fg, dtype=np.uint8)

        # 获取叠加区域
        x, y = position
        bh, bw = bg.size
        fh, fw = fg.size

        # 限制叠加范围，防止越界
        if x + fw > bw:
            fw = bw - x
        if y + fh > bh:
            fh = bh - y

        # 提取 RGBA 通道
        fg_rgb = fg_arr[:fh, :fw, :3]
        fg_alpha = fg_arr[:fh, :fw, 3] / 255.0  # 归一化 alpha

        bg_rgb = bg_arr[y:y+fh, x:x+fw, :3]
        bg_alpha = bg_arr[y:y+fh, x:x+fw, 3] / 255.0

        # 计算新的 alpha 通道
        out_alpha = fg_alpha + bg_alpha * (1 - fg_alpha)
        out_rgb = (fg_rgb * fg_alpha[:, :, None] + bg_rgb * bg_alpha[:, :, None] * (1 - fg_alpha[:, :, None])) / out_alpha[:, :, None]

        # 组合结果
        bg_arr[y:y+fh, x:x+fw, :3] = np.clip(out_rgb, 0, 255).astype(np.uint8)
        bg_arr[y:y+fh, x:x+fw, 3] = np.clip(out_alpha * 255, 0, 255).astype(np.uint8)

        return Image.fromarray(bg_arr, "RGBA")

class ImageDrawManager(ContextDecorator):
    def __init__(self, image: Image.Image, mode: str = 'ps', ppi: int = 72):
        """初始化"""
        self.image = image
        self.draw = None
        self.design_mode = mode
        self.design_ppi = ppi
        self.operations: List[Union[TextOperation, RectangleOperation]] = []  # 记录操作

    def __enter__(self):
        """进入上下文时打开图片并创建绘制对象"""
        return self  # 返回实例以便在上下文中使用

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开上下文时执行操作并保存资源"""
        if self.image:
            self.image.close()  # 释放图片资源

    def add_text(self, operation: TextOperation):
        """写入文字到图片"""
        self.operations.append(operation)

    def add_rectangle(self, operation: RectangleOperation):
        """绘制矩形到图片"""
        self.operations.append(operation)

    def composite_paste(
        self, 
        fg: Image.Image, 
        position: tuple = (0, 0)
    ) -> Image.Image:
        """使用 paste 方法叠加图片（适用于不带透明通道的图片）。

        该方法适用于不带 alpha 通道的前景图叠加到背景图上，
        如果前景图含有 alpha 通道，则会丢失 alpha 通道的信息。

        参数:
            fg (Image.Image): 需要叠加的前景图片。
            position (tuple): 前景图片放置的位置，默认为 (0, 0)。

        返回:
            Image.Image: 叠加后的图片对象。
        """
        # 叠加前景图到背景图
        self.image.paste(fg, position)

    def composite_alpha(
        self, 
        fg: Image.Image, 
        position: tuple = (0, 0)
    ) -> Image.Image:
        """使用 alpha_composite 方法叠加两张图片（适用于带透明通道的图片）。

        该方法适用于带有 alpha 通道的图片，能够保留前景图的透明度效果。
        如果前景图不包含 alpha 通道，会先转换为 RGBA 格式。

        参数:
            fg (Image.Image): 需要叠加的前景图片。
            position (tuple): 前景图片放置的位置，默认为 (0, 0)。

        返回:
            Image.Image: 叠加后的图片对象，包含透明度效果。
        """
        # 如果前景图没有 alpha 通道，先转换为 RGBA
        if fg.mode != 'RGBA':
            fg = fg.convert("RGBA")

        # 叠加前景图到背景图，并保留透明度效果
        self.image.alpha_composite(fg, position)
    
    def get_text_width(self, text: str, font_index: int, font_size: int) -> float:
        """
        计算指定文本的像素宽度。

        参数:
            text (str): 需要计算宽度的文本内容。
            font (ImageFont.FreeTypeFont): 使用的字体对象。

        返回:
            float: 文本的像素宽度。
        """
        if self.design_mode == 'ps':
            size = int(self.design_ppi / 72 * font_size)
        else:
            size = int(72 / 72 * font_size)
        font = font_manager.get_font(font_index, size)
        return font.getlength(text)
    
    def get_text_bbox(self, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int, int, int]:
        """
        计算指定文本的边界框（bbox）。

        参数:
            text (str): 需要计算边界的文本内容。
            font (ImageFont.FreeTypeFont): 使用的字体对象。

        返回:
            tuple[int, int, int, int]: 文本的边界框 (left, top, right, bottom)。
        """
        return font.getbbox(text)
    
    def truncate_text_to_width(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
        """
        根据最大宽度截取文本，超出部分使用省略号 "..." 代替。

        参数:
            text (str): 需要检查的文本内容。
            font (ImageFont.FreeTypeFont): 使用的字体对象。
            max_width (int): 允许的最大宽度（像素）。

        返回:
            str: 处理后的文本，如果超出宽度，则以 "..." 结尾。
        """
        if font.getlength(text) <= max_width:
            return text

        ellipsis_width = font.getlength("...")
        truncated_text = text

        while truncated_text and font.getlength(truncated_text) + ellipsis_width > max_width:
            truncated_text = truncated_text[:-1]  # 逐字符去掉末尾字符

        return truncated_text + "..." if truncated_text else "..."

    def _draw_text(self, operation: TextOperation):
        """执行写入文字的操作"""
        # 计算不同mode和ppi下的font px size
        if self.design_mode == 'ps':
            size = int(self.design_ppi / 72 * operation.font_size)
        else:
            size = int(72 / 72 * operation.font_size)
        font = font_manager.get_font(operation.font_index, size)
        text = str(operation.text)
        # 对于不同对齐模式下的文字x坐标的处理
        if operation.align == 'center':
            text_wight = self._get_text_length(text=text, font=font)
            xy = [operation.position[0] - text_wight/2, operation.position[1]]
        elif operation.align == 'right':
            text_wight = self._get_text_length(text=text, font=font)
            xy = [operation.position[0] - text_wight, operation.position[1]]
        else:
            xy = [operation.position[0], operation.position[1]]
        self.draw.text(
            xy=xy, 
            text=text, 
            fill=operation.color, 
            font=font
        )
    
    def _get_text_length(self, text: str, font: ImageFont.FreeTypeFont) -> float:
        """
        计算指定文本的像素宽度。

        参数:
            text (str): 需要计算宽度的文本内容。
            font (ImageFont.FreeTypeFont): 使用的字体对象。

        返回:
            float: 文本的像素宽度。
        """
        return font.getlength(text)

    def _draw_rectangle(self, operation: RectangleOperation):
        """执行绘制矩形的操作，支持圆角和直角矩形"""
        if operation.corner_radius > 0:
            # 绘制圆角矩形
            self.draw.rounded_rectangle(
                xy=[operation.position, (operation.position[0] + operation.size[0], operation.position[1] + operation.size[1])], 
                radius=operation.corner_radius, 
                fill=operation.color
            )
        else:
            # 绘制直角矩形
            self.draw.rectangle(
                xy=[operation.position, (operation.position[0] + operation.size[0], operation.position[1] + operation.size[1])], 
                fill=operation.color
            )

    def execute_operations(self):
        """统一执行所有记录的操作，按照优先级顺序绘制。

        该方法会根据操作的优先级（priority）从低到高排序，
        先绘制矩形，再绘制文字，确保优先级高的操作先完成。
        """
        self.draw = ImageDraw.Draw(self.image)
        # 按照优先级对操作进行排序，优先级小的操作先执行
        sorted_operations = sorted(self.operations, key=lambda x: x.priority)

        # 先绘制矩形
        for operation in sorted_operations:
            if isinstance(operation, RectangleOperation):
                self._draw_rectangle(operation)

        # 再绘制文字
        for operation in sorted_operations:
            if isinstance(operation, TextOperation):
                self._draw_text(operation)
        
        self.operations = None
    
    def get_image(self):
        """返回处理后的图片"""
        return self.image
