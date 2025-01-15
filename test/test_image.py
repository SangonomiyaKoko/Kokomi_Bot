import os
import time
import json
from typing import Literal
from datetime import datetime, timezone
from PIL import Image, ImageFont, ImageDraw

OUTPUT_DIR = r'F:\Kokomi_PJ_Bot\output'

ASSETS_DIR = r'F:\Kokomi_PJ_Bot\assets'

class FontManager:
    def __init__(self):
        self.font_path = {
            1: os.path.join(ASSETS_DIR, 'fonts', 'SHSCN.ttf'),
            2: os.path.join(ASSETS_DIR, 'fonts', 'NZBZ.ttf')
        }
        self.font_cache = {
            1: {},
            2: {}
        }

    def get_font(self, index: int, size: int) -> ImageFont.FreeTypeFont:
        if size not in self.font_cache[index]:
            self.font_cache[index][size] = ImageFont.truetype(self.font_path[index], size)
        return self.font_cache[index][size]

font_manager = FontManager()

class Text_Data:
    def __init__(
        self,
        xy: tuple,
        text: str,
        fill: tuple,
        font_index: int,
        font_size: int
    ):
        self.xy = xy
        self.text = text
        self.fill = fill
        self.font_index = font_index
        self.font_size = font_size

class Box_Data:
    def __init__(
        self,
        xy: tuple,
        fill: tuple,
    ):
        self.xy = xy
        self.fill = fill

class Picture:
    def hex_to_rgb(hex_color: str ,alpha:int = None) -> str:
        "16进制颜色转rgb颜色"
        if alpha:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return (r, g, b, alpha)
        else:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return (r, g, b)
    
    def return_img(img: Image.Image) -> str:
        try:
            file_name = os.path.join(OUTPUT_DIR, str(time.time()*1000) + '.png')
            img.save(file_name)
            return {
                'status': 'ok',
                'code': 1000,
                'message': 'Success',
                'data': {
                    'img': file_name
                }
            }
        finally:
            del img
    
    def x_coord(in_str: str, font: ImageFont.FreeTypeFont) -> float:
        # x = font.getsize(in_str)[0]
        x = font.getlength(in_str)
        return x
    
    def formate_str(in_str: str, str_len, max_len):
        if str_len <= max_len:
            return in_str
        else:
            return in_str[:int(max_len/str_len*len(in_str))-2] + '...'

    def add_box(box_list, res_img):
        if box_list is None:
            return res_img
        img = ImageDraw.ImageDraw(res_img)
        for index in box_list:
            index: Box_Data
            img.rectangle(
                xy=index.xy,
                fill=index.fill,
                outline=None
            )
        return res_img

    def add_text(text_list, res_img):
        if text_list is None:
            return res_img
        draw = ImageDraw.Draw(res_img)
        for index in text_list:
            index: Text_Data
            fontStyle = font_manager.get_font(index.font_index, index.font_size)
            draw.text(
                xy=index.xy,
                text=index.text,
                fill=index.fill,
                font=fontStyle
            )
        return res_img
    
class ContentLanguage:
    UserClan = 'User\'s Clan'
    Createdat = 'Created at'
    DataType = ''
    RatingNextText_1 = 'Next level'
    RatingNextText_2 = 'Out of top rating'
    
    def get_rating_text(rating_class: int, return_len: bool = False) -> str | tuple:
        rating_text_list = [
            'Unknow','Improvement Needed','Below Average',
            'Average','Good','Very Good','Great','Unicum',
            'Super Unicum','Super Ultra Unicum'
        ]
        rating_len_list = [
            425,910,660,420,
            300,500,330,410,
            630,825
        ]
        if return_len:
            return rating_text_list[rating_class], rating_len_list[rating_class]
        else:
            return rating_text_list[rating_class]

    def get_rank_text(season_rank: int) -> str:
        rank_text_dict = {
            1: 'Gold',
            2: 'Silver',
            3: 'Bronze'
        }
        return rank_text_dict.get(season_rank)
    
class ThemeTextColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.TextThemeColor1 = (255, 255, 255)
            self.TextThemeColor2 = (225, 225, 225)
            self.TextThemeColor3 = (180, 180, 180)
            self.TextThemeColor4 = (130, 130, 130)
            self.TextThemeColor5 = (80, 80, 80)
        elif theme.lower() == "light":
            self.TextThemeColor1 = (0, 0, 0)
            self.TextThemeColor2 = (20, 20, 20)
            self.TextThemeColor3 = (75, 75, 75)
            self.TextThemeColor4 = (125, 125, 125)
            self.TextThemeColor5 = (175, 175, 175)
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")

REGION_UTC_LIST = {
    1: 8,
    2: 1,
    3: -7,
    4: 3,
    5: 8
}

class TimeFormat:
    def get_datetime_now() -> str:
        "获取图片的创建时间的格式"
        # e.g., "2024-12-11 08:30:15.123456+00:00"
        utc_time_with_zone = str(datetime.now(timezone.utc))
        return utc_time_with_zone[:19].replace(' ', 'T') + utc_time_with_zone[26:]
    
    def get_strftime(region_id: int, timestamp: int, format: str = '%Y%m%d') -> str:
        "获取服务器对应时区的时间"
        time_zone = REGION_UTC_LIST.get(region_id)
        return time.strftime(format, time.gmtime(timestamp + time_zone * 3600))

class ThemeRatingColor:
    def __init__(self, theme: Literal['dark', 'light']):
        if theme.lower() == "dark":
            self.RatingThemeColor = [
                (127, 127, 127),
                (205, 51, 51),
                (254, 121, 3),
                (255, 193, 7),
                (78, 206, 0),
                (10, 145, 0),
                (52, 186, 211),
                (200, 45, 200),
                (147, 50, 212)
            ]
        elif theme.lower() == "light":
            self.RatingThemeColor = [
                (127, 127, 127),
                (205, 51, 51),
                (254, 121, 3),
                (255, 193, 7),
                (68, 179, 0),
                (49, 128, 0),
                (52, 186, 211),
                (121, 61, 182),
                (88, 43, 128)
            ]
        else:
            raise ValueError("Invalid theme. Please choose 'dark' or 'light'.")
    
    def get_class_color(self, content_class: int) -> tuple:
        '''获取评分等级对应的颜色'''
        return self.RatingThemeColor[content_class]

class Utils:
    def get_language(language: str) -> str:
        "获取接口语言的参数内容"
        language_dict = {
            'cn': 'chinese',
            'en': 'english',
            'ja': 'japanese'
        }
        return language_dict.get(language)
    
    def get_language_from_input(input: str) -> str | None:
        "处理用户输入的language参数"
        language_dict = {
            'cn':'cn','chinese':'cn',
            'en':'en','english':'en',
            'ja':'ja','japanese':'ja' 
        }
        return language_dict.get(input.lower(), None)
    
    def get_operator_by_id(region_id: int) -> str:
        "获取服务器id对应的运营商，不同运营商对应的素材会有不同"
        if region_id == 4:
            return 'LestaGame'
        else:
            return 'WarGaming'

    def get_region_id_from_input(input: str) -> int | None:
        "处理用户输入的region参数"
        region_dict = {
            'asia':1,'apac':1,'aisa':1,'亚服':1,    # 为什么总会有人拼成aisa？
            'eu':2,'europe':2,'欧服':2,
            'na':3,'northamerica':3,'america':3,'美服':3,
            'ru':4,'russia':4,'俄服':4,'莱服':4,
            'cn':5,'china':5,'国服':5
        }
        return region_dict.get(input.lower(), None)

    def get_region_by_id(region_id: int) -> str:
        "获取region"
        region_dict = {
            1: 'asia',
            2: 'eu',
            3: 'na',
            4: 'ru',
            5: 'cn'
        }
        return region_dict.get(region_id)

