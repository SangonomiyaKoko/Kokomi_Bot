import os

from ..logs import ExceptionLogger
from ..schemas import KokomiUser
from ..config import ASSETS_DIR
from ..common import (
    TimeFormat
)
from ..image import (
    ImageDrawManager, ImageHandler, TextOperation as Text, RectangleOperation as Rectangle
)


@ExceptionLogger.handle_program_exception_async
async def main(
    user: KokomiUser
) -> dict:
    result = get_png(
        user=user
    )
    return result


@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(user: KokomiUser) -> str:
    # 画布宽度和高度
    width, height = 1580, 2130
    # 背景颜色（RGBA）
    # background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    bg_png_path = os.path.join(ASSETS_DIR, 'content', 'default', user.local.language, f'theme.png')
    res_img = ImageHandler.open_image(bg_png_path)
    # 需要叠加的 文字/矩形
    with ImageDrawManager(res_img, 'ps', 72) as image_manager:
        # 叠加图片主题图片
        index = 0
        if user.local.theme == 'default':
            if user.local.content == 'dark':
                index = 1
            else:
                index = 0
        else:
            theme_index = {
                'xnn': 2,
                'mygo': 3,
                'mavuika': 5,
                'furina': 4
            }
            index = theme_index.get(user.local.theme)
        
        image_manager.add_rectangle(
            Rectangle(
                position=(74, 192 + 311 * index),
                size=(100, 10),
                color=(137, 201, 151)
            )
        )
        image_manager.add_rectangle(
            Rectangle(
                position=(74, 192 + 311 * index),
                size=(10, 100),
                color=(137, 201, 151)
            )
        )
        image_manager.add_rectangle(
            Rectangle(
                position=(1406, 493 + 311 * index),
                size=(100, 10),
                color=(137, 201, 151)
            )
        )
        image_manager.add_rectangle(
            Rectangle(
                position=(1496, 403 + 311 * index),
                size=(10, 100),
                color=(137, 201, 151)
            )
        )

        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result
