import os
from PIL import Image
from typing_extensions import TypedDict

from ..config import ASSETS_DIR, bot_settings
from ..logs import logging
from ..api import BaseAPI, Mock
from ..logs import ExceptionLogger
from ..language import Content
from ..common import (
    Utils, GameData, ThemeTextColor, ThemeRatingColor,
    ThemeClanColor, ThemeRegionColor, TimeFormat, ReadVersionFile
)
from ..image import (
    Text_Data, Box_Data, Picture, Insignias, font_manager
)
from ..schemas import (
    KokomiUser, UserBasicDict, UserClanDict, UserOverallDict
)


class OverallDict(TypedDict):
    overall: UserOverallDict
    ship_data: dict
    ship_info: dict
    rank_data: dict
    leaderboard: list

class UserBaseResult(TypedDict):
    user: UserBasicDict
    clan: UserClanDict
    statistics: OverallDict


@ExceptionLogger.handle_program_exception_async
async def main(
    user: KokomiUser,
    region_idx: int,
    ship_id: int
) -> dict:
    path = f'/api/v1/robot/leaderboard/page/{region_idx}/{ship_id}/'
    params = {
        'language': Utils.get_language(user.local.language),
        'page_idx': 1,
        'page_size': 50
    }
    if user.local.algorithm:
        params['algo_type'] = user.local.algorithm
    
    if bot_settings.USE_MOCK:
        result = Mock.read_data('rank_page.json')
        logging.debug('Using MOCK, skip network requests')
    else:
        result = await BaseAPI.get(
            path=path,
            params=params
        )
    if result['code'] != 1000:
        logging.error(f"API request failed, Error: {result['message']}")
        return result
    res_img = get_png(
        user=user,
        result=result['data']
    )
    result = Picture.return_img(img=res_img)
    del res_img
    return result

