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
    help_png_path = os.path.join(ASSETS_DIR, 'docs', user.local.content, user.local.language, 'link.png')
    if os.path.exists(help_png_path):
        res_img = ImageHandler.open_image(help_png_path)
        result = ImageHandler.save_image(res_img)
    else:
        result = JSONResponse.API_10008_ImageResourceMissing
    return result

@ExceptionLogger.handle_program_exception_async
async def post_bind(
    user: KokomiUser,
    region_id: int,
    account_id: int
) -> dict:
    data = {
        'platform': user.platform.name,
        'user_id': user.basic.id,
        'region_id': region_id,
        'account_id': account_id
    }
    if bot_settings.USE_MOCK:
        result = Mock.read_data('post_bind.json')
        logging.debug('Using MOCK, skip network requests')
    else:
        result = await BindAPI.post_user_bind(data)
    if 2000 <= result['code'] <= 9999:
        logging.error(f"API Error, Error: {result['message']}")
        return result
    if result['code'] != 1000:
        return result
    result = get_png(
        user=user,
        result=result['data']
    )
    return result

@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(user: KokomiUser, result: dict) -> str:
    # 画布宽度和高度
    width, height = 2235, 422
    # 背景颜色（RGBA）
    background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    res_img = ImageHandler.new_image([width, height], background_color)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 需要叠加的 文字/矩形
    with ImageDrawManager(res_img, 'ps', 72) as image_manager:
        # 叠加图片主题图片
        if user.local.theme != 'default':
            theme_png_path = os.path.join(ASSETS_DIR, 'theme', user.local.theme, f'link.png')
            if os.path.exists(theme_png_path):
                image_manager.composite_alpha(theme_png_path, (0, 0))
            else:
                ...

        # 叠加图片主体
        content_png_path = os.path.join(ASSETS_DIR, 'content', user.local.content, user.local.language, 'link.png')
        image_manager.composite_alpha(content_png_path, (0, 0))


        if bot_settings.SHOW_DOG_TAG:
            if not result['user']['dog_tag'] or result['user']['dog_tag'] == [] or result['user']['dog_tag'] == {}:
                pass
            else:
                insignias_png_path_list = Insignias.get_insignias(
                    region_id = result['user']['region'],
                    account_id = result['user']['id'],
                    clan_id = None,
                    response = result['user']['dog_tag']
                )
                for insignias_png_path in insignias_png_path_list:
                    image_manager.composite_alpha(insignias_png_path, (66, 51), resize_size=(320, 320))
        
        image_manager.add_text(
            Text(
                text=result['user']['name'],
                position=(434, 63),
                font_index=1,
                font_size=80,
                color=theme_text_color.TextThemeColor2
            )
        )
        if result['user']['level']:
            image_manager.add_rectangle(
                Rectangle(
                    position=(442, 168),
                    size=(130, 49),
                    corner_radius=5,
                    color=Utils.get_level_color(result['user']['level'])
                )
            )
            image_manager.add_text(
                Text(
                    text="Lv " + str(result['user']['level']),
                    position=(458, 174),
                    font_index=1,
                    font_size=36,
                    color=(255, 255, 255)
                )
            )
        else:
            image_manager.add_rectangle(
                Rectangle(
                    position=(442, 168),
                    size=(130, 49),
                    corner_radius=5,
                    color=Utils.get_level_color(result['user']['level'])
                )
            )
            image_manager.add_text(
                Text(
                    text="——",
                    position=(458, 174),
                    font_index=1,
                    font_size=36,
                    color=(255, 255, 255),
                    align='left'
                )
            )
        image_manager.add_text(
            Text(
                text="UID: " + str(result['user']['id']),
                position=(602, 168),
                font_index=1,
                font_size=48,
                color=theme_text_color.TextThemeColor4
            )
        )
        ok_png_path = os.path.join(ASSETS_DIR, 'components', 'icon', 'ok.png')
        error_png_path = os.path.join(ASSETS_DIR, 'components', 'icon', 'error.png')
        ok_color = (137, 201 ,151)
        error_color = (246, 179, 127)
        if result['user']['hidden']:
            image_manager.composite_alpha(error_png_path, (457, 312))
            image_manager.add_text(
                Text(
                    text="Hidden",
                    position=(625, 311),
                    font_index=1,
                    font_size=30,
                    color=error_color,
                    align='right'
                )
            )
        else:
            image_manager.composite_alpha(ok_png_path, (457, 312))
            image_manager.add_text(
                Text(
                    text="OK",
                    position=(625, 311),
                    font_index=1,
                    font_size=30,
                    color=ok_color,
                    align='right'
                )
            )
        if result['func']['recent']:
            image_manager.composite_alpha(ok_png_path, (707, 312))
            image_manager.add_text(
                Text(
                    text="OK",
                    position=(873, 311),
                    font_index=1,
                    font_size=30,
                    color=ok_color,
                    align='right'
                )
            )
        else:
            image_manager.composite_alpha(error_png_path, (707, 312))
            image_manager.add_text(
                Text(
                    text="——",
                    position=(873, 311),
                    font_index=1,
                    font_size=30,
                    color=error_color,
                    align='right'
                )
            )
        if result['func']['recents']:
            image_manager.composite_alpha(ok_png_path, (926, 312))
            image_manager.add_text(
                Text(
                    text="OK",
                    position=(1094, 311),
                    font_index=1,
                    font_size=30,
                    color=ok_color,
                    align='right'
                )
            )
        else:
            image_manager.composite_alpha(error_png_path, (926, 312))
            image_manager.add_text(
                Text(
                    text="——",
                    position=(1094, 311),
                    font_index=1,
                    font_size=30,
                    color=error_color,
                    align='right'
                )
            )
        
        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result

