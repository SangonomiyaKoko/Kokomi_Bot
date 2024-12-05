import os
import re

from api import BasicAPI
from logs import logging
from scripts.config.setting import BotConfig, SCRIPTS_DIR

async def init_bot():
    # 检查当前bot的版本
    least_version = await BasicAPI.get_bot_version()
    if least_version['code'] == 8000:
        logging.warning("The server is currently under maintenance.")
    elif least_version['code'] != 1000:
        logging.warning("An error occurred while obtaining the latest version.")
        logging.error(f"ErrorCode: {least_version['code']},ErrorMsg: {least_version['message']}")
    else:
        code_version = least_version['data']['code']
        if code_version != BotConfig.VERSON:
            logging.warning("The current version code has been updated.")
            logging.warning(f"The latest version: {code_version}")
            logging.warning("The latest code repository: https://github.com/SangonomiyaKoko/Kokomi_Bot")
        else:
            logging.info("The current version of the code is the latest version.")

def read_code_version():
    with open(os.path.join(SCRIPTS_DIR, 'version'), "r", encoding="utf-8") as file:
        version = file.read()
    return extract_variable_regex(version, 'kokomi-','-code')

def read_image_version():
    ...

def extract_variable_regex(text, start, end):
    "使用正则表达式提取固定开头和结尾之间的内容"
    pattern = re.escape(start) + "(.*?)" + re.escape(end)
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

# 主函数
def main():
    version = read_code_version()
    print(f"当前版本: {version}")
    print("请输入图片的文字内容:")
    print("请输入图片的宽度 (默认为800):")
    width = input(">>> ")
    print("请输入图片的高度 (默认为600):")
    height = input(">>> ")

    # 转换用户输入为整数
    width = int(width) if width.isdigit() else 800
    height = int(height) if height.isdigit() else 600
    # 输出生成结果
    logging.info(f"程序完成,{width}*{height}")

if __name__ == "__main__":
    main()