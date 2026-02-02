import json

from ..core import ASSETS_DIR


class I18n:
    _lang_cache = {}

    @classmethod
    def register(cls, lang_code: str):
        """
        注册语言文件，将对应 JSON 文件加载到缓存中。

        参数:
            lang_code (str): 语言代码，例如 "en-US"、"zh-SG"
        """
        file_path = ASSETS_DIR / f"locales/{lang_code}.json"
        with open(file_path, encoding="utf-8") as f:
            cls._lang_cache[lang_code] = json.load(f)

    @classmethod
    def get(cls, key_path: str, lang_code: str = None, placeholders: dict | None = None):
        """
        获取指定语言的翻译文本，并替换占位符。

        参数:
            key_path (str): JSON 键路径，用 '.' 分隔，例如 "code.1000"
            lang_code (str, optional): 语言代码，默认为 None（需先手动指定）
            placeholders (dict, optional): 占位符字典，例如 {"username": "MaoYu"}

        返回:
            str: 翻译文本（如果路径存在占位符，则替换）如果 key 路径不存在，返回原始 key_path
        """
        placeholders = placeholders or {}
        # 获取指定语言缓存
        if lang_code not in cls._lang_cache:
            return key_path
        data = cls._lang_cache[lang_code]
        # 根据路径逐级查找
        for key in key_path.split("."):
            data = data.get(str(key))
            if data is None:
                return key_path  # 如果路径不存在，返回原始 key
        # 替换占位符
        if isinstance(data, str) and placeholders:
            for k, v in placeholders.items():
                data = data.replace(f"{{{k}}}", v)
        return data