import re
import os

from ..config.setting import ASSETS_DIR, SCRIPTS_DIR

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