import asyncio
import sys
import time
from datetime import datetime

sys.path.append(r'F:\Kokomi_PJ_Bot')


from scripts.main import KokomiBot

kokomi_sign = '''
┌────────────────────────────────────────────────────────────────┐
|       _  __     _                   _    ____        _         |
|      | |/ /___ | | _____  _ __ ___ (_)  | __ )  ___ | |_       | 
|      | ' // _ \| |/ / _ \| '_ ` _ \| |  |  _ \ / _ \| __|      |
|      | . \ (_) |   < (_) | | | | | | |  | |_) | (_) | |_       |
|      |_|\_\___/|_|\_\___/|_| |_| |_|_|  |____/ \___/ \__|      |
|                                                                |
└────────────────────────────────────────────────────────────────┘
>  @Author: Maoyu
>  @E-mail: maoy6665@gmail.com
>  @Github: https://github.com/SangonomiyaKoko/Kokomi_Bot
'''

help_message = '''
Usage:
  <start> <command> [params]

Commands:
  /link <region> <ign>
  /link <uid>
'''
def log_format():
    green = '\033[32m'
    reset = '\033[0m'
    blue = '\033[34m'
    now_time = datetime.now().strftime("%m-%d %H:%M:%S")
    return f"{green}{now_time}{reset} [INFO] {blue}kokomibot{reset} | "

async def main():
    print(kokomi_sign)
    kokomi_bot = KokomiBot()
    # 初始化bot并检查bot更新
    await kokomi_bot.init_bot()
    try:
        platform_type = 'qq'
        print(log_format() + "Default platform: QQ")
        user_id = input(log_format() + "Please enter ID >>> ")
        print(log_format() + "Enter `help` to show help or enter `quit` to exit.")
        while True:
            message = input(log_format() + "[INPUT] >>> ")
            if message == 'help':
                print(help_message)
                continue
            if message == 'quit':
                break
            if not message:
                continue
            user_data = {
                'id': user_id,
                'cid': None,
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
            start_time = time.time()
            return_result = await kokomi_bot.main(
                message=message,
                user_info=user_data,
                platform=platform_data
            )
            end_time = time.time()
            if return_result['type'] == 'img':
                print(log_format() + "[RETURN] PIC: " + return_result['data'])
            else:
                print(log_format() + "[RETURN] MSG: " + return_result['data'])
            print(log_format() + f"[TIME] Total cost time: {round(end_time-start_time,2)}s")
        print(log_format() + "Program quit")
    except KeyboardInterrupt:
        print("\n" + log_format() + "Program quit")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())