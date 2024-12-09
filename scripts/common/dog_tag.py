import os
from PIL import Image

special_clan_id = []

dir_list = [
    'PCNA001', 
    'PCNA002', 
    'PCNA003', 
    'PCNA004', 
    'PCNA005', 
    'PCNA006', 
    'PCNA007', 
    'PCNA008', 
    'PCNA009'
]

def dog_tag_2(
    img,
    aid: str,
    cid: str,
    server: str,
    response: dict,
    x1: int = 1912,
    y1: int = 129
):
    dog_tag_data = Game_Data.load_dog_tag_data(server=server)
    background_id = dog_tag_data.get(str(response['background_id']), None)
    symbol_id = dog_tag_data.get(str(response['symbol_id']), None)
    if (
        (
            background_id == None and 
            symbol_id == None
        ) or (
            background_id != None and 
            symbol_id == None
        )
    ):
        return img
    if cid is None:
        cid = 'None'
    user_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'user_tag', f'{aid}.png')
    user_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'user_bg', f'{aid}.png')
    clan_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_tag', f'{cid}.png')
    clan_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_bg', f'{cid}.png')
    if server == 'ru':
        server = 'lesta'
    else:
        server = 'wg'

    if Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(user_bg_png_path):
        symbol = Image.open(user_bg_png_path)
        img.alpha_composite(symbol, (98,129))
        del symbol
    elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(user_tag_png_path):
        symbol = Image.open(user_tag_png_path)
        symbol = symbol.resize((419, 419))
        img.alpha_composite(symbol, (x1, y1))
        del symbol
    elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_bg_png_path) and cid not in special_clan_id:
        symbol = Image.open(clan_bg_png_path)
        img.alpha_composite(symbol, (98,129))
        del symbol
    elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_tag_png_path) and cid not in special_clan_id:
        symbol = Image.open(clan_tag_png_path)
        symbol = symbol.resize((419, 419))
        img.alpha_composite(symbol, (x1, y1))
        del symbol
    elif background_id in dir_list:
        if symbol_id == None:
            return img
        texture_id = dog_tag_data[str(response['texture_id'])][6:]
        background_color_id = Game_Data.background_color[str(response['background_color_id'])]
        background_png_path = os.path.join(plugin_path , 'png', 'dog_tag_2', f'{background_id}_background_{texture_id}_{background_color_id}.png')
        background = Image.open(background_png_path).convert('RGBA')
        background = background.resize((419, 419))
        img.alpha_composite(background, (x1, y1))
        del background
        border_color_id = Game_Data.border_color[str(
            response['border_color_id'])]
        border_png_path = os.path.join(plugin_path , 'png', 'dog_tag_2', f'{background_id}_border_{border_color_id}.png')
        border = Image.open(border_png_path).convert('RGBA')
        border = border.resize((419, 419))
        img.alpha_composite(border, (x1, y1))
        del border
        symbol_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{symbol_id}.png')
        symbol = Image.open(symbol_png_path).convert('RGBA')
        symbol = symbol.resize((419, 419))
        img.alpha_composite(symbol, (x1, y1))
        del symbol
    elif background_id == None and symbol_id != None:
        symbol_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{symbol_id}.png')
        symbol = Image.open(symbol_png_path).convert('RGBA')
        symbol = symbol.resize((419, 419))
        img.alpha_composite(symbol, (x1, y1))
        del symbol
    else:
        background_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{background_id}.png')
        background = Image.open(background_png_path).convert('RGBA')
        background = background.resize((419, 419))
        img.alpha_composite(background, (x1, y1))
        del background
        symbol_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{symbol_id}.png')
        symbol = Image.open(symbol_png_path).convert('RGBA')
        symbol = symbol.resize((419, 419))
        img.alpha_composite(symbol, (x1, y1))
        del symbol
    return img