@ExceptionLogger.handle_program_exception_async
async def lang_help(user: KokomiUser) -> dict:
    help_png_path = os.path.join(ASSETS_DIR, 'docs', user.local.content, user.local.language, 'lang.png')
    if os.path.exists(help_png_path):
        res_img = ImageHandler.open_image(help_png_path)
        result = ImageHandler.save_image(res_img)
    else:
        result = JSONResponse.API_10008_ImageResourceMissing
    return result

@ExceptionLogger.handle_program_exception_async
async def update_language(
    user: KokomiUser,
    language: str
) -> dict:
    result = UserLocalDB().update_language(user,language)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess

@ExceptionLogger.handle_program_exception_async
async def algo_help(user: KokomiUser) -> dict:
    help_png_path = os.path.join(ASSETS_DIR, 'docs', user.local.content, user.local.language, 'algo.png')
    if os.path.exists(help_png_path):
        res_img = ImageHandler.open_image(help_png_path)
        result = ImageHandler.save_image(res_img)
    else:
        result = JSONResponse.API_10008_ImageResourceMissing
    return result

@ExceptionLogger.handle_program_exception_async
async def update_algorithm(
    user: KokomiUser,
    algorithm: str
) -> dict:
    result = UserLocalDB().update_algorithm(user,algorithm)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess

@ExceptionLogger.handle_program_exception_async
async def mode_help(user: KokomiUser) -> dict:
    help_png_path = os.path.join(ASSETS_DIR, 'docs', user.local.content, user.local.language, 'mode.png')
    if os.path.exists(help_png_path):
        res_img = ImageHandler.open_image(help_png_path)
        result = ImageHandler.save_image(res_img)
    else:
        result = JSONResponse.API_10008_ImageResourceMissing
    return result

@ExceptionLogger.handle_program_exception_async
async def update_content(
    user: KokomiUser,
    content: str
) -> dict:
    result = UserLocalDB().update_content(user,content)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess
    
@ExceptionLogger.handle_program_exception_async
async def update_theme(
    user: KokomiUser,
    theme: str
) -> dict:
    result = UserLocalDB().update_theme(user,theme)
    if result['code'] != 1000:
        return result
    else:
        return JSONResponse.API_9006_ChangeSuccess