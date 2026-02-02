import json

from ..core import ASSETS_DIR


class BaseLangStrategy:
    def test(self) -> str:
        raise NotImplementedError
    
class LangStrategy(BaseLangStrategy):
    _cache = None

    def __init__(self, data: dict):
        self._cache = data
        super().__init__()

    def test(self) -> str:
        return str(self._cache)
    
class LangStrategyManager:
    _strategies = {}

    @classmethod
    def register(cls, lang):
        file_path = ASSETS_DIR / f"locales/{lang}.json"
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            cls._strategies[lang] = LangStrategy(data)

    @classmethod
    def get(cls, lang):
        return cls._strategies.get(lang)