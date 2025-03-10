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
    user: KokomiUser
) -> dict:
    path = '/r/user/account/'
    params = {
        'region': Utils.get_region_by_id(user.bind.region_id),
        'account_id': user.bind.account_id,
        'game_type': 'overall',
        'language': Utils.get_language(user.local.language)
    }
    if user.local.algorithm:
        params['algo_type'] = user.local.algorithm
    
    if bot_settings.USE_MOCK:
        result = Mock.read_data('rank_user.json')
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
    width, height = 2428, 3152
    # 背景颜色（RGB）
    background_color = Picture.hex_to_rgb(user.local.background, 0)
    # 创建画布
    canvas = Image.new("RGBA", (width, height), background_color)
    # TODO: 叠加主题背景

    # 叠加图片主体
    content_png_path = os.path.join(ASSETS_DIR, 'content', user.local.content, user.local.language, 'rank_user.png')
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

    # Header用户信息条
    header_png_path = os.path.join(ASSETS_DIR, r'components\header', f'{user.local.content}.png')
    header_png = Image.open(header_png_path)
    res_img.alpha_composite(header_png, (97, 130))
    del header_png
    text_list.append(
        Text_Data(
            xy=(172, 156),
            text=result['user']['name'],
            fill=theme_text_color.TextThemeColor2,
            font_index=1,
            font_size=100
        )
    )
    fontStyle = font_manager.get_font(1,40)
    region = Utils.get_region_by_id(result['user']['region'])
    region = region.upper()
    w = Picture.x_coord(region, fontStyle)
    text_list.append(
        Text_Data(
            xy=(244-w/2, 272),
            text=region,
            fill=theme_text_color.TextThemeColor4,
            font_index=1,
            font_size=40
        )
    )
    w = Picture.x_coord(str(result['user']['id']), fontStyle)
    text_list.append(
        Text_Data(
            xy=(482-w/2, 272),
            text=str(result['user']['id']),
            fill=theme_text_color.TextThemeColor4,
            font_index=1,
            font_size=40
        )
    )
    fontStyle = font_manager.get_font(1,55)
    if result['clan']['id'] != None:
        tag = '['+str(result['clan']['tag'])+']'
    else:
        tag = 'None'
    clan_league_color = GameData.clan_league_color.get(result['clan']['league'])
    text_1 = content_text.UserClan + ':'
    w_1 = Picture.x_coord(text_1, fontStyle)
    text_list.append(
        Text_Data(
            xy=(169, 358),
            text=text_1,
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=55
        )
    )
    text_list.append(
        Text_Data(
            xy=(169+w_1+30, 358),
            text=tag,
            fill=clan_league_color,
            font_index=1,
            font_size=55
        )
    )
    text_2 = content_text.Createdat + ':'
    w_2 = Picture.x_coord(text_2, fontStyle)
    text_list.append(
        Text_Data(
            xy=(169, 448),
            text=text_2,
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=55
        )
    )
    creat_time = TimeFormat.get_strftime(result['user']['region'], result['user']['crated_at'], "%Y-%m-%d")
    text_list.append(
        Text_Data(
            xy=(169+w_2+30, 448),
            text=creat_time,
            fill=theme_text_color.TextThemeColor2,
            font_index=1,
            font_size=55
        )
    )
    # 排行榜信息
    text_list.append(
        Text_Data(
            xy=(1379, 235+462),
            text=result['statistics']['ship_data']['limit'],
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=50
        )
    )
    text_list.append(
        Text_Data(
            xy=(1739, 697),
            text=result['statistics']['ship_data']['update'],
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=50
        )
    )
    text_list.append(
        Text_Data(
            xy=(2099, 697),
            text=result['statistics']['ship_data']['region'],
            fill=theme_text_color.TextThemeColor3,
            font_index=1,
            font_size=50
        )
    )
    # 船只信息条
    ship_name = result['statistics']['ship_info']['name']
    ship_tier = result['statistics']['ship_info']['tier']
    ship_index = result['statistics']['ship_info']['index']
    ship_nation = result['statistics']['ship_info']['nation']
    ship_type = result['statistics']['ship_info']['type']
    premium = result['statistics']['ship_info']['premium']
    special = result['statistics']['ship_info']['special']
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
            xy=(all_len/2+1214-w, 839),
            text=ship_name_str,
            fill=(0,0,0),
            font_index=1,
            font_size=70
        )
    )
    nation_png = Image.open(nation_png_path)
    nation_png = nation_png.resize((108,108))
    x1 = int(1214-all_len/2)
    y1 = 817
    res_img.alpha_composite(nation_png,(x1,y1))
    type_png = Image.open(type_png_path)
    x1 = int(1214-all_len/2+180)
    y1 = 830
    res_img.alpha_composite(type_png,(x1,y1))
    fontStyle = font_manager.get_font(1,30)
    # 用户总体数据页
    rating_class = result['statistics']['overall']['rating_class']
    rating_png_path = os.path.join(ASSETS_DIR, r'content\rating\pr', user.local.language, '{}.png'.format(rating_class))
    rating_png = Image.open(rating_png_path)
    res_img.paste(rating_png, (132, 627+375))
    del rating_png
    if bot_settings.SHOW_DOG_TAG:
        if result['user']['dog_tag'] == [] or result['user']['dog_tag'] == {}:
            pass
        else:
            res_img = Insignias.add_user_insignias(
                img = res_img,
                region_id = result['user']['region'],
                account_id = result['user']['id'],
                clan_id = result['clan']['id'],
                response = result['user']['dog_tag']
            )
    fontStyle = font_manager.get_font(1,35)
    if result['statistics']['overall']['rating_class'] == 9:
        rating_next_text = content_text.RatingNextText_2 + ':    +' + str(result['statistics']['overall']['rating_next'])
    else:
        rating_next_text = content_text.RatingNextText_1 + ':    +' + str(result['statistics']['overall']['rating_next'])
    _, rating_next_len = content_text.get_rating_text(result['statistics']['overall']['rating_class'], True)
    text_list.append(
        Text_Data(
            xy=(132+rating_next_len+10, 690+375),
            text=rating_next_text,
            fill=(255, 255, 255),
            font_index=1,
            font_size=35
        )
    )
    str_pr = result['statistics']['overall']['rating']
    fontStyle = font_manager.get_font(1,80)
    w = Picture.x_coord(str_pr, fontStyle)
    text_list.append(
        Text_Data(
            xy=(2284-w, 642+375),
            text=str_pr,
            fill=(255, 255, 255),
            font_index=1,
            font_size=80
        )
    )
    x0 = 324
    y0 = 860+375
    temp_data: UserOverallDict = result['statistics']['overall']
    battles_count = temp_data['battles_count']
    avg_win = temp_data['win_rate']
    avg_damage = temp_data['avg_damage']
    avg_frag = temp_data['avg_frags']
    avg_xp = temp_data['avg_exp']
    win_rate_color = theme_rating_color.get_class_color(temp_data['win_rate_class'])
    avg_damage_color = theme_rating_color.get_class_color(temp_data['avg_damage_class'])
    avg_frags_color = theme_rating_color.get_class_color(temp_data['avg_frags_class'])

    w = Picture.x_coord(battles_count, fontStyle)
    text_list.append(
        Text_Data(
            xy=(x0+446*0-w/2, y0),
            text=battles_count,
            fill=theme_text_color.TextThemeColor2,
            font_index=1,
            font_size=80
        )
    )
    w = Picture.x_coord(avg_win, fontStyle)
    text_list.append(
        Text_Data(
            xy=(x0+446*1-w/2, y0),
            text=avg_win,
            fill=win_rate_color,
            font_index=1,
            font_size=80
        )
    )
    w = Picture.x_coord(avg_damage, fontStyle)
    text_list.append(
        Text_Data(
            xy=(x0+446*2-w/2, y0),
            text=avg_damage,
            fill=avg_damage_color,
            font_index=1,
            font_size=80
        )
    )
    w = Picture.x_coord(avg_frag, fontStyle)
    text_list.append(
        Text_Data(
            xy=(x0+446*3-w/2, y0),
            text=avg_frag,
            fill=avg_frags_color,
            font_index=1,
            font_size=80
        )
    )
    w = Picture.x_coord(avg_xp, fontStyle)
    text_list.append(
        Text_Data(
            xy=(x0+446*4-w/2, y0),
            text=avg_xp,
            fill=theme_text_color.TextThemeColor2,
            font_index=1,
            font_size=80
        )
    )
    # 排行榜信息
    fontStyle = font_manager.get_font(2, 75)
    w = Picture.x_coord(str(result['statistics']['rank_data']['rank']), fontStyle)
    text_list.append(
        Text_Data(
            xy=(660-w/2, 1549),
            text=str(result['statistics']['rank_data']['rank']),
            fill=theme_text_color.TextThemeColor1,
            font_index=2,
            font_size=75
        )
    )
    w = Picture.x_coord(result['statistics']['rank_data']['percentage'], fontStyle)
    text_list.append(
        Text_Data(
            xy=(500-w/2, 1648),
            text=result['statistics']['rank_data']['percentage'],
            fill=theme_text_color.TextThemeColor1,
            font_index=2,
            font_size=75
        )
    )
    # 排行榜信息
    fontStyle = font_manager.get_font(2, 65)
    w = Picture.x_coord(result['statistics']['rank_data']['sum'], fontStyle)
    text_list.append(
        Text_Data(
            xy=(780-w, 1753),
            text=result['statistics']['rank_data']['sum'],
            fill=theme_text_color.TextThemeColor1,
            font_index=2,
            font_size=65
        )
    )
    max_num = max(result['statistics']['rank_data']['distribution']['bin_count'].values())
    user_bin = result['statistics']['rank_data']['distribution']['user_bin']
    max_index = (int(max_num/100) + 1)*100
    fontStyle = font_manager.get_font(1, 35)
    i = 0
    for bin, count in result['statistics']['rank_data']['distribution']['bin_count'].items():
        
        pic_len = max(270-count/max_index*270, 10)
        x1 = 1050+44*i
        y1 = 1582+int(pic_len)
        x2 = 1090+44*i
        y2 = 1852
        if i == 0:
            text_list.append(
                Text_Data(
                    xy=(1050, y2+5),
                    text='0',
                    fill=theme_text_color.TextThemeColor3,
                    font_index=1,
                    font_size=15
                )
            )
        if int(bin) >= 1000:
            text_list.append(
                Text_Data(
                    xy=(1075+44*i, y2+5),
                    text=bin,
                    fill=theme_text_color.TextThemeColor3,
                    font_index=1,
                    font_size=15
                )
            )
        else:
            text_list.append(
                Text_Data(
                    xy=(1080+44*i, y2+5),
                    text=bin,
                    fill=theme_text_color.TextThemeColor3,
                    font_index=1,
                    font_size=15
                )
            )
        if count != 0:
            if bin != str(int(user_bin)+200):
                box_list.append(
                    Box_Data(
                        xy=((x1, y1), (x2, y2)),
                        fill=(137, 207, 240)
                    )
                )
            else:
                box_list.append(
                    Box_Data(
                        xy=((x1, y1), (x2, y2)),
                        fill=(254, 77, 50)
                    )
                )
                w = Picture.x_coord('▼', fontStyle)
                text_list.append(
                    Text_Data(
                        xy=(1070-w/2+44*i, y1-40),
                        text='▼',
                        fill=(254, 77, 50),
                        font_index=1,
                        font_size=35
                    )
                )
        i += 1
    # 排行榜
    fontStyle = font_manager.get_font(1, 30)
    i = 0
    for index in result['statistics']['leaderboard']:
        y0 = 568+1487
        if index['is_user'] == '1':
            bg_png_path = os.path.join(ASSETS_DIR, r'components\other\red.png')
            bg = Image.open(bg_png_path)
            bg = bg.resize((2234, 55))
            x1 = 97
            y1 = 2042 + 55*i
            res_img.alpha_composite(bg,(x1,y1))
        rank_num = index['rank']
        if int(rank_num) > 9999:
            w = Picture.x_coord(rank_num, font_manager.get_font(1, 20))
            text_list.append(
                Text_Data(
                    xy=(136-w/2, y0 + 55*i + 3),
                    text=rank_num,
                    fill=(0, 0, 0),
                    font_index=1,
                    font_size=20
                )
            )
        else:
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
    footer_hight = 3022
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


            


