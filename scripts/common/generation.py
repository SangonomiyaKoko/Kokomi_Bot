import os
import time

from PIL import Image, ImageFont, ImageDraw

from scripts.config import OUTPUT_DIR
from .fonts import font_manager

fonts = None

class Text_Data:
    def __init__(
        self,
        xy: tuple,
        text: str,
        fill: tuple,
        font_index: int,
        font_size: int
    ):
        self.xy = xy
        self.text = text
        self.fill = fill
        self.font_index = font_index
        self.font_size = font_size

class Box_Data:
    def __init__(
        self,
        xy: tuple,
        fill: tuple,
    ):
        self.xy = xy
        self.fill = fill



class Picture:
    def hex_to_rgb(hex_color: str ,alpha:int = None) -> str:
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
        # x = font.getsize(in_str)[0]
        x = font.getlength(in_str)
        return x
    
    def formate_str(in_str: str, str_len, max_len):
        if str_len <= max_len:
            return in_str
        else:
            return in_str[:int(max_len/str_len*len(in_str))-2] + '...'

    def add_box(box_list, res_img):
        if box_list is None:
            return res_img
        img = ImageDraw.ImageDraw(res_img)
        for index in box_list:
            index: Box_Data
            img.rectangle(
                xy=index.xy,
                fill=index.fill,
                outline=None
            )
        return res_img

    def add_text(text_list, res_img):
        if text_list is None:
            return res_img
        draw = ImageDraw.Draw(res_img)
        for index in text_list:
            index: Text_Data
            fontStyle = font_manager.get_font(index.font_index, index.font_size)
            draw.text(
                xy=index.xy,
                text=index.text,
                fill=index.fill,
                font=fontStyle
            )
        return res_img