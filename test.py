import asyncio
from datetime import datetime
import sys

sys.path.append(r'F:\Kokomi_PJ_Bot')


from scripts.main import KokomiBot

kokomi_sign = '''
┌───────────────────────────────────────────────────────────────┐
|       _  __     _                   _   ____        _         |
|      | |/ /___ | | _____  _ __ ___ (_) | __ )  ___ | |_       | 
|      | ' // _ \| |/ / _ \| '_ ` _ \| | |  _ \ / _ \| __|      |
|      | . \ (_) |   < (_) | | | | | | | | |_) | (_) | |_       |
|      |_|\_\___/|_|\_\___/|_| |_| |_|_| |____/ \___/ \__|      |
|                                                               |
└───────────────────────────────────────────────────────────────┘
>  @Author: Maoyu
>  @E-mail: maoy6665@gmail.com
>  @Github: https://github.com/SangonomiyaKoko/Kokomi_Bot
'''
def log_format():
    green = '\033[32m'
    reset = '\033[0m'
    blue = '\033[34m'
    now_time = datetime.now().strftime("%m-%d %H:%M:%S")
    return f"{green}{now_time}{reset} [INFO] {blue}kokomibot{reset} | "

async def main():
    print(kokomi_sign)
    # 初始化bot并检查bot更新
    await KokomiBot.init_bot()
    try:
        platform_type = 'qq'
        print(log_format() + "Default platform: QQ")
        user_id = input(log_format() + "Please enter ID >>> ")
        print(log_format() + "Pleasa enter command or enter `quit` to exit.")
        while True:
            message = input(log_format() + ">>> ")
            if message == 'quit':
                break
            if not message:
                continue
            user_data = {
                'id': user_id,
                'name': None,
                'avatar': None
            }
            platform_data = {
                'type': platform_type,
                'id': None,
                'cid': None,
                'name': None,
                'avatar': None,
                'users': None
            }
            await KokomiBot.main(
                message=message,
                user=user_data,
                platform=platform_data
            )
        print(log_format() + "程序已退出")
    except KeyboardInterrupt:
        print("\n" + log_format() + "程序已退出")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())