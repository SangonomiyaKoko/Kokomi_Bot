import asyncio
# import sys
import time
from datetime import datetime

# sys.path.append(r'F:\Kokomi_PJ_Bot')


from app import KokomiBot, Platform, UserBasic

check_memory = True  # 用于检查是否有内存泄漏问题

if check_memory:
    import psutil
    import os
    pid = os.getpid()
    process = psutil.Process(pid)

def get_memory_usage():
    # 获取当前进程的内存使用信息
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # 转换为 MB

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
  /test                               Test
  /link <region> <ign>                Link to your game account
  /me                                 Overall 
  /set language <cn/en/ja>            Change language
  /set rating <show/hide>             Show or hide personal rating
'''


reset = '\033[0m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
pin = '\033[35m'
qin = '\033[36m'

def log_format():
    now_time = datetime.now().strftime("%m-%d %H:%M:%S")
    return f"{green}{now_time}{reset} [INFO] {blue}kokomibot{reset} | "

async def main():
    print(kokomi_sign)
    kokomi_bot = KokomiBot()
    # 初始化bot并检查bot更新
    await kokomi_bot.init_bot()
    try:
        platform_type = 'qq_bot'
        print(log_format() + "Default platform: " + platform_type.upper())
        user_id = input(log_format() + "Please enter ID >>> ")
        print(log_format() + "Enter `help` to show help or enter `quit` to exit.")
        while True:
            message = input(log_format() + f"{blue}[INPUT]{reset} >>> ")
            if message == 'help':
                print(help_message)
                continue
            if message == 'quit':
                break
            if not message:
                continue
            user = UserBasic(user_id,user_id)
            platform = Platform(platform_type, 123, 123)
            start_time = time.time()
            return_result = await kokomi_bot.main(
                message=message,
                user=user,
                platform=platform
            )
            end_time = time.time()
            if return_result['type'] == 'img':
                print(log_format() + f"{green}[RETURN]{reset} PIC: " + return_result['data'])
            else:
                print(log_format() + f"{green}[RETURN]{reset} MSG: " + return_result['data'])
            print(log_format() + f"{pin}[TIME]{reset} Total cost time: {round(end_time-start_time,2)}s")
            if check_memory:
                memory_usage = get_memory_usage()
                print(log_format() + f"{qin}[DEBUG]{reset} Memory usage: {memory_usage:.2f} MB")
        print(log_format() + "Program quit")
    except KeyboardInterrupt:
        print("\n" + log_format() + "Program quit")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())