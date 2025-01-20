class Utils:
    def get_language(language: str) -> str:
        "获取接口语言的参数内容"
        language_dict = {
            'cn': 'chinese',
            'en': 'english',
            'ja': 'japanese'
        }
        return language_dict.get(language)
    
    def get_language_from_input(input: str) -> str | None:
        "处理用户输入的language参数"
        language_dict = {
            'cn':'cn','chinese':'cn',
            'en':'en','english':'en',
            'ja':'ja','japanese':'ja' 
        }
        return language_dict.get(input.lower(), None)
    
    def get_operator_by_id(region_id: int) -> str:
        "获取服务器id对应的运营商，不同运营商对应的素材会有不同"
        if region_id == 4:
            return 'LestaGame'
        else:
            return 'WarGaming'

    def get_region_id_from_input(input: str) -> int | None:
        "处理用户输入的region参数"
        region_dict = {
            'asia':1,'apac':1,'aisa':1,'亚服':1,    # 为什么总会有人拼成aisa？
            'eu':2,'europe':2,'欧服':2,
            'na':3,'northamerica':3,'america':3,'美服':3,
            'ru':4,'russia':4,'俄服':4,'莱服':4,
            'cn':5,'china':5,'国服':5
        }
        return region_dict.get(input.lower(), None)

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
    