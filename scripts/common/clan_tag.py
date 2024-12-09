import os
from PIL import Image

def clan_tag_1(
    img,
    cid: str,
    text_list: list,
    response: dict,
    x1: int = 1912,
    y1: int = 131
):
    clan_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_tag', f'{cid}.png')
    clan_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_bg', f'{cid}.png')
    if Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_bg_png_path):
        symbol = Image.open(clan_bg_png_path)
        x1 = 98
        y1 = 129
        img.alpha_composite(symbol, (x1, y1))
        del symbol
        return img, text_list
    elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_tag_png_path):
        symbol = Image.open(clan_tag_png_path)
        symbol = symbol.resize((419, 419))
        img.alpha_composite(symbol, (x1, y1))
        del symbol
        return img, text_list
    elif response == {}:
        return img, text_list
    elif response['stage'] == {}:
        cvc_png_path = os.path.join(plugin_path, 'png', 'clan', '{}-{}-normal.png'.format(
            response['league'], 
            response['division'])
        )
        cvc_png = Image.open(cvc_png_path)
        cvc_png = cvc_png.resize((422, 422))
        img.alpha_composite(cvc_png, (x1, y1))
        division_rating = str(response['division_rating'])
        fontStyle = fonts.data[1][55]
        w = Picture.x_coord(division_rating, fontStyle)
        text_list.append(
            Text_Data(
                xy=(x1+210-w/2, y1+344),
                text=division_rating,
                fill=(230, 230, 230),
                font_index=1,
                font_size=55
            )
        )
        return img, text_list
    else:
        cvc_png_path = os.path.join(plugin_path, 'png', 'clan', '{}-{}-{}.png'.format(
            response['league'], 
            response['division'],
            response['stage']['type']
            )
        )
        cvc_png = Image.open(cvc_png_path)
        cvc_png = cvc_png.resize((422, 422))
        img.alpha_composite(cvc_png, (x1, y1))
        victory_png_path = os.path.join(plugin_path, 'png', 'clan', 'victory.png')
        defeat_png_path = os.path.join(plugin_path, 'png', 'clan', 'defeat.png')
        victory_png = Image.open(victory_png_path)
        victory_png = victory_png.resize((42, 40))
        defeat_png = Image.open(defeat_png_path)
        defeat_png = defeat_png.resize((42, 40))
        i = 0
        for index in response['stage']['progress']:
            if index == 'victory':
                x2 = int(x1 + 76.6 + 56.85*i)
                y2 = y1 + 351
                img.alpha_composite(victory_png, (x1, y1))
            else:
                x2 = int(x1 + 76.6 + 56.85*i)
                y2 = y1 + 351
                img.alpha_composite(defeat_png, (x1, y1))
            i += 1
        del victory_png
        del defeat_png
        return img, text_list
    
def clan_tag_3(
    img,
    cid: str,
    text_list: list,
    x1: int = 1912,
    y1: int = 131
):
    clan_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_tag', f'{cid}.png')
    clan_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_bg', f'{cid}.png')
    if Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_bg_png_path):
        symbol = Image.open(clan_bg_png_path)
        x1 = 98
        y1 = 129
        img.alpha_composite(symbol, (x1, y1))
        del symbol
        return img, text_list
    elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_tag_png_path):
        symbol = Image.open(clan_tag_png_path)
        symbol = symbol.resize((419, 419))
        img.alpha_composite(symbol, (x1, y1))
        del symbol
        return img, text_list
    return img, text_list
    
