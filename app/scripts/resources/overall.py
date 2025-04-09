import os
from typing_extensions import TypedDict

from ..config import ASSETS_DIR, bot_settings
from ..logs import logging
from ..api import BaseAPI, Mock
from ..logs import ExceptionLogger
from ..language import Content
from ..common import (
    Insignias, Utils, GameData, ThemeTextColor, ThemeRatingColor, TimeFormat, ReadVersionFile
)
from ..image import (
    ImageDrawManager, ImageHandler, TextOperation as Text, RectangleOperation as Rectangle
)
from ..schemas import (
    KokomiUser, UserBasicDict, UserClanDict, UserOverallDict,
    ResultShipTypeDict, ResultBattleTypeDict, BasicBattleTypeDict
)


class OverallDict1(TypedDict):
    overall: UserOverallDict
    battle_type: ResultBattleTypeDict
    ship_type: ResultShipTypeDict
    chart_data: dict

class OverallDict2(TypedDict):
    data_type: str
    overall: UserOverallDict
    battle_type: BasicBattleTypeDict
    ship_type: ResultShipTypeDict
    chart_data: dict

class UserBaseResult1(TypedDict):
    user: UserBasicDict
    clan: UserClanDict
    statistics: OverallDict1

class UserBaseResult2(TypedDict):
    user: UserBasicDict
    clan: UserClanDict
    statistics: OverallDict2


@ExceptionLogger.handle_program_exception_async
async def main(
    user: KokomiUser,
    filter_type: str = None
) -> dict:
    if not filter_type:
        path = '/api/v1/robot/user/stats/basic1/'
        params = {
            'region': Utils.get_region_by_id(user.bind.region_id),
            'account_id': user.bind.account_id,
            'language': Utils.get_language(user.local.language)
        }
        if user.local.algorithm:
            params['algo_type'] = user.local.algorithm
        
        if bot_settings.USE_MOCK:
            result = Mock.read_data('basic1.json')
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
        result = get_png1(
            user=user,
            result=result['data']
        )
    else:
        path = '/api/v1/robot/user/stats/basic2/'
        params = {
            'region': Utils.get_region_by_id(user.bind.region_id),
            'account_id': user.bind.account_id,
            'language': Utils.get_language(user.local.language),
            'filter_type': filter_type
        }
        if user.local.algorithm:
            params['algo_type'] = user.local.algorithm
        
        if bot_settings.USE_MOCK:
            result = Mock.read_data('basic2.json')
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
        result = get_png2(
            user=user,
            result=result['data']
        )
    return result


