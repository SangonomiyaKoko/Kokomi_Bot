from scripts.api import BindAPI
from scripts.logs import logging
from scripts.language import Message
from scripts.select_func import SelectFunc
from scripts.schemas import UserInfoDict, PlatformDict
from scripts.common import (
    Utils,
    UserLocal,
    JSONResponse,
    ReadVersionFile
)


class KokomiBot:
    async def main(
        self,
        message: str,
        user_info: UserInfoDict,
        platform: PlatformDict
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
        default_language = Utils.get_default_language(platform)
        logging.debug(f"Receive a message from {platform['type']}-{user_info['id']} [{message}]")
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
        # user_bind = await BindAPI.get_user_bind(
        #     platform = platform['type'],
        #     user = user_info['id']
        # )
        user_bind = {
            'status': 'ok',
            'code': 1000,
            'message': 'SUccess',
            'data': {
                'region_id': 1,
                'account_id': 2023619512,
            }
        }
        # user_local = UserLocal.get_user_local(
        #     platform = platform['type'],
        #     user = user_info['id']
        # )
        user_local = {
            'status': 'ok',
            'code': 1000,
            'message': 'SUccess',
            'data': {
                'language': 'ja',
                'algorithm': 'pr',
                'background': '#313131',
                'content': 'dark',
                'theme': 'default'
            }
        }
        if user_bind['code'] != 1000:
            # 获取用户绑定信息失败
            return self.__process_result(
                language = default_language,
                result = user_bind
            )
        if user_local['code'] != 1000:
            # 获取用户本地信息失败
            return self.__process_result(
                language = default_language,
                result = user_local
            )
        # 获取用户绑定信息成功
        if user_bind['data'] == None:
            # 用户没有绑定数据，提示用户绑定账号
            user_bind = JSONResponse.API_9001_UserNotLinked
            return self.__process_result(
                language = default_language,
                result = user_bind
            )
        select_func_dict = {
            'cn': SelectFunc.main,
            'en': SelectFunc.main,
            'ja': SelectFunc.main
        }
        select_func = select_func_dict[user_local['data']['language']]
        select_result = select_func(message_list = message_list)
        if select_result:
            generate_func = select_result['callback_func']
            generate_result = await generate_func(
                platform = platform,
                user_info = user_info,
                user_bind = user_bind['data'],
                user_local = user_local['data'],
                **select_result['extra_kwargs']
            )
            logging.debug(str(generate_result))
            return self.__process_result(
                language = user_local['data']['language'],
                result = generate_result
            )
        else:
            return self.__process_result(
                language = user_local['data']['language'],
                result = JSONResponse.API_9002_FuncNotFound
            )

    def __process_result(self, language: str, result: dict):
        if result['code'] == 1000:
            # 正常结果，返回图片
            return {
                'type': 'img',
                'data': result['data']['img']
            }
        else:
            # 正常结果，返回文字
            msg = Message.return_message(
                language = language,
                result = result
            )
            return {
                'type': 'msg',
                'data': msg
            }

    async def init_bot(self):
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