@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(
    user: KokomiUser,
    result: UserBaseResult
) -> str:
    # 画布宽度和高度
    width, height = 2428, 3800
    # 背景颜色（RGB）
    background_color = Picture.hex_to_rgb(user.local.background, 0)
    # 创建画布
    canvas = Image.new("RGBA", (width, height), background_color)
    # TODO: 叠加主题背景

    # 叠加图片主体
    content_png_path = os.path.join(ASSETS_DIR, 'content', user.local.content, user.local.language, 'rank_page.png')
    content_png = Image.open(content_png_path)
    canvas.alpha_composite(content_png, (0, 0))
    del content_png
    # TODO: 叠加图片主题图片
    
    res_img = canvas
    del canvas
    # 获取语言对应的文本文字
    content_text = Content.get_content_language(user.local.language)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 获取不同主题的评分颜色
    theme_rating_color = ThemeRatingColor(user.local.content)
    # 获取不同主题的评分颜色
    theme_clan_color = ThemeClanColor(user.local.content)
    # 获取不同主题的评分颜色
    theme_region_color = ThemeRegionColor(user.local.content)
    # 需要叠加的 文字/矩形
    text_list = []
    box_list = []

    # 排行榜信息
    text_list.append(
        Text_Data(
            xy=(1379, 235),
            text=result['ship_data']['limit'],
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=50
        )
    )
    text_list.append(
        Text_Data(
            xy=(1739, 235),
            text=result['ship_data']['update'],
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=50
        )
    )
    text_list.append(
        Text_Data(
            xy=(2099, 235),
            text=result['ship_data']['region'],
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=50
        )
    )
    # 船只信息条
    ship_name = result['ship_info']['name']
    ship_tier = result['ship_info']['tier']
    ship_index = result['ship_info']['index']
    ship_nation = result['ship_info']['nation']
    ship_type = result['ship_info']['type']
    premium = result['ship_info']['premium']
    special = result['ship_info']['special']
    ship_name_str = GameData.tier_dict[ship_tier] + '    ' + ship_name
    nation_png_path = os.path.join(ASSETS_DIR, r'components\ships\nation', f'flag_{ship_index}.png')
    if os.path.exists(nation_png_path) is False:
        nation_png_path = os.path.join(ASSETS_DIR, r'components\ships\nation', f'flag_{ship_nation}.png')
    if premium:
        type_png_path = os.path.join(ASSETS_DIR, r'components\ships\type_icon', f'{ship_type}_Premium.png')
    elif special:
        type_png_path = os.path.join(ASSETS_DIR, r'components\ships\type_icon', f'{ship_type}_Special.png')
    else:
        type_png_path = os.path.join(ASSETS_DIR, r'components\ships\type_icon', f'{ship_type}_Elite.png')
    fontStyle = font_manager.get_font(1,70)
    w = Picture.x_coord(ship_name_str, fontStyle)
    all_len = 320+w
    text_list.append(
        Text_Data(
            xy=(all_len/2+1214-w, 377),
            text=ship_name_str,
            fill=(0,0,0),
            font_index=1,
            font_size=70
        )
    )
    nation_png = Image.open(nation_png_path)
    nation_png = nation_png.resize((108,108))
    x1 = int(1214-all_len/2)
    y1 = 355
    res_img.alpha_composite(nation_png,(x1,y1))
    type_png = Image.open(type_png_path)
    x1 = int(1214-all_len/2+180)
    y1 = 368
    res_img.alpha_composite(type_png,(x1,y1))
    fontStyle = font_manager.get_font(1,30)
    # 排行榜
    fontStyle = font_manager.get_font(1, 30)
    i = 0
    for index in result['leaderboard']:
        if i >= 50:
            break
        y0 = 568
        rank_num = index['rank']
        w = Picture.x_coord(rank_num, fontStyle)
        text_list.append(
            Text_Data(
                xy=(136-w/2, y0 + 55*i),
                text=rank_num,
                fill=(0, 0, 0),
                font_index=1,
                font_size=30
            )
        )
        region_id = eval(index['region_id'])
        region = index['region']
        region_color = theme_region_color.get_color(region_id-1)
        battle_type_color = theme_rating_color.get_class_color(index['battle_type_class'])
        rating_color = theme_rating_color.get_class_color(index['rating_class'])
        win_rate_color = theme_rating_color.get_class_color(index['win_rate_class'])
        avg_damage_color = theme_rating_color.get_class_color(index['avg_dmg_class'])
        avg_frags_color = theme_rating_color.get_class_color(index['avg_frags_class'])
        w = Picture.x_coord(region, fontStyle)
        text_list.append(
            Text_Data(
                xy=(225-w/2, y0 + 55*i),
                text=region,
                fill=region_color,
                font_index=1,
                font_size=30
            )
        )
        if index['clan_tag'] != 'nan':
            clan_name = '[' + index['clan_tag'] + ']'
            clan_tag_color = theme_clan_color.get_color(index['clan_tag_class'])
            w = Picture.x_coord(clan_name, fontStyle)
            text_list.append(
                Text_Data(
                    xy=(288, y0 + 55*i),
                    text=clan_name,
                    fill=clan_tag_color,
                    font_index=1,
                    font_size=30
                )
            )
            user_name = index['user_name']
            is_change = False
            while len(user_name.encode('utf-8')) > 25 - len(clan_name):
                if not user_name:
                    break
                user_name = user_name[:-1]  # 删除最后一个字符
                is_change = True
            if is_change:
                user_name = user_name + '...'
            text_list.append(
                Text_Data(
                    xy=(288+w+5, y0 + 55*i),
                    text=user_name,
                    fill=(0, 0, 0),
                    font_index=1,
                    font_size=30
                )
            )
        else:
            user_name = index['user_name']
            is_change = False
            while len(user_name.encode('utf-8')) > 25:
                if not user_name:
                    break
                user_name = user_name[:-1]  # 删除最后一个字符
                is_change = True
            if is_change:
                user_name = user_name + '...'
            text_list.append(
                Text_Data(
                    xy=(288, y0 + 55*i),
                    text=user_name,
                    fill=(0, 0, 0),
                    font_index=1,
                    font_size=30
                )
            )
        w = Picture.x_coord(index['battles_count'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(848-w/2, y0 + 55*i),
                text=index['battles_count'],
                fill=(0, 0, 0),
                font_index=1,
                font_size=30
            )
        )
        rating_value = index['rating']
        w = Picture.x_coord(rating_value, fontStyle)
        text_list.append(
            Text_Data(
                xy=(981-w/2, y0 + 55*i),
                text=rating_value,
                fill=rating_color,
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['rating_info'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(1156-w/2, y0 + 55*i),
                text=index['rating_info'],
                fill=(0, 0, 0),
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['win_rate'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(1327-w/2, y0 + 55*i),
                text=index['win_rate'],
                fill=win_rate_color,
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['battle_type'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(1476-w/2, y0 + 55*i),
                text=index['battle_type'],
                fill=battle_type_color,
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['avg_dmg'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(1645-w/2, y0 + 55*i),
                text=index['avg_dmg'],
                fill=avg_damage_color,
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['avg_frags'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(1804-w/2, y0 + 55*i),
                text=index['avg_frags'],
                fill=avg_frags_color,
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['avg_exp'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(1943-w/2, y0 + 55*i),
                text=index['avg_exp'],
                fill=(0, 0, 0),
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['max_dmg'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(2102-w/2, y0 + 55*i),
                text=index['max_dmg'],
                fill=(0, 0, 0),
                font_index=1,
                font_size=30
            )
        )
        w = Picture.x_coord(index['max_exp'], fontStyle)
        text_list.append(
            Text_Data(
                xy=(2261-w/2, y0 + 55*i),
                text=index['max_exp'],
                fill=(0, 0, 0),
                font_index=1,
                font_size=30
            )
        )
        i += 1
    # Footer底部信息条
    footer_hight = 3670
    footer_png_path = os.path.join(ASSETS_DIR, r'components\footer', f'{user.local.content}.png')
    footer_png = Image.open(footer_png_path)
    res_img.alpha_composite(footer_png, (97, footer_hight))
    del footer_png
    text_list.append(
        Text_Data(
            xy=(145, footer_hight + 23),
            text=bot_settings.BOT_INFO,
            fill=theme_text_color.TextThemeColor4,
            font_index=1,
            font_size=50
        )
    )
    text_list.append(
        Text_Data(
            xy=(1217, footer_hight + 23),
            text=TimeFormat.get_datetime_now(),
            fill=theme_text_color.TextThemeColor4,
            font_index=1,
            font_size=50
        )
    )
    text_list.append(
        Text_Data(
            xy=(2015, footer_hight + 23),
            text=ReadVersionFile.read_version(),
            fill=theme_text_color.TextThemeColor4,
            font_index=1,
            font_size=50
        )
    )
    # 完成文字和矩形的叠加
    res_img = Picture.add_box(box_list, res_img)
    res_img = Picture.add_text(text_list, res_img)
    # res_img_size = res_img.size
    # 缩小图片大小
    # res_img = res_img.resize(
    #     (
    #         int(res_img_size[0]*0.5), 
    #         int(res_img_size[1]*0.5)
    #     )
    # )
    return res_img


            


