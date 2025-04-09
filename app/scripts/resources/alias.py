import os

from ..logs import ExceptionLogger, logging
from ..api import BindAPI, Mock
from ..schemas import JSONResponse
from ..db import UserLocalDB
from ..schemas import KokomiUser
from ..config import ASSETS_DIR, bot_settings
from ..language import Content
from ..common import (
    Insignias, Utils, ThemeTextColor, TimeFormat
)
from ..image import (
    ImageDrawManager, ImageHandler, TextOperation as Text, RectangleOperation as Rectangle
)



@ExceptionLogger.handle_program_exception_async
async def help(user: KokomiUser) -> dict:
    help_png_path = os.path.join(ASSETS_DIR, 'docs', user.local.content, user.local.language, 'alias.png')
    if os.path.exists(help_png_path):
        res_img = ImageHandler.open_image(help_png_path)
        result = ImageHandler.save_image(res_img)
    else:
        result = JSONResponse.API_10008_ImageResourceMissing
    return result

@ExceptionLogger.handle_program_exception_async
async def add_alias(
    user: KokomiUser,
    alias_data: dict
) -> dict:
    result = UserLocalDB().add_alias(user,alias_data)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_10010_AliasAddedSuccessfully
    
@ExceptionLogger.handle_program_exception_async
async def del_alias(
    user: KokomiUser,
    alias_index: int
) -> dict:
    result = UserLocalDB().del_alias(user,alias_index)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_10011_AliasDeletedSuccessfully
    
@ExceptionLogger.handle_program_exception_async
async def alias_list(
    user: KokomiUser
) -> dict:
    if not user.local.alias_list or len(user.local.alias_list) < 1:
        return JSONResponse.API_10012_AliasNotSet
    result = get_png(
        user=user
    )
    return result


@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(user: KokomiUser) -> str:
    # 画布宽度和高度
    width, height = 1580, 260 + len(user.local.alias_list) * 100 + 70
    # 背景颜色（RGBA）
    background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    res_img = ImageHandler.new_image([width, height], background_color)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 需要叠加的 文字/矩形
    with ImageDrawManager(res_img, 'ps', 300) as image_manager:
        # 叠加图片主题图片

        # 叠加图片主体
        content_png_path = os.path.join(ASSETS_DIR, 'content', user.local.content, user.local.language, 'alias.png')
        image_manager.composite_alpha(content_png_path, (0, 0))

        i = 0
        for alias_data in user.local.alias_list:
            image_manager.add_text(
                Text(
                    text=str(i + 1),
                    position=(148,64+50*i),
                    font_index=1,
                    font_size=8,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=alias_data['alias'],
                    position=(218,64+50*i),
                    font_index=1,
                    font_size=8,
                    color=theme_text_color.TextThemeColor3,
                    align='left'
                )
            )
            image_manager.add_text(
                Text(
                    text=Utils.get_region_by_id(alias_data['region_id']),
                    position=(747,64+50*i),
                    font_index=1,
                    font_size=8,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=alias_data['nickname'],
                    position=(857,64+50*i),
                    font_index=1,
                    font_size=8,
                    color=theme_text_color.TextThemeColor3,
                    align='left'
                )
            )
            
            i += 1

        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result