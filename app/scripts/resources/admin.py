import os
from ..logs import ExceptionLogger
from ..common import (
    TimeFormat, Utils
)
from ..image import (
    ImageDrawManager, ImageHandler, TextOperation as Text, RectangleOperation as Rectangle
)
from ..schemas import KokomiUser
from ..config import ASSETS_DIR


@ExceptionLogger.handle_program_exception_async
async def main(user: KokomiUser) -> dict:
    result = {} # 用于图片渲染的数据
    # 完成以下部分的代码
    # TODO: 通过相关接口获取cpu、mem数据，直接问gpt
    # 平台名称可以通过user.platform.name获取
    # bot版本可以从from .scripts.common import ReadVersionFile获取
    # 关于bot的今日请求数据，是通过bot的log文件获取，log文件按日期储存，直接读取当日文件然后遍历即可
    '''
    日志文件会自动记录在log\message\YYYY-MM-DD.log文件内，示例如下
    19:39:41 [MSG] | {'type': 1, 'cid': 123, 'uid': '1', 'msg': '/basic'}
    19:39:43 [MSG] | {'type': 0, 'cid': 123, 'uid': '1', 'rid': 1, 'aid': 1234567, 'return': 'img', 'data': 'F:\\xxx\\xxx.png'}
    19:40:10 [MSG] | {'type': 1, 'cid': 123, 'uid': '1', 'msg': '/admin'}
    19:40:11 [MSG] | {'type': 0, 'cid': 123, 'uid': '1', 'rid': None, 'aid': None, 'return': 'img', 'data': 'F:\\xxx\\xxx.png'}
    直接解析|符号后面的字符串获取数据，注意前后的空格

    type：表示收到还是返回数据，1表示收到的消息，0表示返回的消息
    cid：表示群或者频道id
    uid：表示用户id
    rid：表示用户绑定账号的服务器，注意value是可能为None的
    '''
    result = get_png(
        user=user,
        result=result
    )
    return result

@TimeFormat.cost_time_sync(message='Image generation completed')
def get_png(user: KokomiUser, result: dict) -> str:
    background_path = os.path.join(ASSETS_DIR, r'content\other', 'admin.png')
    res_img = ImageHandler.open_image(background_path)
    if type(res_img) == dict:
        return res_img
    # 由于当前功能是admin需要，所以暂时不兼容多语言和主题切换
    # 开始图片渲染流程
    with ImageDrawManager(res_img, 'ps', 300) as image_manager:
        # 完成以下部分的代码
        # TODO: 图片渲染，文字或者矩形渲染
        '''
        示例，关于参数请参考app\scripts\image\generation.py文件的注释
        image_manager.add_text(
            Text(
                text=test_msg,
                position=(0,50),          # ps中文字的坐标
                font_index=1,
                font_size=25,             # ps中文字的size，可能会略小，看效果可以适当加1~2
                color=theme_text_color.TextThemeColor3,
                align='left',
                priority=10
            )
        )
        image_manager.add_rectangle(
            Rectangle(
                position=(x1, y1),
                size=(x2-x1, y2-y1),
                color=box_color
            )
        )
        '''
        image_manager.add_text(
            Text(
                text='12,345',
                position=(75, 148),
                font_index=2,
                font_size=18,
                color=(30, 30, 30)
            )
        )
        image_manager.execute_operations()
        res_img = image_manager.get_image()
        result = ImageHandler.save_image(res_img)
        return result
