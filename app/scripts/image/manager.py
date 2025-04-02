from contextlib import ContextDecorator
from typing import List, Union, Tuple, Optional

from PIL import Image, ImageFont, ImageDraw

from ..logs import logging
from .fonts import font_manager
from .operations import TextOperation, RectangleOperation


class ImageDrawManager(ContextDecorator):
    """管理图像绘制操作的类，提供多种绘制方法，如添加文字、绘制矩形、图片合成等

    属性:
        image (Image.Image): 被绘制的背景图像
        draw (ImageDraw.Draw): 用于绘制图像的对象
        design_mode (str): 设计模式，控制绘制的细节（如使用PSD文件设计使用 'ps' 模式）
        design_ppi (int): 每英寸像素数（用于字体大小计算）
        operations (List[Union[TextOperation, RectangleOperation]]): 保存所有待执行的绘制操作

    注意:
        计算字体大小时，PPI（每英寸像素数）起着至关重要的作用，尤其在不同的设计模式中，PPI 值决定了字体在物理设备上的显示大小
        PPI 越高，字体的实际显示大小越小，因为每英寸显示更多的像素。在设计时，字体大小可能是基于固定的像素尺寸，而最终显示效果会根据设备的 PPI 进行缩放
        在 PSD 文档中，PPI 用于确定图像和字体的实际物理尺寸。在默认的 72 PPI 的标准下，字体的大小通常与设计尺寸一致
        如果 PSD 文档的 PPI 大于 72，则需要根据该 PPI 值来调整字体的像素大小，以确保最终效果在不同设备上显示一致
    
    方法:
        add_text(): 添加文字绘制操作
        add_rectangle(): 添加矩形绘制操作
        composite_paste(): 使用 paste 方法合成背景图与前景图（适用于无透明度的图片）
        composite_alpha(): 使用 alpha_composite 方法合成背景图与前景图（适用于带透明度的图片）
        get_text_width(): 计算指定文本的宽度
        get_text_bbox(): 计算指定文本的边界框
        truncate_text_to_width(): 截取超出指定宽度的文本并加上省略号
        execute_operations(): 执行所有记录的绘制操作，并按优先级排序
        get_image(): 返回绘制后的图片
    """
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
        image_path: str,
        position: Tuple[int, int] = (0, 0),
        crop_box: Optional[Tuple[int, int, int, int]] = None,
        resize_size: Optional[Tuple[int, int]] = None
    ) -> Image.Image:
        """使用 paste 方法将前景图叠加到背景图上（适用于矩形不带透明通道的图片）

        该方法将指定路径的前景图叠加到当前背景图上。如果前景图含有 alpha 通道，则会丢失 alpha 通道的信息

        可选操作包括裁剪前景图和调整前景图的大小

        参数:
            image_path (str): 前景图片的文件路径
            position (Tuple[int, int]): 前景图片放置的位置，默认为 (0, 0)
            crop_box (Optional[Tuple[int, int, int, int]]): 前景图片裁剪框 (左, 上, 右, 下)，默认为 None
            resize_size (Optional[Tuple[int, int]]): 前景图片的目标尺寸 (宽, 高)，默认为 None

        返回:
            Image.Image: 叠加后的图片对象。返回的图片是当前背景图（self.image）与前景图叠加后的结果
        """
        # 叠加前景图到背景图
        try:
            fg = Image.open(image_path)
            if crop_box:
                fg = fg.crop(crop_box)  # 裁剪前景图
            if resize_size:
                fg = fg.resize(resize_size)  # 调整前景图大小
            self.image.paste(fg, position)  # 将前景图粘贴到背景图上
        except (FileNotFoundError, OSError):
            logging.warning(f"File not found: {image_path}")
        finally:
            if fg:
                fg.close()

    def composite_alpha(
        self, 
        image_path: str, 
        position: Tuple[int, int] = (0, 0), 
        crop_box: Optional[Tuple[int, int, int, int]] = None, 
        resize_size: Optional[Tuple[int, int]] = None
    ) -> Image.Image:
        """使用 alpha_composite 方法将前景图叠加到背景图上（适用于带透明通道的图片）

        该方法将指定路径的前景图叠加到当前背景图上，并保留前景图的透明度效果
        如果前景图不包含 alpha 通道，会先转换为 RGBA 格式
        
        可选操作包括裁剪前景图和调整前景图的大小

        参数:
            image_path (str): 前景图片的文件路径
            position (Tuple[int, int]): 前景图片放置的位置，默认为 (0, 0)
            crop_box (Optional[Tuple[int, int, int, int]]): 前景图片裁剪框 (左, 上, 右, 下)，默认为 None
            resize_size (Optional[Tuple[int, int]]): 前景图片的目标尺寸 (宽, 高)，默认为 None

        返回:
            Image.Image: 叠加后的图片对象，包含透明度效果
        """
        try:
            fg = Image.open(image_path)
            if crop_box:
                fg = fg.crop(crop_box)  # 裁剪前景图
            if resize_size:
                fg = fg.resize(resize_size)  # 调整前景图大小

            # 如果前景图没有 alpha 通道，先转换为 RGBA
            if fg.mode != 'RGBA':
                fg = fg.convert("RGBA")

            # 叠加前景图到背景图，并保留透明度效果
            self.image.alpha_composite(fg, position)  # 将前景图叠加到背景图
        except (FileNotFoundError, OSError):
            logging.warning(f"File not found: {image_path}")
        finally:
            if fg:
                fg.close()
    
    def get_text_width(self, text: str, font_index: int, font_size: int) -> float:
        """
        计算指定文本的像素宽度

        参数:
            text (str): 需要计算宽度的文本内容
            font (ImageFont.FreeTypeFont): 使用的字体对象

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
        计算指定文本的边界框（bbox）

        参数:
            text (str): 需要计算边界的文本内容。
            font (ImageFont.FreeTypeFont): 使用的字体对象

        返回:
            tuple[int, int, int, int]: 文本的边界框 (left, top, right, bottom)
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
        self.draw = None
    
    def get_image(self):
        """返回处理后的图片"""
        return self.image
