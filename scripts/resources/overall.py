import os
import time
from PIL import Image
from typing_extensions import TypedDict

from scripts.config import ASSETS_DIR, bot_settings
from scripts.api import BaseAPI
from scripts.logs import ExceptionLogger
from scripts.language import ContentText_CN, ContentText_EN, ContentText_JA
from scripts.common import Text_Data, Box_Data, Picture, Utils
from scripts.schemas import (
    PlatformDict, UserInfoDict, UserBindDict, UserLocalDict,
    UserBasicDict, UserClanDict, UserOverallDict,
    ResultShipTypeDict, ResultBattleTypeDict
)


class OverallDict(TypedDict):
    user: UserBasicDict
    clan: UserClanDict
    overall: UserOverallDict
    battle_type: ResultBattleTypeDict
    ship_type: ResultShipTypeDict
    chart_data: dict


@ExceptionLogger.handle_program_exception_async
async def main(
    platform: PlatformDict,
    user_info: UserInfoDict,
    user_bind: UserBindDict,
    user_local: UserLocalDict
) -> dict:
    path = '/r/account/'
    params = {
        'region': Utils.get_region_by_id(user_bind['region_id']),
        'account_id': user_bind['account_id'],
        'game_type': 'overall',
        'language': Utils.get_language(user_bind['language'])
    }
    if user_bind['algorithm']:
        params['algo_type'] = user_bind['algorithm']
    result = await BaseAPI.get(
        path=path,
        params=params
    )
    if result['code'] != 1000:
        return result
    res_img = get_png(
        result=result['data'],
        platform=platform,
        user_info=user_info,
        user_bind=user_bind,
        user_local=user_local
    )
    result = Picture.return_img(img=res_img)
    del res_img
    return result


