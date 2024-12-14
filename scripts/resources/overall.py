import os
import time
from PIL import Image
from typing_extensions import TypedDict

from scripts.config import ASSETS_DIR, bot_settings
from scripts.common import font_manager
from scripts.logs import logging
from scripts.api import BaseAPI
from scripts.logs import ExceptionLogger
from scripts.language import ContentText_CN, ContentText_EN, ContentText_JA
from scripts.common import (
    Text_Data, Box_Data, Picture, Utils, GameData, 
    ThemeTextColor, ThemeRatingColor, TimeFormat,
    Insignias
)
from scripts.schemas import (
    KokomiUser, UserBasicDict, UserClanDict, UserOverallDict,
    ResultShipTypeDict, ResultBattleTypeDict
)


class OverallDict(TypedDict):
    overall: UserOverallDict
    battle_type: ResultBattleTypeDict
    ship_type: ResultShipTypeDict
    chart_data: dict

class UserBaseResult(TypedDict):
    user: UserBasicDict
    clan: UserClanDict
    statistics: OverallDict


@ExceptionLogger.handle_program_exception_async
async def main(
    user: KokomiUser
) -> dict:
    path = '/r/account/'
    params = {
        'region': Utils.get_region_by_id(user.bind.region_id),
        'account_id': user.bind.account_id,
        'game_type': 'overall',
        'language': Utils.get_language(user.local.language)
    }
    if user.local.algorithm:
        params['algo_type'] = user.local.algorithm
    st = time.time()
    result = await BaseAPI.get(
        path=path,
        params=params
    )
    et = time.time()
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
    width, height = 2428, 3350
    # 背景颜色（RGB）
    background_color = Picture.hex_to_rgb(user.local.background, 0)
    # 创建画布
    canvas = Image.new("RGBA", (width, height), background_color)
    # TODO: 叠加主题背景

    # 叠加图片主体
    content_png_path = os.path.join(ASSETS_DIR, 'content', user.local.content, user.local.language, 'basic.png')
    content_png = Image.open(content_png_path)
    canvas.alpha_composite(content_png, (0, 0))
    # TODO: 叠加图片主题图片
    
    res_img = canvas
    del canvas
    # 获取语言对应的文本文字
    if user.local.language == 'cn':
        content_text = ContentText_CN
    elif user.local.language == 'en':
        content_text = ContentText_EN
    elif user.local.language == 'ja':
        content_text = ContentText_JA
    else:
        # 必须确保后续程序执行中不会遇到不支持的语言
        raise ValueError("Invaild language.")
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 获取不同主题的评分颜色
    theme_rating_color = ThemeRatingColor(user.local.content)
    # 需要叠加的 文字/矩形
    text_list = []
    box_list = []

    # Header用户信息条
    text_list.append(
        Text_Data(
            xy=(172, 161),
            text=result['user']['name'],
            fill=theme_text_color.TextThemeColor2,
            font_index=1,
            font_size=100
        )
    )
    region = Utils.get_region_by_id(result['user']['id'])
    text_list.append(
        Text_Data(
            xy=(199, 275),
            text=f"{region} -- {result['user']['id']}",
            fill=(163, 163, 163),
            font_index=1,
            font_size=45
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
    # 用户总体数据页
    rating_class = result['statistics']['overall']['rating_class']
    rating_png_path = os.path.join(ASSETS_DIR, r'content\rating\pr', user.local.language, '{}.png'.format(rating_class))
    rating_png = Image.open(rating_png_path)
    res_img.paste(rating_png, (132, 627))
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
            xy=(132+rating_next_len+10, 690),
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
            xy=(2284-w, 642),
            text=str_pr,
            fill=(255, 255, 255),
            font_index=1,
            font_size=80
        )
    )
    x0 = 324
    y0 = 860
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
    # 战斗类型数据页
    i = 0
    for index in ['pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']:
        x0 = 0
        y0 = 1258
        temp_data: UserOverallDict = result['statistics']['battle_type'][index]
        battles_count = temp_data['battles_count']
        avg_win = temp_data['win_rate']
        avg_damage = temp_data['avg_damage']
        avg_frag = temp_data['avg_frags']
        avg_xp = temp_data['avg_exp']
        win_rate_color = theme_rating_color.get_class_color(temp_data['win_rate_class'])
        avg_damage_color = theme_rating_color.get_class_color(temp_data['avg_damage_class'])
        avg_frags_color = theme_rating_color.get_class_color(temp_data['avg_frags_class'])
        avg_pr_color = theme_rating_color.get_class_color(temp_data['rating_class'])
        rating_text = content_text.get_rating_text(temp_data['rating_class'])
        if temp_data['rating'] == '-2':
            str_pr = '-'
        else:
            if user.local.language == 'cn':
                str_pr = rating_text + '(+'+str(temp_data['rating_next'])+')'
            else:
                str_pr = '■ ' + temp_data['rating']
        fontStyle = font_manager.get_font(1,55)
        w = Picture.x_coord(battles_count, fontStyle)
        text_list.append(
            Text_Data(
                xy=(588-w/2+x0, y0+90*i),
                text=battles_count,
                fill=theme_text_color.TextThemeColor2,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(str_pr, fontStyle)
        text_list.append(
            Text_Data(
                xy=(955-w/2+x0, y0+90*i),
                text=str_pr,
                fill=avg_pr_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_win, fontStyle)
        text_list.append(
            Text_Data(
                xy=(1307-w/2+x0, y0+90*i),
                text=avg_win,
                fill=win_rate_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_damage, fontStyle)
        text_list.append(
            Text_Data(
                xy=(1613-w/2+x0, y0+90*i),
                text=avg_damage,
                fill=avg_damage_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_frag, fontStyle)
        text_list.append(
            Text_Data(
                xy=(1909-w/2+x0, y0+90*i),
                text=avg_frag,
                fill=avg_frags_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_xp, fontStyle)
        text_list.append(
            Text_Data(
                xy=(2177-w/2+x0, y0+90*i),
                text=avg_xp,
                fill=theme_text_color.TextThemeColor2,
                font_index=1,
                font_size=55
            )
        )
        i += 1
    # 船只类型数据页
    i = 0
    for index in ['AirCarrier', 'Battleship', 'Cruiser', 'Destroyer', 'Submarine']:
        x0 = 0
        y0 = 1855
        temp_data: UserOverallDict = result['statistics']['ship_type'][index]
        battles_count = temp_data['battles_count']
        avg_win = temp_data['win_rate']
        avg_damage = temp_data['avg_damage']
        avg_frag = temp_data['avg_frags']
        avg_xp = temp_data['avg_exp']
        win_rate_color = theme_rating_color.get_class_color(temp_data['win_rate_class'])
        avg_damage_color = theme_rating_color.get_class_color(temp_data['avg_damage_class'])
        avg_frags_color = theme_rating_color.get_class_color(temp_data['avg_frags_class'])
        avg_pr_color = theme_rating_color.get_class_color(temp_data['rating_class'])
        if temp_data['rating'] == '-2':
            str_pr = '-'
        else:
            if user.local.language == 'cn':
                str_pr = rating_text + '(+'+str(temp_data['rating_next'])+')'
            else:
                str_pr = '■ ' + temp_data['rating']
        fontStyle = font_manager.get_font(1,55)
        w = Picture.x_coord(battles_count, fontStyle)
        text_list.append(
            Text_Data(
                xy=(588-w/2+x0, y0+90*i),
                text=battles_count,
                fill=theme_text_color.TextThemeColor2,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(str_pr, fontStyle)
        text_list.append(
            Text_Data(
                xy=(955-w/2+x0, y0+90*i),
                text=str_pr,
                fill=avg_pr_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_win, fontStyle)
        text_list.append(
            Text_Data(
                xy=(1307-w/2+x0, y0+90*i),
                text=avg_win,
                fill=win_rate_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_damage, fontStyle)
        text_list.append(
            Text_Data(
                xy=(1613-w/2+x0, y0+90*i),
                text=avg_damage,
                fill=avg_damage_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_frag, fontStyle)
        text_list.append(
            Text_Data(
                xy=(1909-w/2+x0, y0+90*i),
                text=avg_frag,
                fill=avg_frags_color,
                font_index=1,
                font_size=55
            )
        )
        w = Picture.x_coord(avg_xp, fontStyle)
        text_list.append(
            Text_Data(
                xy=(2177-w/2+x0, y0+90*i),
                text=avg_xp,
                fill=theme_text_color.TextThemeColor2,
                font_index=1,
                font_size=55
            )
        )
        i += 1
    # 条形图数据
    max_num = 0
    num_list = []
    for _, num in result['statistics']['chart_data'].items():
        if num >= max_num:
            max_num = num
        num_list.append(num)
    max_index = (int(max_num/100) + 1)*100
    i = 0
    fontStyle = font_manager.get_font(1,35)
    for index in num_list:
        pic_len = 500-index/max_index*500
        x1 = 272+129*i
        y1 = 2544+int(pic_len)
        x2 = 350+129*i
        y2 = 3048
        box_list.append(
            Box_Data(
                xy=((x1, y1), (x2, y2)),
                fill=(137, 207, 240)
            )
        )
        w = Picture.x_coord(str(index), fontStyle)
        text_list.append(
            Text_Data(
                xy=(311-w/2+129*i, y1-40),
                text=str(index),
                fill=theme_text_color.TextThemeColor2,
                font_index=1,
                font_size=35
            )
        )
        i += 1
    # 底部信息条
    fontStyle = font_manager.get_font(1,55)
    png_create_time = TimeFormat.get_datetime_now()
    text_list.append(
        Text_Data(
            xy=(97+20, 3214),
            text='Creation time: '+png_create_time,
            fill=theme_text_color.TextThemeColor5,
            font_index=1,
            font_size=55
        )
    )
    w = Picture.x_coord('Powered by '+bot_settings.BOT_INFO, fontStyle)
    text_list.append(
        Text_Data(
            xy=(2331-20-w, 3214),
            text='Powered by '+bot_settings.BOT_INFO,
            fill=theme_text_color.TextThemeColor5,
            font_index=1,
            font_size=55
        )
    )
    # 完成文字和矩形的叠加
    res_img = Picture.add_box(box_list, res_img)
    res_img = Picture.add_text(text_list, res_img)
    res_img_size = res_img.size
    # 缩小图片大小
    res_img = res_img.resize(
        (
            int(res_img_size[0]*0.5), 
            int(res_img_size[1]*0.5)
        )
    )
    return res_img


            