# def clan_tag(
#     img,
#     cid: str,
#     text_list: list,
#     response: dict,
#     x1: int = 1912,
#     y1: int = 131
# ):
#     clan_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_tag', f'{cid}.png')
#     clan_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_bg', f'{cid}.png')
#     if Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_bg_png_path):
#         symbol = cv2.imread(clan_bg_png_path, cv2.IMREAD_UNCHANGED)
#         x1 = 98
#         x2 = 129
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#         return img, text_list
#     elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_tag_png_path):
#         symbol = cv2.imread(clan_tag_png_path, cv2.IMREAD_UNCHANGED)
#         symbol = cv2.resize(symbol, None, fx=0.818, fy=0.818)
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#         return img, text_list
#     elif response == {}:
#         return img, text_list
#     elif response['stage'] == {}:
#         cvc_png_path = os.path.join(plugin_path, 'png', 'clan', '{}-{}-normal.png'.format(
#             response['league'], 
#             response['division'])
#         )
#         cvc_png = cv2.imread(cvc_png_path, cv2.IMREAD_UNCHANGED)
#         cvc_png = cv2.resize(cvc_png, None, fx=0.824, fy=0.824)
#         x2 = x1 + cvc_png.shape[1]
#         y2 = y1 + cvc_png.shape[0]
#         img = Picture.merge_img(img, cvc_png, y1, y2, x1, x2)
#         division_rating = str(response['division_rating'])
#         fontStyle = fonts.data[1][55]
#         w = Picture.x_coord(division_rating, fontStyle)
#         text_list.append(
#             Text_Data(
#                 xy=(x1+210-w/2, y1+344),
#                 text=division_rating,
#                 fill=(230, 230, 230),
#                 font_index=1,
#                 font_size=55
#             )
#         )
#         return img, text_list
#     else:
#         cvc_png_path = os.path.join(plugin_path, 'png', 'clan', '{}-{}-{}.png'.format(
#             response['league'], 
#             response['division'],
#             response['stage']['type']
#             )
#         )
#         cvc_png = cv2.imread(cvc_png_path, cv2.IMREAD_UNCHANGED)
#         cvc_png = cv2.resize(cvc_png, None, fx=0.824, fy=0.824)
#         x2 = x1 + cvc_png.shape[1]
#         y2 = y1 + cvc_png.shape[0]
#         img = Picture.merge_img(img, cvc_png, y1, y2, x1, x2)
#         victory_png_path = os.path.join(plugin_path, 'png', 'clan', 'victory.png')
#         defeat_png_path = os.path.join(plugin_path, 'png', 'clan', 'defeat.png')
#         victory_png = cv2.imread(victory_png_path, cv2.IMREAD_UNCHANGED)
#         victory_png = cv2.resize(victory_png, None, fx=0.824, fy=0.824)
#         defeat_png = cv2.imread(defeat_png_path, cv2.IMREAD_UNCHANGED)
#         defeat_png = cv2.resize(defeat_png, None, fx=0.824, fy=0.824)
#         i = 0
#         for index in response['stage']['progress']:
#             if index == 'victory':
#                 x2 = int(x1 + 76.6 + 56.85*i)
#                 y2 = y1 + 351
#                 x3 = x2 + victory_png.shape[1]
#                 y3 = y2 + victory_png.shape[0]
#                 img = Picture.merge_img(img, victory_png, y2, y3, x2, x3)
#             else:
#                 x2 = int(x1 + 76.6 + 56.85*i)
#                 y2 = y1 + 351
#                 x3 = x2 + defeat_png.shape[1]
#                 y3 = y2 + defeat_png.shape[0]
#                 img = Picture.merge_img(img, defeat_png, y2, y3, x2, x3)
#             i += 1
#         del victory_png
#         del defeat_png
#         return img, text_list

# def clan_tag_2(
#     img,
#     cid: str,
#     text_list: list,
#     x1: int = 1912,
#     y1: int = 131
# ):
#     clan_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_tag', f'{cid}.png')
#     clan_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_bg', f'{cid}.png')
#     if Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_bg_png_path):
#         symbol = cv2.imread(clan_bg_png_path, cv2.IMREAD_UNCHANGED)
#         x1 = 98
#         x2 = 129
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_tag_png_path):
#         symbol = cv2.imread(clan_tag_png_path, cv2.IMREAD_UNCHANGED)
#         symbol = cv2.resize(symbol, None, fx=0.818, fy=0.818)
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     return img, text_list