# def dog_tag(
#     img,
#     aid: str,
#     cid: str,
#     server: str,
#     response: dict,
#     x1: int = 1912,
#     y1: int = 129
# ):
#     dog_tag_data = Game_Data.load_dog_tag_data(server=server)
#     background_id = dog_tag_data.get(str(response['background_id']), None)
#     symbol_id = dog_tag_data.get(str(response['symbol_id']), None)
#     if (
#         (
#             background_id == None and 
#             symbol_id == None
#         ) or (
#             background_id != None and 
#             symbol_id == None
#         )
#     ):
#         return img
#     if cid is None:
#         cid = 'None'
#     user_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'user_tag', f'{aid}.png')
#     user_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'user_bg', f'{aid}.png')
#     clan_tag_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_tag', f'{cid}.png')
#     clan_bg_png_path = os.path.join(plugin_path, 'png', 'dog_tag_custom', 'clan_bg', f'{cid}.png')
#     if server == 'ru':
#         server = 'lesta'
#     else:
#         server = 'wg'

#     if Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(user_bg_png_path):
#         symbol = cv2.imread(user_bg_png_path, cv2.IMREAD_UNCHANGED)
#         x1 = 98
#         x2 = 129
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(user_tag_png_path):
#         symbol = cv2.imread(user_tag_png_path, cv2.IMREAD_UNCHANGED)
#         symbol = cv2.resize(symbol, None, fx=0.818, fy=0.818)
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_bg_png_path) and cid not in special_clan_id:
#         symbol = cv2.imread(clan_bg_png_path, cv2.IMREAD_UNCHANGED)
#         x1 = 98
#         x2 = 129
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     elif Plugin_Config.SHOW_CUSTOM_TAG is True and os.path.exists(clan_tag_png_path) and cid not in special_clan_id:
#         symbol = cv2.imread(clan_tag_png_path, cv2.IMREAD_UNCHANGED)
#         symbol = cv2.resize(symbol, None, fx=0.818, fy=0.818)
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     elif background_id in dir_list:
#         if symbol_id == None:
#             return img
#         texture_id = dog_tag_data[str(response['texture_id'])][6:]
#         background_color_id = Game_Data.background_color[str(response['background_color_id'])]
#         background_png_path = os.path.join(plugin_path , 'png', 'dog_tag_2', f'{background_id}_background_{texture_id}_{background_color_id}.png')
#         background = cv2.imread(background_png_path, cv2.IMREAD_UNCHANGED)
#         background = cv2.resize(background, None, fx=0.818, fy=0.818)
#         x2 = x1 + background.shape[1]
#         y2 = y1 + background.shape[0]
#         img = Picture.merge_img(img, background, y1, y2, x1, x2)
#         del background
#         border_color_id = Game_Data.border_color[str(
#             response['border_color_id'])]
#         border_png_path = os.path.join(plugin_path , 'png', 'dog_tag_2', f'{background_id}_border_{border_color_id}.png')
#         border = cv2.imread(border_png_path, cv2.IMREAD_UNCHANGED)
#         border = cv2.resize(border, None, fx=0.818, fy=0.818)
#         x2 = x1 + border.shape[1]
#         y2 = y1 + border.shape[0]
#         img = Picture.merge_img(img, border, y1, y2, x1, x2)
#         del border
#         symbol_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{symbol_id}.png')
#         symbol = cv2.imread(symbol_png_path, cv2.IMREAD_UNCHANGED)
#         symbol = cv2.resize(symbol, None, fx=0.818, fy=0.818)
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     elif background_id == None and symbol_id != None:
#         symbol_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{symbol_id}.png')
#         symbol = cv2.imread(symbol_png_path, cv2.IMREAD_UNCHANGED)
#         symbol = cv2.resize(symbol, None, fx=0.818, fy=0.818)
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     else:
#         background_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{background_id}.png')
#         background = cv2.imread(background_png_path, cv2.IMREAD_UNCHANGED)
#         background = cv2.resize(background, None, fx=0.818, fy=0.818)
#         x2 = x1 + background.shape[1]
#         y2 = y1 + background.shape[0]
#         img = Picture.merge_img(img, background, y1, y2, x1, x2)
#         del background
#         symbol_png_path = os.path.join(plugin_path , 'png', f'dog_tag_{server}', f'{symbol_id}.png')
#         symbol = cv2.imread(symbol_png_path, cv2.IMREAD_UNCHANGED)
#         symbol = cv2.resize(symbol, None, fx=0.818, fy=0.818)
#         x2 = x1 + symbol.shape[1]
#         y2 = y1 + symbol.shape[0]
#         img = Picture.merge_img(img, symbol, y1, y2, x1, x2)
#         del symbol
#     return img