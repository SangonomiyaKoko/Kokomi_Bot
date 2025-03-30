# import os
# from PIL import Image
# from typing_extensions import TypedDict

# from ..config import ASSETS_DIR, bot_settings
# from ..logs import logging
# from ..api import BaseAPI, Mock
# from ..logs import ExceptionLogger
# from ..common import (
#     Utils, GameData, ThemeTextColor, ThemeRatingColor, TimeFormat
# )
# from ..image import (
#     Text_Data, Box_Data, Picture, Insignias, font_manager
# )
# from ..schemas import (
#     KokomiUser, UserBasicDict, UserClanDict, UserSignatureDict
# )


# class SignatureDict(TypedDict):
#     random: UserSignatureDict
#     ranked: UserSignatureDict

# class UserBaseResult(TypedDict):
#     user: UserBasicDict
#     clan: UserClanDict
#     statistics: SignatureDict


# @ExceptionLogger.handle_program_exception_async
# async def main(
#     user: KokomiUser
# ) -> dict:
#     path = '/api/v1/robot/user/account/'
#     params = {
#         'region': Utils.get_region_by_id(user.bind.region_id),
#         'account_id': user.bind.account_id,
#         'game_type': 'signature',
#         'language': Utils.get_language(user.local.language)
#     }
#     if user.local.algorithm:
#         params['algo_type'] = user.local.algorithm
#     if bot_settings.USE_MOCK:
#         result = Mock.read_data('signature.json')
#         logging.debug('Using MOCK, skip network requests')
#     else:
#         result = await BaseAPI.get(
#             path=path,
#             params=params
#         )
#     if 2000 <= result['code'] <= 9999:
#         logging.error(f"API Error, Error: {result['message']}")
#         return result
#     if result['code'] != 1000:
#         return result
#     res_img = get_png(
#         user=user,
#         result=result['data']
#     )
#     result = Picture.return_img(img=res_img)
#     del res_img
#     return result

# @TimeFormat.cost_time_sync(message='Image generation completed')
# def get_png(
#     user: KokomiUser,
#     result: UserBaseResult
# ) -> str:
#     # 画布宽度和高度
#     width, height = 1400, 518
#     # 背景颜色（RGB）
#     background_color = Picture.hex_to_rgb(user.local.background, 0)
#     # 创建画布
#     canvas = Image.new("RGBA", (width, height), background_color)
#     # TODO: 叠加主题背景

#     # 叠加图片主体
#     content_png_path = os.path.join(ASSETS_DIR, 'content', 'default', user.local.language, 'signature.png')
#     content_png = Image.open(content_png_path)
#     canvas.alpha_composite(content_png, (0, 0))
#     # TODO: 叠加图片主题图片
    
#     res_img = canvas
#     del canvas
#     # 获取不同主题的文字颜色
#     theme_text_color = ThemeTextColor('dark')
#     # 获取不同主题的评分颜色
#     theme_rating_color = ThemeRatingColor('dark')
#     # 需要叠加的 文字/矩形
#     text_list = []
#     box_list = []

#     if result['clan']['id'] != None:
#         name = '['+str(result['clan']['tag'])+']  ' + result['user']['name']
#     else:
#         name = result['user']['name']
#     text_list.append(
#         Text_Data(
#             xy=(31, 30),
#             text=name,
#             fill=theme_text_color.TextThemeColor1,
#             font_index=1,
#             font_size=35
#         )
#     )
#     i = 0
#     fontStyle = font_manager.get_font(2,30)
#     for battle_type in ['random', 'ranked']:
#         temp_data: UserSignatureDict = result['statistics'][battle_type]
#         battles_count = temp_data['battles_count']
#         avg_win = temp_data['win_rate']
#         avg_damage = temp_data['avg_damage']
#         avg_frag = temp_data['avg_frags']
#         avg_pr = temp_data['rating']
#         win_rate_color = theme_rating_color.get_class_color(temp_data['win_rate_class'])
#         avg_damage_color = theme_rating_color.get_class_color(temp_data['avg_damage_class'])
#         avg_frags_color = theme_rating_color.get_class_color(temp_data['avg_frags_class'])
#         avg_pr_color = theme_rating_color.get_class_color(temp_data['rating_class'])
#         w = Picture.x_coord(battles_count, fontStyle)
#         text_list.append(
#             Text_Data(
#                 xy=(311-w/2+171*i, 311+35*0),
#                 text=battles_count,
#                 fill=theme_text_color.TextThemeColor1,
#                 font_index=2,
#                 font_size=30
#             )
#         )
#         w = Picture.x_coord(avg_win, fontStyle)
#         text_list.append(
#             Text_Data(
#                 xy=(311-w/2+171*i, 311+35*1),
#                 text=avg_win,
#                 fill=win_rate_color,
#                 font_index=2,
#                 font_size=30
#             )
#         )
#         w = Picture.x_coord(avg_damage, fontStyle)
#         text_list.append(
#             Text_Data(
#                 xy=(311-w/2+171*i, 311+35*2),
#                 text=avg_damage,
#                 fill=avg_damage_color,
#                 font_index=2,
#                 font_size=30
#             )
#         )
#         w = Picture.x_coord(avg_frag, fontStyle)
#         text_list.append(
#             Text_Data(
#                 xy=(311-w/2+171*i, 311+35*3),
#                 text=avg_frag,
#                 fill=avg_frags_color,
#                 font_index=2,
#                 font_size=30
#             )
#         )
#         w = Picture.x_coord(avg_pr, fontStyle)
#         text_list.append(
#             Text_Data(
#                 xy=(311-w/2+171*i, 311+35*4),
#                 text=avg_pr,
#                 fill=avg_pr_color,
#                 font_index=2,
#                 font_size=30
#             )
#         )
#         i += 1

#     # 完成文字和矩形的叠加
#     res_img = Picture.add_box(box_list, res_img)
#     res_img = Picture.add_text(text_list, res_img)
#     res_img_size = res_img.size
#     # 缩小图片大小
#     # res_img = res_img.resize(
#     #     (
#     #         int(res_img_size[0]*0.5), 
#     #         int(res_img_size[1]*0.5)
#     #     )
#     # )
#     return res_img


            


