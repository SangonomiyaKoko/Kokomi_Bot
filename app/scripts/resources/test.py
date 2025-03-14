from PIL import Image

from ..logs import logging
from ..logs import ExceptionLogger
from ..language import Content
from ..common import (
    ThemeTextColor, TimeFormat
)
from ..image import (
    Text_Data, Box_Data, Picture
)
from ..schemas import KokomiUser

@ExceptionLogger.handle_program_exception_async
async def main(user: KokomiUser, test_msg: str) -> dict:
    res_img = get_png(
        user=user,
        test_msg = test_msg
    )
    result = Picture.return_img(img=res_img)
    del res_img
    return result

@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(user: KokomiUser, test_msg: str) -> str:
    # 画布宽度和高度
    width, height = 150, 75
    # 背景颜色（RGBA）
    background_color = Picture.hex_to_rgb(user.local.background, 0)
    # 创建画布
    res_img = Image.new("RGBA", (width, height), background_color)
    # 获取语言对应的文本文字
    content_text = Content.get_content_language(user.local.language)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 需要叠加的 文字/矩形
    text_list = []
    box_list = []
    text_list.append(
        Text_Data(
            xy=(0,0),
            text=content_text.Test,
            fill=theme_text_color.TextThemeColor2,
            font_index=1,
            font_size=50
        )
    )
    text_list.append(
        Text_Data(
            xy=(0,50),
            text=test_msg,
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=25
        )
    )
    res_img = Picture.add_box(box_list, res_img)
    res_img = Picture.add_text(text_list, res_img)
    return res_img


            


