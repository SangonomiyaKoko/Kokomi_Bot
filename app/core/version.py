import json

from .path import PROJECT_ROOT

def read_version():
    "读取本地文件中的代码版本"
    path = PROJECT_ROOT / 'package.json'
    if not path.exists():
        raise FileNotFoundError("The `package.json` file does not exist.")
    with open(path, "r", encoding="utf-8") as f:
        package_json = json.load(f)
        return package_json.get('version', 'Unknown')