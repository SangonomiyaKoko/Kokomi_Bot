#
# KokomiBot.
# $Id$
#
# the Image class wrapper
#
# partial release history:
# 2024-12-30 main   Created
#
#
# See the README file for information on usage and redistribution.
#


# from .scripts.api import BindAPI, BasicAPI
from .loggers import logging, csv_writer
from .core import AppContext, AppInitError, read_version, Config, ASSETS_DIR
from .db import LocalDB
from .response import JSONResponse
from .i18n import I18n, LangStrategyManager
from .models.schemas import (
    KokomiUser, Platform, UserBasic
)

class KokomiBot:
    async def init_bot(self):
        """初始化 Bot 运行环境"""
        # 初始化本地数据库
        LocalDB.init_local_db()
        # 检查当前bot的版本
        current_code_version = read_version()
        logging.debug(f"The current version: {current_code_version}")
        # 校验配置是否加载成功
        if not Config:
            raise AppInitError('Failed to load configuration data')
        # 遍历配置中定义的语言列表
        for lang_code in self.__split_config(Config.bot.language):
            if lang_code not in ['zh_SG', 'en_US']:
                logging.warning(f"Unsupported language code: `{lang_code}`")
                continue
            # 校验对应语言的静态资源目录是否存在
            lang_static_path = ASSETS_DIR / f'media/images/{lang_code}'
            if not lang_static_path.exists():
                logging.warning(f"Missing static assets: `{lang_code}`")
                continue
            # 注册语言包与语言策略
            I18n.register(lang_code)
            LangStrategyManager.register(lang_code)
            # 将语言注册到全局应用上下文
            AppContext.set_languages(lang_code)
            logging.debug(f"Language package `{lang_code}` registered successfully")
        # 设置应用初始化完成状态
        AppContext.set_init_status()
        logging.debug("Initialization successful")

    def get_user_level(self, user_id: str):
        """ 获取用户的权限"""
        if user_id in self.__split_config(Config.bot.root_users):
            return 1
        else:
            return 0

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
        csv_writer(user.id, platform.id, message)
        if not AppContext.InitStatus:
            raise AppInitError('Initialization not completed')
        kokomi_user = KokomiUser(platform,user)
        user_level = self.get_user_level(kokomi_user.basic.cid)
        kokomi_user.set_user_level(user_level)
        user_local = LocalDB.get_user_local(kokomi_user)
        if user_local['code'] != 1000:
            # 获取用户本地信息失败
            return self.__process_result(
                kokomi_user = kokomi_user,
                result = user_local
            )
        else:
            kokomi_user.set_user_local(user_local['data'])
        return self.__process_result(
            kokomi_user = kokomi_user,
            result = JSONResponse.API_6001_TestMessage
        )
        # 指令解析
        # select_result = await select_func(kokomi_user, message)
        # if select_result['status'] == 'error':
        #     logging.error(str(select_result))
        # if select_result['code'] == 1000:
        #     generate_func = select_result['data']['callback_func']
        #     requires_binding = select_result['data']['requires_binding']
        #     # 需要绑定但是没有查询账号的信息则去请求绑定数据
        #     if requires_binding and not kokomi_user.check_user_bind():
        #         user_bind = await BindAPI.get_user_bind(kokomi_user)
        #         if user_bind['code'] != 1000:
        #             # 获取用户绑定信息失败
        #             return self.__process_result(
        #                 kokomi_user = kokomi_user,
        #                 language = kokomi_user.local.language,
        #                 result = user_bind
        #             )
        #         if user_bind['data'] != None:
        #             kokomi_user.set_user_bind(user_bind['data'])
        #         else:
        #             return self.__process_result(
        #                 kokomi_user = kokomi_user,
        #                 language = kokomi_user.local.language,
        #                 result = JSONResponse.API_10003_UserNotBound
        #             )
        #         logging.debug(str(user_bind['data']))
        #     # 调用相关resources的函数，请求接口获取数据或生成图片
        #     generate_result = await generate_func(
        #         user = kokomi_user,
        #         **select_result['data']['extra_kwargs']
        #     )
        #     logging.debug(str(generate_result))
        #     return self.__process_result(
        #         kokomi_user = kokomi_user,
        #         language = kokomi_user.local.language,
        #         result = generate_result
        #     )
            

    def __process_result(self, kokomi_user: KokomiUser, result: dict):
        if result['code'] == 1000:
            # 正常结果，返回图片
            return {
                'type': 'img',
                'data': result['data']['img']
            }
        else:
            # 正常结果，返回文字
            path = f"code.{result['code']}"
            msg = I18n.get(path, kokomi_user.local.language)
            if msg == path:
                msg = f"IDX_Code{result['code']}_{result['message']}"
            return {
                'type': 'msg',
                'data': msg
            }

    def __split_config(self, config_str: str) -> list:
        # Config数据分割
        if not config_str:  # None 或空字符串
            return []
        return config_str.split(":")