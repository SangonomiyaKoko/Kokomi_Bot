import os
from PIL import Image
from typing_extensions import TypedDict

from ..config import ASSETS_DIR, bot_settings
from ..logs import logging
from ..api import BaseAPI, Mock
from ..logs import ExceptionLogger
from ..language import Content
from ..common import (
    Insignias, Utils, GameData, ThemeTextColor, ThemeRatingColor, TimeFormat
)
from ..image import (
    ImageDrawManager, ImageHandler, TextOperation as Text, RectangleOperation as Rectangle
)
from ..schemas import (
    KokomiUser, UserBasicDict, UserClanDict, UserSignatureDict
)


class UserBaseResult(TypedDict):
    user: UserBasicDict
    clan: UserClanDict
    statistics: dict


@ExceptionLogger.handle_program_exception_async
async def main(
    user: KokomiUser
) -> dict:
    path = '/api/v1/robot/user/stats/card/'
    params = {
        'region': Utils.get_region_by_id(user.bind.region_id),
        'account_id': user.bind.account_id,
        'language': Utils.get_language(user.local.language)
    }
    if user.local.algorithm:
        params['algo_type'] = user.local.algorithm
    if bot_settings.USE_MOCK:
        result = Mock.read_data('card.json')
        logging.debug('Using MOCK, skip network requests')
    else:
        result = await BaseAPI.get(
            path=path,
            params=params
        )
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
def get_png(
    user: KokomiUser,
    result: dict
) -> str:
    # 画布宽度和高度
    width, height = 1920, 1080
    # 背景颜色（RGBA）
    background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    res_img = ImageHandler.new_image([width, height], background_color)
    # 获取语言对应的文本文字
    content_text = Content.get_content_language(user.local.language)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor('light')
    # 获取不同主题的评分颜色
    theme_rating_color = ThemeRatingColor('light')
    # 开始图片渲染流程
    with ImageDrawManager(res_img, 'ps', 72) as image_manager:

        # 叠加图片主体
        content_png_path = os.path.join(ASSETS_DIR, 'content', 'default', user.local.language, 'card.png')
        image_manager.composite_alpha(content_png_path, (0, 0))

        # ===================== Header组件 =====================
        
        region = Utils.get_region_by_id(result['user']['region'])
        image_manager.add_rectangle(
            Rectangle(
                position=(473, 234),
                size=(80, 35),
                color=Utils.get_region_color(result['user']['region']),
                corner_radius=5
            )
        )
        image_manager.add_text(
            Text(
                text=region.upper(),
                position=(513, 238),
                font_index=1,
                font_size=26,
                color=(255, 255, 255),
                align='center'
            )
        )
        image_manager.add_rectangle(
            Rectangle(
                position=(569, 234),
                size=(100, 35),
                color=Utils.get_level_color(result['user']['level']),
                corner_radius=5
            )
        )
        image_manager.add_text(
            Text(
                text='Lv ' + str(result['user']['level']),
                position=(618, 238),
                font_index=1,
                font_size=26,
                color=(255, 255, 255),
                align='center'
            )
        )
        image_manager.add_rectangle(
            Rectangle(
                position=(683, 234),
                size=(183, 35),
                color=(175, 175, 175),
                corner_radius=5
            )
        )
        image_manager.add_text(
            Text(
                text=str(result['user']['id']),
                position=(774, 238),
                font_index=1,
                font_size=26,
                color=(255, 255, 255),
                align='center'
            )
        )
        if result['clan']['id'] != None:
            tag = '['+str(result['clan']['tag'])+']'
            clan_league_color = GameData.clan_league_color.get(result['clan']['league'])
            image_manager.add_text(
                Text(
                    text=tag,
                    position=(469, 177),
                    font_index=1,
                    font_size=42,
                    color=clan_league_color
                )
            )
            tag_w = image_manager.get_text_width(tag, 1, 42) + 20
        else:
            tag = 'None'
            tag_w = 0
        
        image_manager.add_text(
            Text(
                text=result['user']['name'],
                position=(469+tag_w, 177),
                font_index=1,
                font_size=42,
                color=theme_text_color.TextThemeColor2
            )
        )

        text_1 = content_text.Createdat + ':'
        image_manager.add_text(
            Text(
                text=text_1,
                position=(472, 285),
                font_index=1,
                font_size=28,
                color=theme_text_color.TextThemeColor3
            )
        )
        w_1 = image_manager.get_text_width(text_1, 1, 28)
        creat_time = TimeFormat.get_strftime(result['user']['region'], result['user']['created_at'], "%Y-%m-%d")
        image_manager.add_text(
            Text(
                text=creat_time,
                position=(472+w_1+10, 285),
                font_index=1,
                font_size=28,
                color=theme_text_color.TextThemeColor2
            )
        )

        text_2 = content_text.Activedat + ':'
        image_manager.add_text(
            Text(
                text=text_2,
                position=(472, 327),
                font_index=1,
                font_size=28,
                color=theme_text_color.TextThemeColor3
            )
        )
        w_2 = image_manager.get_text_width(text_2, 1, 28)
        active_time = TimeFormat.get_strftime(result['user']['region'], result['user']['actived_at'], "%Y-%m-%d")
        image_manager.add_text(
            Text(
                text=active_time,
                position=(472+w_2+10, 327),
                font_index=1,
                font_size=28,
                color=theme_text_color.TextThemeColor2
            )
        )
        if bot_settings.SHOW_DOG_TAG:
            if result['user']['dog_tag'] == [] or result['user']['dog_tag'] == {}:
                pass
            else:
                insignias_png_path_list = Insignias.get_insignias(
                    region_id = result['user']['region'],
                    account_id = result['user']['id'],
                    clan_id = result['clan']['id'],
                    response = result['user']['dog_tag']
                )
                for insignias_png_path in insignias_png_path_list:
                    image_manager.composite_alpha(insignias_png_path, (205, 157), resize_size=(220, 220))
        # ===================== Battles组件 =====================
        image_manager.add_text(
            Text(
                text=result['statistics']['total']['battles_count'],
                position=(239, 524),
                font_index=1,
                font_size=48,
                color=theme_text_color.TextThemeColor2
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['total']['ships_count'],
                position=(465, 605),
                font_index=1,
                font_size=24,
                color=theme_text_color.TextThemeColor2,
                align='right'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['total']['achievements_count'],
                position=(724, 605),
                font_index=1,
                font_size=24,
                color=theme_text_color.TextThemeColor2,
                align='right'
            )
        )
        # ===================== Stats组件 =====================
        i = 0
        for index in ['random', 'ranked']:
            x0 = 0
            y0 = 560
            temp_data = result['statistics']['stats'][index]
            battles_count = temp_data['battles_count']
            avg_win = temp_data['win_rate']
            avg_damage = temp_data['avg_damage']
            avg_frags = temp_data['avg_frags']
            win_rate_color = theme_rating_color.get_class_color(temp_data['win_rate_class'])
            avg_damage_color = theme_rating_color.get_class_color(temp_data['avg_damage_class'])
            avg_frags_color = theme_rating_color.get_class_color(temp_data['avg_frags_class'])
            avg_pr_color = theme_rating_color.get_class_color(temp_data['rating_class'])
            rating_text = content_text.get_rating_text(temp_data['rating_class'])
            if temp_data['rating'] == '-2':
                str_pr = '-'
            else:
                str_pr = temp_data['rating']
            image_manager.add_text(
                Text(
                    text=battles_count,
                    position=(918+x0, y0+45*i),
                    font_index=1,
                    font_size=24,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=str_pr,
                    position=(1015+x0, y0+45*i),
                    font_index=1,
                    font_size=24,
                    color=avg_pr_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_win,
                    position=(1115+x0, y0+45*i),
                    font_index=1,
                    font_size=24,
                    color=win_rate_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_damage,
                    position=(1237+x0, y0+45*i),
                    font_index=1,
                    font_size=24,
                    color=avg_damage_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_frags,
                    position=(1333+x0, y0+45*i),
                    font_index=1,
                    font_size=24,
                    color=avg_frags_color,
                    align='center'
                )
            )
            i += 1
        # ===================== Order组件 =====================
        x0 = 205
        y0 = 757
        for achv_level, achv_count in result['statistics']['achievement']['ranked'].items():
            achv_level = int(achv_level)
            if achv_count != 0:
                achv_png_path = os.path.join(ASSETS_DIR, 'components', 'achievements', 'order', f'RANK_LEAGUE_{achv_level}.png')
                image_manager.composite_alpha(achv_png_path, (x0+120*abs(achv_level-2), y0))
                image_manager.add_text(
                    Text(
                        text='x' + str(achv_count),
                        position=(x0+83+120*abs(achv_level-2), y0+63),
                        font_index=1,
                        font_size=16,
                        color=theme_text_color.TextThemeColor2  
                    )
                )
        x0 = 205
        y0 = 855
        for achv_level, achv_count in result['statistics']['achievement']['clan_battle'].items():
            achv_level = int(achv_level)
            if achv_count != 0:
                achv_png_path = os.path.join(ASSETS_DIR, 'components', 'achievements', 'order', f'CLAN_LEAGUE_{achv_level}.png')
                image_manager.composite_alpha(achv_png_path, (x0+120*abs(achv_level-4), y0))
                image_manager.add_text(
                    Text(
                        text='x' + str(achv_count),
                        position=(x0+83+120*abs(achv_level-4), y0+63),
                        font_index=1,
                        font_size=16,
                        color=theme_text_color.TextThemeColor2  
                    )
                )
        # ===================== Record组件 =====================
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_damage_dealt']['count'],
                position=(983, 760),
                font_index=1,
                font_size=34,
                color=theme_text_color.TextThemeColor2,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_damage_dealt']['tier'] + '  ' + result['statistics']['record']['max_damage_dealt']['name'],
                position=(983, 800),
                font_index=1,
                font_size=18,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_frags']['count'],
                position=(1286, 760),
                font_index=1,
                font_size=34,
                color=theme_text_color.TextThemeColor2,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_frags']['tier'] + '  ' + result['statistics']['record']['max_frags']['name'],
                position=(1286, 800),
                font_index=1,
                font_size=18,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_exp']['count'],
                position=(954, 860),
                font_index=1,
                font_size=34,
                color=theme_text_color.TextThemeColor2,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_exp']['tier'] + '  ' + result['statistics']['record']['max_exp']['name'],
                position=(954, 900),
                font_index=1,
                font_size=18,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_planes_killed']['count'],
                position=(1254, 860),
                font_index=1,
                font_size=34,
                color=theme_text_color.TextThemeColor2,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=result['statistics']['record']['max_planes_killed']['tier'] + '  ' + result['statistics']['record']['max_planes_killed']['name'],
                position=(1254, 900),
                font_index=1,
                font_size=18,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        # 提交操作并返回渲染好的图片
        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result