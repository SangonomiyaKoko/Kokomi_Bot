from ..logs import ExceptionLogger
from ..language import Content
from ..common import (
    ThemeTextColor, TimeFormat, Utils
)
from ..image import (
    ImageDrawManager, ImageHandler, TextOperation as Text, RectangleOperation as Rectangle
)
from ..schemas import KokomiUser

@ExceptionLogger.handle_program_exception_async
async def main(user: KokomiUser, test_msg: str) -> dict:
    result = get_png(
        user=user,
        test_msg=test_msg
    )
    return result

@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(user: KokomiUser, test_msg: str) -> str:
    # 画布宽度和高度
    width, height = 150, 75
    # 背景颜色（RGBA）
    background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    res_img = ImageHandler.new_image([width, height], background_color)
    # 获取语言对应的文本文字
    content_text = Content.get_content_language(user.local.language)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 需要叠加的 文字/矩形
    with ImageDrawManager(res_img) as image_manager:
        image_manager.add_text(
            Text(
                text=content_text.Test,
                position=(0,0),
                font_index=1,
                font_size=50,
                color=theme_text_color.TextThemeColor2,
                align='left',
                priority=10
            )
        )
        image_manager.add_text(
            Text(
                text=test_msg,
                position=(0,50),
                font_index=1,
                font_size=25,
                color=theme_text_color.TextThemeColor3,
                align='left',
                priority=10
            )
        )
        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result
