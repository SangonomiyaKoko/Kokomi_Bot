import os
import json

from ..config import CONFIG_DIR


class ReadVersionFile:
    @classmethod
    def read_version(cls):
        "读取本地文件中的代码版本"
        try:
            package_json_path = os.path.join(CONFIG_DIR, 'package.json')
            temp = open(package_json_path, "r", encoding="utf-8")
            package_json = json.load(temp)
            temp.close()
            return package_json.get('version')
        except:
            return None