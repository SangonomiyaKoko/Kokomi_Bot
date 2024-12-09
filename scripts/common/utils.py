class Utils:
    def get_language(language: str) -> str:
        language_dict = {
            'cn': 'chinese',
            'en': 'english',
            'ja': 'japanese'
        }
        return language_dict.get(language)

    def get_region_by_id(region_id: int) -> str:
        "获取region"
        region_dict = {
            1: 'asia',
            2: 'eu',
            3: 'na',
            4: 'ru',
            5: 'cn'
        }
        return region_dict.get(region_id)

    def get_default_language(platform: dict) -> str:
        if platform['type'] in ['qq_bot', 'qq_group', 'qq_guild']:
            return 'cn'
        else:
            return 'en'
        
    def get_default_picture() -> dict:
        return {
            'background': '#F8F9FB',
            'content': 'light',
            'theme': 'default'
        }