def get_png(
    result: OverallDict,
    platform: PlatformDict,
    user_info: UserInfoDict,
    user_bind: UserBindDict,
    user_local: UserLocalDict
) -> str:
    # 画布宽度和高度
    width, height = 2428, 3350
    # 背景颜色（RGB）
    background_color = Picture.hex_to_rgb(user_local['background'], 100) # 红色
    # 创建画布
    canvas = Image.new("RGBA", (width, height), background_color)
    # TODO: 叠加主题背景

    # 叠加图片主体
    content_png_path = os.path.join(ASSETS_DIR, 'content', user_local['content'], user_bind['language'], 'basic.png')
    content_png = Image.open(content_png_path)
    canvas.alpha_composite(content_png, (0, 0))
    # TODO: 叠加图片主题图片
    
    res_img = canvas
    del canvas
    # 叠加 文字/矩形
    text_list = []
    box_list = []
    text_list.append(
        Text_Data(
            xy=(172, 161),
            text=result['user']['name'],
            fill=(0, 0, 0),
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
    fontStyle = fonts.data[1][55]
    if result['data']['clans']['clan_tag'] != 'None':
        tag = '['+str(result['data']['clans']['clan_tag'])+']'
    else:
        tag = str(result['data']['clans']['clan_tag'])
    tag_color = Picture.hex_to_rgb(result['data']['clans']['clan_color'])
    header_dict = {
        'cn': [
            {'title': ContentText_CN.UserClan + ':', 'left': 169, 'top': 358},
            {'title': ContentText_CN.Createdat + ':', 'left': 169, 'top': 448}
        ],
        'en': [
            {'title': ContentText_EN.UserClan + ':', 'left': 169, 'top': 358},
            {'title': ContentText_EN.Createdat + ':', 'left': 169, 'top': 448}
        ],
        'ja': [
            {'title': ContentText_JA.UserClan + ':', 'left': 169, 'top': 358},
            {'title': ContentText_JA.Createdat + ':', 'left': 169, 'top': 448}
        ]
    }
    header_data = header_dict[user_bind['language']]
    text_1 = header_data[0]['title']
    w_1 = Picture.x_coord(text_1, fontStyle)
    text_list.append(
        Text_Data(
            xy=(header_data[0]['left'], header_data[0]['top']),
            text=text_1,
            fill=(72, 72, 72),
            font_index=1,
            font_size=55
        )
    )
    text_list.append(
        Text_Data(
            xy=(header_data[0]['left']+w_1+30, header_data[0]['top']),
            text=tag,
            fill=tag_color,
            font_index=1,
            font_size=55
        )
    )
    text_2 = header_data[1]['title']
    w_2 = Picture.x_coord(text_2, fontStyle)
    text_list.append(
        Text_Data(
            xy=(header_data[1]['left'], header_data[1]['top']),
            text=text_2,
            fill=(72, 72, 72),
            font_index=1,
            font_size=55
        )
    )
    creat_time = time.strftime("%Y-%m-%d", time.localtime(result['user']['crated_at']))
    text_list.append(
        Text_Data(
            xy=(header_data[1]['left']+w_2+30, header_data[1]['top']),
            text=creat_time,
            fill=(0,0,0),
            font_index=1,
            font_size=55
        )
    )
    rating_class = result['overall']['rating_class']
    rating_png_path = os.path.join(ASSETS_DIR, r'content\rating\pr', user_bind['language'], '{}.png'.format(rating_class))
    rating_png = Image.open(rating_png_path)
    res_img.paste(rating_png, (132, 627))
    del rating_png
    if bot_settings.SHOW_DOG_TAG:
        if result['user']['dog_tag'] == [] or result['user']['dog_tag'] == {}:
            pass
        else:
            # TODO: 叠加徽章
            pass
    rating_dict = {
        'cn': [
            {'text': ContentText_CN.RatingNextText_1 + ':    +'},
            {'text': ContentText_CN.RatingNextText_2 + ':    +'}
        ],
        'en': [
            {'text': ContentText_EN.RatingNextText_1 + ':    +'},
            {'text': ContentText_EN.RatingNextText_2 + ':    +'}
        ],
        'ja': [
            {'text': ContentText_JA.RatingNextText_1 + ':    +'},
            {'text': ContentText_JA.RatingNextText_2 + ':    +'}
        ]
    }
    fontStyle = fonts.data[1][35]
    if result['overall']['rating_class'] == 9:
        rating_next_text = rating_dict[user_bind['language']][1] + str(result['overall']['rating_next'])
    else:
        rating_next_text = rating_dict[user_bind['language']][0] + str(result['overall']['rating_next'])
    text_list.append(
        Text_Data(
            xy=(132+ss+10, 690),
            text=rating_next_text,
            fill=(255, 255, 255),
            font_index=1,
            font_size=35
        )
    )
    str_pr = '{:,}'.format(result['data']['pr']['avg_pr'])
    fontStyle = fonts.data[1][80]
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
    index = result['data']['pr']['battle_type'].upper()
    x0 = 324
    y0 = 860
    temp_data = result['data']['pr']
    battles_count = temp_data['battles_count']
    avg_win = temp_data['win_rate']
    avg_damage = temp_data['avg_damage']
    avg_frag = temp_data['avg_frags']
    avg_xp = temp_data['avg_exp']
    win_rate_color = Picture.hex_to_rgb(temp_data['win_rate_color'])
    avg_damage_color = Picture.hex_to_rgb(temp_data['avg_damage_color'])
    avg_frags_color = Picture.hex_to_rgb(temp_data['avg_frags_color'])

    fontStyle = fonts.data[1][80]
    w = Picture.x_coord(battles_count, fontStyle)
    text_list.append(
        Text_Data(
            xy=(x0+446*0-w/2, y0),
            text=battles_count,
            fill=(0, 0, 0),
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
            fill=(0, 0, 0),
            font_index=1,
            font_size=80
        )
    )
    i = 0
    for index in ['pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']:
        x0 = 0
        y0 = 1258
        temp_data = result['data']['battle_type'][index]
        battles_count = temp_data['battles_count']
        avg_win = temp_data['win_rate']
        avg_damage = temp_data['avg_damage']
        avg_frag = temp_data['avg_frags']
        avg_xp = temp_data['avg_exp']
        win_rate_color = Picture.hex_to_rgb(temp_data['win_rate_color'])
        avg_damage_color = Picture.hex_to_rgb(temp_data['avg_damage_color'])
        avg_frags_color = Picture.hex_to_rgb(temp_data['avg_frags_color'])
        avg_pr_color = Picture.hex_to_rgb(temp_data['avg_pr_color'])
        if temp_data['avg_pr_des'] == '-':
            str_pr = '-'
        else:
            if lang == 'cn':
                str_pr = temp_data['avg_pr_des'] + '(+'+str(temp_data['avg_pr_dis'])+')'
            elif lang == 'en':
                str_pr = '■ '+str(int(temp_data['avg_pr']))
            elif lang == 'ja':
                str_pr = '■ '+str(int(temp_data['avg_pr']))
        fontStyle = fonts.data[1][55]
        w = Picture.x_coord(battles_count, fontStyle)
        text_list.append(
            Text_Data(
                xy=(588-w/2+x0, y0+90*i),
                text=battles_count,
                fill=(0, 0, 0),
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
                fill=(0, 0, 0),
                font_index=1,
                font_size=55
            )
        )
        i += 1
    i = 0
    for index in ['AirCarrier', 'Battleship', 'Cruiser', 'Destroyer', 'Submarine']:
        x0 = 0
        y0 = 1855
        temp_data = result['data']['ship_type'][index]
        battles_count = temp_data['battles_count']
        avg_win = temp_data['win_rate']
        avg_damage = temp_data['avg_damage']
        avg_frag = temp_data['avg_frags']
        avg_xp = temp_data['avg_exp']
        win_rate_color = Picture.hex_to_rgb(temp_data['win_rate_color'])
        avg_damage_color = Picture.hex_to_rgb(temp_data['avg_damage_color'])
        avg_frags_color = Picture.hex_to_rgb(temp_data['avg_frags_color'])
        avg_pr_color = Picture.hex_to_rgb(temp_data['avg_pr_color'])
        if temp_data['avg_pr_des'] == '-':
            str_pr = '-'
        else:
            if lang == 'cn':
                str_pr = temp_data['avg_pr_des'] + '(+'+str(temp_data['avg_pr_dis'])+')'
            elif lang == 'en':
                str_pr = '■ '+str(int(temp_data['avg_pr']))
            elif lang == 'ja':
                str_pr = '■ '+str(int(temp_data['avg_pr']))
        fontStyle = fonts.data[1][55]
        w = Picture.x_coord(battles_count, fontStyle)
        text_list.append(
            Text_Data(
                xy=(588-w/2+x0, y0+90*i),
                text=battles_count,
                fill=(0, 0, 0),
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
                fill=(0, 0, 0),
                font_index=1,
                font_size=55
            )
        )
        i += 1
    max_num = 0
    num_list = []
    for tier, num in result['data']['ship_tier'].items():
        if num >= max_num:
            max_num = num
        num_list.append(num)
    max_index = (int(max_num/100) + 1)*100
    i = 0
    fontStyle = fonts.data[1][35]
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
                fill=(0, 0, 0),
                font_index=1,
                font_size=35
            )
        )
        i += 1
    fontStyle = fonts.data[1][80]
    w = Picture.x_coord(Plugin_Config.BOT_INFO[lang], fontStyle)
    text_list.append(
        Text_Data(
            xy=(1214-w/2, 3214),
            text=Plugin_Config.BOT_INFO[lang],
            fill=(174, 174, 174),
            font_index=1,
            font_size=80
        )
    )
    res_img = Picture.add_box(box_list, res_img)
    res_img = Picture.add_text(text_list, res_img)
    res_img_size = res_img.size
    res_img = res_img.resize(
        (
            int(res_img_size[0]*0.5), 
            int(res_img_size[1]*0.5)
        )
    )
    return res_img


            


