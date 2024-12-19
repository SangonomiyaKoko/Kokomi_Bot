from scripts.api import BindAPI, BasicAPI
from scripts.logs import logging
from scripts.language import Message
from scripts.select_func import SelectFunc
from scripts.schemas import (
    KokomiUser, Platform, UserBasic
)
from scripts.common import (
    UserLocalDB,
    ReadVersionFile
)


class KokomiBot:
    async def main(
        self,
        message: str,
        user: UserBasic,
        platform: Platform
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
        kokomi_user = KokomiUser(platform,user)
        user_binding_status = False
        logging.debug(f"Receive a message from {kokomi_user.platform.name}-{kokomi_user.basic.id} [{message}]")
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
        user_bind = await BindAPI.get_user_bind(kokomi_user)
        logging.debug(str(user_bind))
        user_local = UserLocalDB.get_user_local(kokomi_user)
        logging.debug(str(user_local))
        if user_bind['code'] != 1000:
            # 获取用户绑定信息失败
            return self.__process_result(
                language = kokomi_user.local.language,
                result = user_bind
            )
        elif user_bind['data']:
            user_binding_status = True
            kokomi_user.bind.set_user_bind(user_bind['data'])
        else:
            user_binding_status = False
        if user_local['code'] != 1000:
            # 获取用户本地信息失败
            return self.__process_result(
                language = kokomi_user.local.language,
                result = user_local
            )
        else:
            kokomi_user.local.set_user_local(user_local['data'])

        select_func_dict = {
            'cn': SelectFunc.main,
            'en': SelectFunc.main,
            'ja': SelectFunc.main
        }
        select_func = select_func_dict[kokomi_user.local.language]
        user_binding_status = True if user_bind['data'] else False
        select_result = select_func(user_binding_status, message_list)
        if select_result['code'] == 1000:
            generate_func = select_result['data']['callback_func']
            generate_result = await generate_func(
                user = kokomi_user,
                **select_result['data']['extra_kwargs']
            )
            logging.debug(str(generate_result))
            return self.__process_result(
                language = kokomi_user.local.language,
                result = generate_result
            )
        else:
            return self.__process_result(
                language = kokomi_user.local.language,
                result = select_result
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
        least_version = await BasicAPI.get_bot_version()
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
