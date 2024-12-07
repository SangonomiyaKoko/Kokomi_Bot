from scripts.api import BasicAPI, BindAPI
from scripts.logs import logging
from scripts.common.version import ReadVersionFile
from scripts.common import (
    JSONResponse
)


class KokomiBot:
    async def main(
        message: str = None,
        user: dict = None,
        platform: dict = None
    ):
        '''通过用户输入的参数返回生成的图片

        参数:
            message: 用户输入的指令
            user: 用户数据
            platform: 平台数据

        返回:
            type: 返回的数据的格式img/msg
            data: 返回数据的内容
        '''
        try:
            # 用户输入的消息按照空格切割成list
            message_list = message.split(' ')
            # 删除触发词
            CN_STARTWITH = 'wws'
            EN_STARTWITH = '/'
            if message_list[0] == CN_STARTWITH:
                del message_list[0]
            if EN_STARTWITH == message_list[0]:
                del message_list[0]
            if EN_STARTWITH in message_list[0]:
                message_list[0] = message_list[0].replace(EN_STARTWITH,'')
            user_bind = await BindAPI.get_user_bind(
                platform = platform['type'],
                user = user['id']
            )
            if user_bind['code'] == 1000:
                # 获取用户绑定信息成功
                if user_bind['data'] == None:
                    # 用户没有绑定数据，提示用户绑定数据
                    user_bind = JSONResponse.API_9001_UserNotLinked
                bind_data = {
                    'account_id': None,
                    'region_id': None,
                    'language': None,
                    'algorithm': None
                }
                # 如果用户没有绑定，给出默认的language
                bind_data['language'] = None
                # 获取用户的图片类型
                bind_data['pic_type'] = None
                # TODO: 检查该图片类型是否支持
                # TODO: 根据用户输入的消息获取对应的函数

                return {
                    'type': None,
                    'data': None
                }
            else:
                # 获取用户绑定信息失败
                ...
        except:
            pass

    def process_result(result: dict):
        if result['code'] == 1000:
            # 返回图片
            ...
        elif result['code'] in [2000,3000]:
            # 返回错误图片
            ...
        else:
            # 返回文字
            ...


    async def init_bot():
        # 检查当前bot的版本
        # least_version = await BasicAPI.get_bot_version()
        least_version = {'status': 'ok','code': 1000,'message': 'Success','data': {'code': '5.0.0.bate1', 'image': '5.0.0.bate1'}}
        if least_version['code'] == 8000:
            logging.warning("The server is currently under maintenance.")
        elif least_version['code'] != 1000:
            logging.warning("An error occurred while obtaining the latest version.")
            logging.error(f"ErrorCode: {least_version['code']},ErrorMsg: {least_version['message']}")
        else:
            least_code_version = least_version['data']['code']
            current_code_version = ReadVersionFile.read_code_version()
            if not current_code_version:
                raise Exception("The code version cannot be read from the file.")
            logging.info(f"The current version of the code: {current_code_version}")
            if least_code_version != current_code_version:
                logging.warning("The current version code has been updated.")
                logging.warning(f"The latest version: {least_code_version}")
                logging.warning("The latest code repository: https://github.com/SangonomiyaKoko/Kokomi_Bot")
            least_image_version = least_version['data']['image']
            current_image_version = ReadVersionFile.read_image_version()
            if not current_image_version:
                raise Exception("The image version cannot be read from the file.")
            logging.info(f"The current version of the image: {current_image_version}")
            if least_image_version != current_image_version:
                logging.warning("The current version image has been updated.")
                logging.warning(f"The latest version: {least_image_version}")
                logging.warning("Please download the latest image file")
