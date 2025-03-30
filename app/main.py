from .scripts.api import BindAPI, BasicAPI
from .scripts.logs import logging, message_logger
from .scripts.language import Message
from .scripts.common import ReadVersionFile
from .scripts.command import select_func
from .scripts.db import UserLocalManager
from .permission import get_user_level
from .scripts.schemas import (
    KokomiUser, Platform, UserBasic
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
        message_logger.debug(f"Receive | FROM={kokomi_user.platform.name.upper()} UID={kokomi_user.basic.id} MSG=\'{message}\'")
        # 以下为Bot的中间件0
        user_level = get_user_level(kokomi_user.basic.cid)
        kokomi_user.set_user_level(user_level)
        # 获取用户的本地数据库信息
        user_local = UserLocalManager.get_user_local(kokomi_user)
        if user_local['code'] != 1000:
            # 获取用户本地信息失败
            return self.__process_result(
                kokomi_user = kokomi_user,
                language = kokomi_user.local.language,
                result = user_local
            )
        else:
            kokomi_user.set_user_local(user_local['data'])
        logging.debug(str(user_local['data']))
        # 指令解析
        select_result = await select_func(kokomi_user, message)
        if select_result['status'] == 'error':
            logging.error(str(select_result))
        if select_result['code'] == 1000:
            generate_func = select_result['data']['callback_func']
            requires_binding = select_result['data']['requires_binding']
            # 需要绑定但是没有查询账号的信息则去请求绑定数据
            if requires_binding and not kokomi_user.check_user_bind():
                user_bind = await BindAPI.get_user_bind(kokomi_user)
                if user_bind['code'] != 1000:
                    # 获取用户绑定信息失败
                    return self.__process_result(
                        kokomi_user = kokomi_user,
                        language = kokomi_user.local.language,
                        result = user_bind
                    )
                elif user_bind['data']:
                    kokomi_user.set_user_bind(user_bind['data'])
                logging.debug(str(user_bind['data']))
            # 调用相关resources的函数，请求接口获取数据或生成图片
            generate_result = await generate_func(
                user = kokomi_user,
                **select_result['data']['extra_kwargs']
            )
            logging.debug(str(generate_result))
            return self.__process_result(
                kokomi_user = kokomi_user,
                language = kokomi_user.local.language,
                result = generate_result
            )
        else:
            return self.__process_result(
                kokomi_user = kokomi_user,
                language = kokomi_user.local.language,
                result = select_result
            )

    def __process_result(self, kokomi_user: KokomiUser, language: str, result: dict):
        if result['code'] == 1000:
            # 正常结果，返回图片
            message_logger.debug(f"Return | TO={kokomi_user.platform.name.upper()} UID={kokomi_user.basic.id} RID={kokomi_user.bind.region_id} MSG=Image")
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
            message_logger.debug(f"Return | TO={kokomi_user.platform.name.upper()} UID={kokomi_user.basic.id} RID={kokomi_user.bind.region_id} MSG=\'{msg}\'")
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
            current_code_version = ReadVersionFile.read_version()
            if not current_code_version:
                raise ValueError("The code version cannot be read from the file.")
            logging.info(f"The current version of the code: {current_code_version}")
            if least_code_version != current_code_version:
                logging.warning("The current version code has been updated.")
                logging.warning(f"The latest version: {least_code_version}")
                logging.warning("The latest code repository: https://github.com/SangonomiyaKoko/Kokomi_Bot")