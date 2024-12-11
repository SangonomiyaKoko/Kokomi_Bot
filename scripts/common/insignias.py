import os
import json
from PIL import Image

from scripts.config import ASSETS_DIR, bot_settings
from .const import GameData
from .utils import Utils

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


class Insignias:
    def add_user_insignias(
        img: Image,
        region_id: int,
        account_id: str,
        clan_id: str,
        response: str,
        x1: int = 1912,
        y1: int = 129
    ):
        "在图片上叠加徽章或者定制背景"
        operator = Utils.get_operator_by_id(region_id)
        dog_tag_json = os.path.join(ASSETS_DIR, 'json', operator, 'dog_tags.json')
        temp = open(dog_tag_json, "r", encoding="utf-8")
        dog_tag_data = json.load(temp)
        temp.close()
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
        if clan_id is None:
            clan_id = 'None'
        user_tag_png_path = os.path.join(ASSETS_DIR, 'custom', 'user_tag', f'{account_id}.png')
        user_bg_png_path = os.path.join(ASSETS_DIR, 'custom', 'user_bg', f'{account_id}.png')
        clan_tag_png_path = os.path.join(ASSETS_DIR, 'custom', 'clan_tag', f'{clan_id}.png')
        clan_bg_png_path = os.path.join(ASSETS_DIR, 'custom', 'clan_bg', f'{clan_id}.png')
        if bot_settings.SHOW_CUSTOM_TAG is True and os.path.exists(user_bg_png_path):
            symbol = Image.open(user_bg_png_path)
            img.alpha_composite(symbol, (98,129))
            del symbol
        elif bot_settings.SHOW_CUSTOM_TAG is True and os.path.exists(user_tag_png_path):
            symbol = Image.open(user_tag_png_path)
            symbol = symbol.resize((419, 419))
            img.alpha_composite(symbol, (x1, y1))
            del symbol
        elif bot_settings.SHOW_CUSTOM_TAG is True and os.path.exists(clan_bg_png_path) and clan_id not in special_clan_id:
            symbol = Image.open(clan_bg_png_path)
            img.alpha_composite(symbol, (98,129))
            del symbol
        elif bot_settings.SHOW_CUSTOM_TAG is True and os.path.exists(clan_tag_png_path) and clan_id not in special_clan_id:
            symbol = Image.open(clan_tag_png_path)
            symbol = symbol.resize((419, 419))
            img.alpha_composite(symbol, (x1, y1))
            del symbol
        elif background_id in dir_list:
            if symbol_id == None:
                return img
            texture_id = dog_tag_data[str(response['texture_id'])][6:]
            background_color_id = GameData.background_color[str(response['background_color_id'])]
            background_png_name = f'{background_id}_background_{texture_id}_{background_color_id}'
            background_png_path = os.path.join(ASSETS_DIR, r'components\insignias\background', f'{background_png_name}.png')
            background = Image.open(background_png_path).convert('RGBA')
            background = background.resize((419, 419))
            img.alpha_composite(background, (x1, y1))
            del background
            border_color_id = GameData.border_color[str(response['border_color_id'])]
            border_png_name = f'{background_id}_border_{border_color_id}'
            border_png_path = os.path.join(ASSETS_DIR, r'components\insignias\symbol', operator, f'{border_png_name}.png')
            border = Image.open(border_png_path).convert('RGBA')
            border = border.resize((419, 419))
            img.alpha_composite(border, (x1, y1))
            del border
            symbol_png_path = os.path.join(ASSETS_DIR, r'components\insignias\symbol', operator, f'{symbol_id}.png')
            symbol = Image.open(symbol_png_path).convert('RGBA')
            symbol = symbol.resize((419, 419))
            img.alpha_composite(symbol, (x1, y1))
            del symbol
        elif background_id == None and symbol_id != None:
            symbol_png_path = os.path.join(ASSETS_DIR, r'components\insignias\symbol', operator, f'{symbol_id}.png')
            symbol = Image.open(symbol_png_path).convert('RGBA')
            symbol = symbol.resize((419, 419))
            img.alpha_composite(symbol, (x1, y1))
            del symbol
        else:
            background_png_path = os.path.join(ASSETS_DIR, r'components\insignias\symbol', operator, f'{background_id}.png')
            background = Image.open(background_png_path).convert('RGBA')
            background = background.resize((419, 419))
            img.alpha_composite(background, (x1, y1))
            del background
            symbol_png_path = os.path.join(ASSETS_DIR, r'components\insignias\symbol', operator, f'{symbol_id}.png')
            symbol = Image.open(symbol_png_path).convert('RGBA')
            symbol = symbol.resize((419, 419))
            img.alpha_composite(symbol, (x1, y1))
            del symbol
        return img
