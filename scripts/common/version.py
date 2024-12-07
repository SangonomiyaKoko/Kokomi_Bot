import re
import os

from scripts.config import ASSETS_DIR, SCRIPTS_DIR


class ReadVersionFile:
    @classmethod
    def read_code_version(cls):
        "读取本地version文件中的代码版本"
        try:
            with open(os.path.join(SCRIPTS_DIR, 'version'), "r", encoding="utf-8") as file:
                version = file.read()
            return cls.extract_variable_regex(version, 'kokomibot-','-code')
        except:
            return None
        
    @classmethod
    def read_image_version(cls):
        "读取本地version文件中的图片版本"
        try:
            with open(os.path.join(ASSETS_DIR, 'version'), "r", encoding="utf-8") as file:
                version = file.read()
            return cls.extract_variable_regex(version, 'kokomibot-','-image')
        except:
            return None

    def extract_variable_regex(text, start, end):
        "使用正则表达式提取固定开头和结尾之间的内容"
        pattern = re.escape(start) + "(.*?)" + re.escape(end)
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None