@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png1(
    user: KokomiUser,
    result: UserBaseResult1
) -> str:
    # 画布宽度和高度
    width, height = 2428, 3320 + 130
    # 背景颜色（RGBA）
    background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    res_img = ImageHandler.new_image([width, height], background_color)
    # 获取语言对应的文本文字
    content_text = Content.get_content_language(user.local.language)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 获取不同主题的评分颜色
    theme_rating_color = ThemeRatingColor(user.local.content)
    # 开始图片渲染流程
    with ImageDrawManager(res_img, 'ps', 300) as image_manager:
        # 叠加图片主题图片
        if user.local.theme != 'default':
            theme_png_path = os.path.join(ASSETS_DIR, 'theme', user.local.theme, f'{user.local.content}_basic.png')
            if os.path.exists(theme_png_path):
                image_manager.composite_alpha(theme_png_path, (0, 0))
            else:
                ...
    
        # 叠加图片主体
        content_png_path = os.path.join(ASSETS_DIR, 'content', user.local.content, user.local.language, 'basic.png')
        image_manager.composite_alpha(content_png_path, (0, 0))

        # ===================== Header组件 =====================
        header_png_path = os.path.join(ASSETS_DIR, 'components', 'header', f'{user.local.content}.png')
        image_manager.composite_alpha(header_png_path, (97, 130))
        image_manager.add_text(
            Text(
                text=result['user']['name'],
                position=(171, 155),
                font_index=1,
                font_size=22,
                color=theme_text_color.TextThemeColor2
            )
        )
        region = Utils.get_region_by_id(result['user']['region'])
        region_png_path = os.path.join(ASSETS_DIR, 'components', 'region', f'{region}.png')
        image_manager.composite_alpha(region_png_path, (81+97, 142+130), resize_size=(76, 42))
        image_manager.add_text(
            Text(
                text=region.upper(),
                position=(251+97, 272),
                font_index=1,
                font_size=10,
                color=theme_text_color.TextThemeColor4,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=str(result['user']['id']),
                position=(489+97, 272),
                font_index=1,
                font_size=10,
                color=theme_text_color.TextThemeColor4,
                align='center'
            )
        )
        if result['clan']['id'] != None:
            tag = '['+str(result['clan']['tag'])+']'
        else:
            tag = 'None'
        clan_league_color = GameData.clan_league_color.get(result['clan']['league'])
        text_1 = content_text.UserClan + ':'
        image_manager.add_text(
            Text(
                text=text_1,
                position=(169, 358),
                font_index=1,
                font_size=14,
                color=theme_text_color.TextThemeColor3
            )
        )
        w_1 = image_manager.get_text_width(text_1, 1, 14)
        image_manager.add_text(
            Text(
                text=tag,
                position=(169+w_1+30, 358),
                font_index=1,
                font_size=14,
                color=clan_league_color
            )
        )
        text_2 = content_text.Createdat + ':'
        image_manager.add_text(
            Text(
                text=text_2,
                position=(169, 448),
                font_index=1,
                font_size=14,
                color=theme_text_color.TextThemeColor3
            )
        )
        w_2 = image_manager.get_text_width(text_2, 1, 14)
        creat_time = TimeFormat.get_strftime(result['user']['region'], result['user']['created_at'], "%Y-%m-%d")
        image_manager.add_text(
            Text(
                text=creat_time,
                position=(169+w_2+30, 448),
                font_index=1,
                font_size=14,
                color=theme_text_color.TextThemeColor2
            )
        )
        # ===================== Overall组件 =====================
        rating_class = result['statistics']['overall']['rating_class']
        rating_png_path = os.path.join(ASSETS_DIR, 'content', 'rating', 'pr', user.local.language, user.local.content, '{}.png'.format(rating_class))
        image_manager.composite_paste(rating_png_path, (132, 627))
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
                    image_manager.composite_alpha(insignias_png_path, (1912, 129), resize_size=(419, 419))
        if result['statistics']['overall']['rating_class'] == 9:
            rating_next_text = content_text.RatingNextText_2 + ':    +' + str(result['statistics']['overall']['rating_next'])
        else:
            rating_next_text = content_text.RatingNextText_1 + ':    +' + str(result['statistics']['overall']['rating_next'])
        _, rating_next_len = content_text.get_rating_text(result['statistics']['overall']['rating_class'], True)
        image_manager.add_text(
            Text(
                text=rating_next_text,
                position=(132+rating_next_len+10, 690),
                font_index=1,
                font_size=8,
                color=(255, 255, 255)
            )
        )
        str_pr = result['statistics']['overall']['rating']
        image_manager.add_text(
            Text(
                text=result['statistics']['overall']['rating'],
                position=(2284, 642),
                font_index=1,
                font_size=20,
                color=(255, 255, 255),
                align='right'
            )
        )
        x0 = 324
        y0 = 860
        temp_data: UserOverallDict = result['statistics']['overall']
        battles_count = temp_data['battles_count']
        avg_win = temp_data['win_rate']
        avg_damage = temp_data['avg_damage']
        avg_frags = temp_data['avg_frags']
        avg_xp = temp_data['avg_exp']
        win_rate_color = theme_rating_color.get_class_color(temp_data['win_rate_class'])
        avg_damage_color = theme_rating_color.get_class_color(temp_data['avg_damage_class'])
        avg_frags_color = theme_rating_color.get_class_color(temp_data['avg_frags_class'])
        image_manager.add_text(
            Text(
                text=battles_count,
                position=(x0+446*0, y0),
                font_index=1,
                font_size=20,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_win,
                position=(x0+446*1, y0),
                font_index=1,
                font_size=20,
                color=win_rate_color,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_damage,
                position=(x0+446*2, y0),
                font_index=1,
                font_size=20,
                color=avg_damage_color,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_frags,
                position=(x0+446*3, y0),
                font_index=1,
                font_size=20,
                color=avg_frags_color,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_xp,
                position=(x0+446*4, y0),
                font_index=1,
                font_size=20,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        # ===================== BattleType组件 =====================
        i = 0
        for index in ['pvp_solo', 'pvp_div2', 'pvp_div3', 'rank_solo']:
            x0 = 0
            y0 = 1258
            temp_data: UserOverallDict = result['statistics']['battle_type'][index]
            battles_count = temp_data['battles_count']
            avg_win = temp_data['win_rate']
            avg_damage = temp_data['avg_damage']
            avg_frags = temp_data['avg_frags']
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
            image_manager.add_text(
                Text(
                    text=battles_count,
                    position=(588+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=str_pr,
                    position=(955+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_pr_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_win,
                    position=(1307+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=win_rate_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_damage,
                    position=(1613+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_damage_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_frags,
                    position=(1909+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_frags_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_xp,
                    position=(2177+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            i += 1
        ## ===================== ShipType组件 =====================
        i = 0
        for index in ['AirCarrier', 'Battleship', 'Cruiser', 'Destroyer', 'Submarine']:
            x0 = 0
            y0 = 1855
            temp_data: UserOverallDict = result['statistics']['ship_type'][index]
            battles_count = temp_data['battles_count']
            avg_win = temp_data['win_rate']
            avg_damage = temp_data['avg_damage']
            avg_frags = temp_data['avg_frags']
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
            image_manager.add_text(
                Text(
                    text=battles_count,
                    position=(588+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=str_pr,
                    position=(955+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_pr_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_win,
                    position=(1307+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=win_rate_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_damage,
                    position=(1613+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_damage_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_frags,
                    position=(1909+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_frags_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_xp,
                    position=(2177+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            i += 1
        # ===================== 图表组件 =====================
        max_num = 0
        num_list = []
        for _, num in result['statistics']['chart_data'].items():
            if num >= max_num:
                max_num = num
            num_list.append(num)
        max_index = (int(max_num/100) + 1)*100
        if user.local.content == 'dark':
            box_color = (0, 117, 169)
        else:
            box_color = (52, 186, 211)
        i = 0
        for index in num_list:
            pic_len = 500-index/max_index*500
            x1 = 272+129*i
            y1 = 2542+int(pic_len)
            x2 = 350+129*i
            y2 = 3045
            image_manager.add_rectangle(
                Rectangle(
                    position=(x1, y1),
                    size=(x2-x1, y2-y1),
                    color=box_color
                )
            )
            image_manager.add_text(
                Text(
                    text=str(index),
                    position=(311+129*i, y1-40),
                    font_index=1,
                    font_size=8,
                    color=theme_text_color.TextThemeColor2,
                    align='center'
                )
            )
            i += 1
        # ===================== Footer组件 =====================
        footer_png_path = os.path.join(ASSETS_DIR, 'components', 'footer', f'{user.local.content}.png')
        image_manager.composite_alpha(footer_png_path, (97, 3220))
        image_manager.add_text(
            Text(
                text=bot_settings.BOT_INFO,
                position=(145, 3243),
                font_index=1,
                font_size=12,
                color=theme_text_color.TextThemeColor4
            )
        )
        image_manager.add_text(
            Text(
                text=TimeFormat.get_datetime_now(),
                position=(1212, 3243),
                font_index=1,
                font_size=12,
                color=theme_text_color.TextThemeColor4
            )
        )
        image_manager.add_text(
            Text(
                text=ReadVersionFile.read_version(),
                position=(2010, 3243),
                font_index=1,
                font_size=12,
                color=theme_text_color.TextThemeColor4
            )
        )
        # 提交操作并返回渲染好的图片
        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result

@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png2(
    user: KokomiUser,
    result: UserBaseResult2
) -> str:
    # 画布宽度和高度
    width, height = 2428, 3360 + 130
    # 背景颜色（RGBA）
    background_color = Utils.hex_to_rgb(user.local.background, 255)
    # 创建画布
    res_img = ImageHandler.new_image([width, height], background_color)
    # 获取语言对应的文本文字
    content_text = Content.get_content_language(user.local.language)
    # 获取不同主题的文字颜色
    theme_text_color = ThemeTextColor(user.local.content)
    # 获取不同主题的评分颜色
    theme_rating_color = ThemeRatingColor(user.local.content)
    # 开始图片渲染流程
    with ImageDrawManager(res_img, 'ps', 300) as image_manager:
        # # 叠加图片主题图片
        if user.local.theme != 'default':
            theme_png_path = os.path.join(ASSETS_DIR, 'theme', user.local.theme, f'{user.local.content}_basic.png')
            if os.path.exists(theme_png_path):
                image_manager.composite_alpha(theme_png_path, (0, 0))
            else:
                ...
    
        # 叠加图片主体
        content_png_path = os.path.join(ASSETS_DIR, 'content', user.local.content, user.local.language, 'basic2.png')
        image_manager.composite_alpha(content_png_path, (0, 0))

        # ===================== Header组件 =====================
        header_png_path = os.path.join(ASSETS_DIR, 'components', 'header', f'{user.local.content}.png')
        image_manager.composite_alpha(header_png_path, (97, 130))
        image_manager.add_text(
            Text(
                text=result['user']['name'],
                position=(171, 155),
                font_index=1,
                font_size=22,
                color=theme_text_color.TextThemeColor2
            )
        )
        region = Utils.get_region_by_id(result['user']['region'])
        region_png_path = os.path.join(ASSETS_DIR, 'components', 'region', f'{region}.png')
        image_manager.composite_alpha(region_png_path, (81+97, 142+130), resize_size=(76, 42))
        image_manager.add_text(
            Text(
                text=region.upper(),
                position=(251+97, 272),
                font_index=1,
                font_size=10,
                color=theme_text_color.TextThemeColor4,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=str(result['user']['id']),
                position=(489+97, 272),
                font_index=1,
                font_size=10,
                color=theme_text_color.TextThemeColor4,
                align='center'
            )
        )
        if result['clan']['id'] != None:
            tag = '['+str(result['clan']['tag'])+']'
        else:
            tag = 'None'
        clan_league_color = GameData.clan_league_color.get(result['clan']['league'])
        text_1 = content_text.UserClan + ':'
        image_manager.add_text(
            Text(
                text=text_1,
                position=(169, 358),
                font_index=1,
                font_size=14,
                color=theme_text_color.TextThemeColor3
            )
        )
        w_1 = image_manager.get_text_width(text_1, 1, 14)
        image_manager.add_text(
            Text(
                text=tag,
                position=(169+w_1+30, 358),
                font_index=1,
                font_size=14,
                color=clan_league_color
            )
        )
        text_2 = content_text.Createdat + ':'
        image_manager.add_text(
            Text(
                text=text_2,
                position=(169, 448),
                font_index=1,
                font_size=14,
                color=theme_text_color.TextThemeColor3
            )
        )
        w_2 = image_manager.get_text_width(text_2, 1, 14)
        creat_time = TimeFormat.get_strftime(result['user']['region'], result['user']['created_at'], "%Y-%m-%d")
        image_manager.add_text(
            Text(
                text=creat_time,
                position=(169+w_2+30, 448),
                font_index=1,
                font_size=14,
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
                    image_manager.composite_alpha(insignias_png_path, (1912, 129), resize_size=(419, 419))
        # ===================== BattleType组件 =====================
        image_manager.add_text(
            Text(
                text=content_text.get_basic_type_text(result['statistics']['data_type']),
                position=(1214, 602),
                font_index=1,
                font_size=16,
                color=theme_text_color.TextThemeColor2,
                align='center'
            )
        )
        # ===================== Overall组件 =====================
        rating_class = result['statistics']['overall']['rating_class']
        rating_png_path = os.path.join(ASSETS_DIR, 'content', 'rating', 'pr', user.local.language, user.local.content, '{}.png'.format(rating_class))
        image_manager.composite_paste(rating_png_path, (132, 757))
        if result['statistics']['overall']['rating_class'] == 9:
            rating_next_text = content_text.RatingNextText_2 + ':    +' + str(result['statistics']['overall']['rating_next'])
        else:
            rating_next_text = content_text.RatingNextText_1 + ':    +' + str(result['statistics']['overall']['rating_next'])
        _, rating_next_len = content_text.get_rating_text(result['statistics']['overall']['rating_class'], True)
        image_manager.add_text(
            Text(
                text=rating_next_text,
                position=(132+rating_next_len+10, 820),
                font_index=1,
                font_size=8,
                color=(255, 255, 255)
            )
        )
        str_pr = result['statistics']['overall']['rating']
        image_manager.add_text(
            Text(
                text=result['statistics']['overall']['rating'],
                position=(2284, 772),
                font_index=1,
                font_size=20,
                color=(255, 255, 255),
                align='right'
            )
        )
        x0 = 324
        y0 = 990
        temp_data: UserOverallDict = result['statistics']['overall']
        battles_count = temp_data['battles_count']
        avg_win = temp_data['win_rate']
        avg_damage = temp_data['avg_damage']
        avg_frags = temp_data['avg_frags']
        avg_xp = temp_data['avg_exp']
        win_rate_color = theme_rating_color.get_class_color(temp_data['win_rate_class'])
        avg_damage_color = theme_rating_color.get_class_color(temp_data['avg_damage_class'])
        avg_frags_color = theme_rating_color.get_class_color(temp_data['avg_frags_class'])
        image_manager.add_text(
            Text(
                text=battles_count,
                position=(x0+446*0, y0),
                font_index=1,
                font_size=20,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_win,
                position=(x0+446*1, y0),
                font_index=1,
                font_size=20,
                color=win_rate_color,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_damage,
                position=(x0+446*2, y0),
                font_index=1,
                font_size=20,
                color=avg_damage_color,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_frags,
                position=(x0+446*3, y0),
                font_index=1,
                font_size=20,
                color=avg_frags_color,
                align='center'
            )
        )
        image_manager.add_text(
            Text(
                text=avg_xp,
                position=(x0+446*4, y0),
                font_index=1,
                font_size=20,
                color=theme_text_color.TextThemeColor3,
                align='center'
            )
        )
        # ===================== BattleType组件 =====================
        i = 0
        for index in ['solo', 'div2', 'div3']:
            x0 = 0
            y0 = 1388
            temp_data: UserOverallDict = result['statistics']['battle_type'][index]
            battles_count = temp_data['battles_count']
            avg_win = temp_data['win_rate']
            avg_damage = temp_data['avg_damage']
            avg_frags = temp_data['avg_frags']
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
            image_manager.add_text(
                Text(
                    text=battles_count,
                    position=(588+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=str_pr,
                    position=(955+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_pr_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_win,
                    position=(1307+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=win_rate_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_damage,
                    position=(1613+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_damage_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_frags,
                    position=(1909+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_frags_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_xp,
                    position=(2177+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            i += 1
        ## ===================== ShipType组件 =====================
        i = 0
        for index in ['AirCarrier', 'Battleship', 'Cruiser', 'Destroyer', 'Submarine']:
            x0 = 0
            y0 = 1895
            temp_data: UserOverallDict = result['statistics']['ship_type'][index]
            battles_count = temp_data['battles_count']
            avg_win = temp_data['win_rate']
            avg_damage = temp_data['avg_damage']
            avg_frags = temp_data['avg_frags']
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
            image_manager.add_text(
                Text(
                    text=battles_count,
                    position=(588+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=str_pr,
                    position=(955+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_pr_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_win,
                    position=(1307+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=win_rate_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_damage,
                    position=(1613+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_damage_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_frags,
                    position=(1909+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=avg_frags_color,
                    align='center'
                )
            )
            image_manager.add_text(
                Text(
                    text=avg_xp,
                    position=(2177+x0, y0+90*i),
                    font_index=1,
                    font_size=14,
                    color=theme_text_color.TextThemeColor3,
                    align='center'
                )
            )
            i += 1
        # ===================== 图表组件 =====================
        max_num = 0
        num_list = []
        for _, num in result['statistics']['chart_data'].items():
            if num >= max_num:
                max_num = num
            num_list.append(num)
        max_index = (int(max_num/100) + 1)*100
        if user.local.content == 'dark':
            box_color = (0, 117, 169)
        else:
            box_color = (52, 186, 211)
        i = 0
        for index in num_list:
            pic_len = 500-index/max_index*500
            x1 = 272+129*i
            y1 = 2582+int(pic_len)
            x2 = 350+129*i
            y2 = 3085
            image_manager.add_rectangle(
                Rectangle(
                    position=(x1, y1),
                    size=(x2-x1, y2-y1),
                    color=box_color
                )
            )
            image_manager.add_text(
                Text(
                    text=str(index),
                    position=(311+129*i, y1-40),
                    font_index=1,
                    font_size=8,
                    color=theme_text_color.TextThemeColor2,
                    align='center'
                )
            )
            i += 1
        # ===================== Footer组件 =====================
        footer_png_path = os.path.join(ASSETS_DIR, 'components', 'footer', f'{user.local.content}.png')
        image_manager.composite_alpha(footer_png_path, (97, 3260))
        image_manager.add_text(
            Text(
                text=bot_settings.BOT_INFO,
                position=(145, 3283),
                font_index=1,
                font_size=12,
                color=theme_text_color.TextThemeColor4
            )
        )
        image_manager.add_text(
            Text(
                text=TimeFormat.get_datetime_now(),
                position=(1212, 3283),
                font_index=1,
                font_size=12,
                color=theme_text_color.TextThemeColor4
            )
        )
        image_manager.add_text(
            Text(
                text=ReadVersionFile.read_version(),
                position=(2010, 3283),
                font_index=1,
                font_size=12,
                color=theme_text_color.TextThemeColor4
            )
        )
        # 提交操作并返回渲染好的图片
        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result
