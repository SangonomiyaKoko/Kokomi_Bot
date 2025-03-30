# 此处是用于更新船只图片的功能，需要配合解压工具使用

from PIL import Image, ImageDraw, ImageFont
import json
import os

file_path = os.path.dirname(__file__)

def x_coord(in_str: str, font: ImageFont.FreeTypeFont):
    x = font.getlength(in_str)
    out_coord = x
    return out_coord

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

ship_info = json.load(open(os.path.join(file_path, 'json', 'ship_name_main.json'), "r", encoding="utf-8"))
img_jpg_path = os.path.join(file_path, 'bg_2.png')
img_jpg = Image.open(img_jpg_path)
i = 1
lang = 'cn'
res = None
all_dict = {}
text_list = []
for ship_id, ship_data in ship_info.items():
    nation = ship_data['nation']
    type = ship_data['type']
    tier = ship_data['tier']
    name = ship_data['index']
    nickname = ship_data['ship_name'][lang]
    server = ship_data['server']
    all_dict[name] = i
    if name == 'PHSC711':
        name = 'PHSC710'
    if server == 'wg':
        ship_path = os.path.join(file_path, 'as_unpack', 'gui', 'ship_icons', '{}.png'.format(name))
    elif server == 'lesta':
        ship_path = os.path.join(file_path, 'ru_unpack', 'gui', 'ship_icons', '{}.png'.format(name))
    else:
        ship_path = os.path.join(file_path, 'as_unpack', 'gui', 'ship_icons', '{}.png'.format(name))
    img_png_path = os.path.join(file_path, 'ship_type', '{}.png'.format(type))
    img2_png_path = os.path.join(file_path, 'ship_nation', 'flag_{}.png'.format(name))
    if os.path.exists(img2_png_path) != True:
        img2_png_path = os.path.join(
            file_path, 'ship_nation', 'flag_{}.png'.format(nation))
    print(i,' :  ',ship_path)
    img3_png_path = ship_path
    img_png = Image.open(img_png_path)
    img2_png = Image.open(img2_png_path)
    img3_png = Image.open(img3_png_path).convert('RGBA')
    img2_png = img2_png.resize((194, 119))
    img3_png = img3_png.resize((365, 63))
    x = (i % 10) * 517
    y = int(i / 10) * 115
    # 设置叠加位置坐标
    if i == 1:
        res_img = img_jpg
    else:
        res_img = res
    x1 = 1 + x
    y1 = 1 + y
    res_img.alpha_composite(img2_png,(x1,y1))
    x1 = 3 + x
    y1 = 74 + y
    res_img.alpha_composite(img_png,(x1,y1))
    if type in ['Submarine','Destroyer']:
        x1 = 170 + x + 5
    elif type in ['Battleship','AirCarrier']:
        if tier in [8,9,10,11]:
            x1 = 170 + x - 18
        else:
            x1 = 170 + x - 15
    else:
        x1 = 170 + x
    y1 = 1 + y
    res_img.alpha_composite(img3_png,(x1,y1))
    if lang == 'en':
        text_list.append([nickname, 482+x-3, 64+y, (0, 0, 0), 45, True])
    elif lang == 'ja':
        text_list.append([nickname, 482+x-3, 64+y, (0, 0, 0), 45, True])
    else:
        text_list.append([nickname, 482+x-3, 68+y, (0, 0, 0), 45, True])
    text_list.append([tier_dict[tier], 65+x, 77+y, (255, 255, 255), 30, False])
    i += 1
    res = res_img

draw = ImageDraw.Draw(res_img)
for index in text_list:
    text = index[0]
    left = index[1]
    top = index[2]
    textColor = index[3]
    textSize = index[4]
    on_right = index[5]
    fontStyle = ImageFont.truetype(os.path.join(file_path, 'fonts', 'SourceHanSansCN-Bold.ttf'), textSize, encoding="utf-8")
    if on_right:
        w = x_coord(text, font=fontStyle)
        if w >= 300:
            del_len = int(((w-300)/w)*len(text))
            text = text[:(len(text)-del_len-1)]+'...'
            w = x_coord(text, font=fontStyle)
        left = left - w
    draw.text((left, top), text, textColor, font=fontStyle)

print(i)
if i % 10 == 0:
    res_img = res_img.crop((0, 0, 5170, 115*int(i/10)))
    res_img = res_img.resize((3600,80*int(i/10)))
else:
    res_img = res_img.crop((0, 0, 5170, 115*int(i/10+1)))
    res_img = res_img.resize((3600,80*int(i/10+1)))
res_img.save(os.path.join(file_path,  f'ship_preview_{lang}.png'))
with open(os.path.join(file_path, f'ship_preview_{lang}.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(all_dict, ensure_ascii=False))
f.close()