class GameData:
    tier_dict = {
        1: 'Ⅰ',
        2: 'Ⅱ',
        3: 'Ⅲ',
        4: 'Ⅳ',
        5: 'Ⅴ',
        6: 'Ⅵ',
        7: 'Ⅶ',
        8: 'Ⅷ',
        9: 'Ⅸ',
        10: 'Ⅹ',
        11: '★',
    }

    type_dict = {
        'AirCarrier': 'CV',
        'Battleship': 'BB',
        'Cruiser': 'CA',
        'Destroyer': 'DD',
        'Submarine': 'SS',
    }

    border_color = {
        "4293348272": "0x282828",
        "4292299696": "0x23325d",
        "4291251120": "0x15668c",
        "4290202544": "0x213f47",
        "4289153968": "0x3a4a23",
        "4288105392": "0x553b16",
        "4287056816": "0x6d4f29",
        "4286008240": "0x8a763a",
        "4284959664": "0xd9d9d9",
        "4283911088": "0xf3c612",
        "4282862512": "0xcb7208",
        "4281813936": "0xa73a1c",
        "4280765360": "0xa32323",
        "4279716784": "0x7f1919",
        "4278668208": "0x382c4f"
    }

    background_color = {
        "4293577648": "0x252525",
        "4292529072": "0x25355d",
        "4291480496": "0x2b6e91",
        "4290431920": "0x22454a",
        "4289383344": "0x3f4d2c",
        "4288334768": "0x8f7e44",
        "4287286192": "0x8b6932",

        "4286237616": "0xc9c9c9",
        "4285189040": "0xcfa40f",
        "4284140464": "0xd98815",
        "4283091888": "0xb74522",
        "4282043312": "0xad1d1d",
        "4280994736": "0x771d27",
        "4279946160": "0x3b2f4e"
    }

    clan_league_color = {
        0: (121, 61, 182),
        1: (144, 223, 143),
        2: (234, 197, 0),
        3: (147, 147, 147),
        4: (184, 115, 51),
        5: (147, 147, 147)
    }

response_path = r'C:\Users\MaoYu\Downloads\response_1736433127065.json'
temp = open(response_path, "r", encoding="utf-8")
result = json.load(temp)['data']
temp.close()

# 画布宽度和高度
width, height = 2428, 3350
# 背景颜色（RGB）
background_color = Picture.hex_to_rgb('#F8F9FB', 100)
# 创建画布
canvas = Image.new("RGBA", (width, height), background_color)
# TODO: 叠加主题背景

# 叠加图片主体
content_png_path = os.path.join(ASSETS_DIR, 'content', 'light', 'en', 'basic.png')
content_png = Image.open(content_png_path)
canvas.alpha_composite(content_png, (0, 0))
# TODO: 叠加图片主题图片

res_img = canvas
del canvas
# 获取语言对应的文本文字
content_text = ContentLanguage
# 获取不同主题的文字颜色
theme_text_color = ThemeTextColor('light')
# 获取不同主题的评分颜色
theme_rating_color = ThemeRatingColor('light')
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
        text=f"ASIA -- {result['user']['id']}",
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
rating_png_path = os.path.join(ASSETS_DIR, r'content\rating\pr', 'en', '{}.png'.format(rating_class))
rating_png = Image.open(rating_png_path)
res_img.paste(rating_png, (132, 627))
del rating_png
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
temp_data = result['statistics']['overall']
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
    temp_data = result['statistics']['battle_type'][index]
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
    temp_data = result['statistics']['ship_type'][index]
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
w = Picture.x_coord('Powered by '+'Kokomi-Bot 5.0.0', fontStyle)
text_list.append(
    Text_Data(
        xy=(2331-20-w, 3214),
        text='Powered by '+'Kokomi-Bot 5.0.0',
        fill=theme_text_color.TextThemeColor5,
        font_index=1,
        font_size=55
    )
)
# 完成文字和矩形的叠加
res_img = Picture.add_box(box_list, res_img)
res_img = Picture.add_text(text_list, res_img)
file_name = os.path.join(OUTPUT_DIR, str(time.time()*1000) + '.png')
res_img.save(file_name)