import os
import time
from typing import List

from PIL import Image, ImageFont, ImageDraw

from ..config import OUTPUT_DIR
from .fonts import font_manager

fonts = None

class Text_Data:
    def __init__(self, xy: tuple, text: str, fill: tuple, font_index: int, font_size: int):
        self.xy = xy
        self.text = text
        self.fill = fill
        self.font_index = font_index
        self.font_size = font_size

    def __repr__(self):
        return (f"Text_Data(xy={self.xy}, text={self.text}, "
                f"fill={self.fill}, font_index={self.font_index}, font_size={self.font_size})")


class Box_Data:
    def __init__(self, xy: tuple, fill: tuple):
        self.xy = xy
        self.fill = fill

    def __repr__(self):
        return f"Box_Data(xy={self.xy}, fill={self.fill})"


class Picture:
    def hex_to_rgb(hex_color: str ,alpha: int = None) -> str:
        "16进制颜色转rgb颜色"
        if alpha:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return (r, g, b, alpha)
        else:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return (r, g, b)
    
    def return_img(img: Image.Image) -> str:
        try:
            file_name = os.path.join(OUTPUT_DIR, str(time.time()*1000) + '.png')
            img.save(file_name)
            return {
                'status': 'ok',
                'code': 1000,
                'message': 'Success',
                'data': {
                    'img': file_name
                }
            }
        finally:
            del img
    
    def x_coord(in_str: str, font: ImageFont.FreeTypeFont) -> float:
        "获取文字的长度(像素)"
        # x = font.getsize(in_str)[0]
        x = font.getlength(in_str)
        return x
    
    def formate_str(in_str: str, str_len, max_len):
        if str_len <= max_len:
            return in_str
        else:
            return in_str[:int(max_len/str_len*len(in_str))-2] + '...'

    def add_box(box_list: List[Box_Data], res_img: Image.Image) -> Image.Image:
        "在图片上叠加上文字"
        if box_list is None:
            return res_img
        img = ImageDraw.ImageDraw(res_img)
        for index in box_list:
            img.rectangle(
                xy=index.xy,
                fill=index.fill,
                outline=None
            )
        box_list.clear()
        return res_img

    def add_text(text_list: List[Text_Data], res_img: Image.Image) -> Image.Image:
        "在图片上叠加上矩形"
        if text_list is None:
            return res_img
        draw = ImageDraw.Draw(res_img)
        for index in text_list:
            fontStyle = font_manager.get_font(index.font_index, index.font_size)
            draw.text(
                xy=index.xy,
                text=index.text,
                fill=index.fill,
                font=fontStyle
            )
        text_list.clear()
        return res_img
    
    def add_png(
        bottom_img: Image.Image, 
        top_img: Image.Image, 
        xy: tuple = (0, 0)
    ) -> Image.Image:
        "不带有alpha通道图片叠加，如有会丢失alpha通道的信息"
        bottom_img.paste(top_img, xy)
        return bottom_img
    
    def add_png_with_alpha(
        bottom_img: Image.Image, 
        top_img: Image.Image, 
        xy: tuple = (0, 0)
    ) -> Image.Image:
        "带有alpha通道图片叠加，不带alpha通道无法叠加"
        if top_img.mode != 'RGBA':
            # 检查顶图是否有 alpha 通道
            raise ValueError('Top image does not have an alpha channel')
        bottom_img.alpha_composite(top_img, xy)
        return bottom_img