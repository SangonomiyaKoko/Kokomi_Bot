from typing import Tuple, Literal


class TextOperation:
    """封装写入文字的操作，支持指定字体、大小、颜色和优先级
    
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
        self.text = text
        self.position = position
        self.font_index = font_index
        self.font_size = font_size
        self.color = color
        self.priority = priority
        self.align = align  # 文字对齐方式

class RectangleOperation:
    """封装绘制矩形的操作，支持圆角矩形
    
    参数:
        position (tuple): 矩形的位置 (x, y)
        size (tuple): 矩形的尺寸 (宽, 高)
        color (tuple): 矩形的填充颜色 (R, G, B)
        corner_radius (int, optional): 圆角半径，默认值为 0，即不绘制圆角
        priority (int, optional): 操作的优先级，数字越小优先级越高。默认值为 10
    """
    
    def __init__(self, position: tuple, size: tuple, color: tuple, corner_radius: int = 0, priority: int = 10):
        self.position = position
        self.size = size
        self.color = color
        self.corner_radius = corner_radius
        self.priority = priority
