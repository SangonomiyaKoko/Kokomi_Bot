from typing import Optional, Union

class Utils:
    """
    Utils 类包含一些常用的工具方法，处理颜色转换、语言处理、地区处理等操作。
    """

    def hex_to_rgb(
        hex_color: str, 
        alpha: Optional[int] = None
    ) -> Union[tuple[int, int, int], tuple[int, int, int, int]]:
        """
        将 16 进制颜色转换为 RGB 或 RGBA 颜色值。

        参数:
            hex_color (str): 以 '#' 开头的 16 进制颜色字符串，例如 '#FF5733'。
            alpha (Optional[int]): 透明度，可选，取值范围 0-255。如果不传入，返回 RGB 颜色。

        返回:
            Union[tuple[int, int, int], tuple[int, int, int, int]]: 
            如果 `alpha` 存在，则返回 (R, G, B, A)，否则返回 (R, G, B)。
        """
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        # 如果传入了 alpha 参数，则返回 RGBA
        return (r, g, b, alpha) if alpha is not None else (r, g, b)

    def get_language(language: str) -> str:
        """
        获取接口语言的参数内容。

        根据输入的语言代码，返回对应的语言名称。

        参数:
            language (str): 语言的代码，支持 'cn', 'en', 'ja'。

        返回:
            str: 对应的语言名称，如 'chinese', 'english', 'japanese'。
        """
        language_dict = {
            'cn': 'chinese',
            'en': 'english',
            'ja': 'japanese'
        }
        return language_dict.get(language, '')

    def get_language_from_input(input: str) -> Optional[str]:
        """
        处理用户输入的 language 参数，将其转换为标准格式。

        根据用户输入的语言，返回对应的标准语言代码。

        参数:
            input (str): 用户输入的语言，可以是 'cn', 'chinese' 等。

        返回:
            Optional[str]: 返回标准的语言代码，如 'cn', 'en', 'ja'，如果输入不匹配，返回 None。
        """
        language_dict = {
            'cn': 'cn', 'chinese': 'cn',
            'en': 'en', 'english': 'en',
            'ja': 'ja', 'japanese': 'ja'
        }
        return language_dict.get(input.lower())

    def get_operator_by_id(region_id: int) -> str:
        """
        获取服务器 id 对应的运营商，不同运营商对应的素材会有不同。

        参数:
            region_id (int): 区域 ID，根据区域 ID 返回对应的运营商。

        返回:
            str: 运营商名称，如 'LestaGame' 或 'WarGaming'。
        """
        # 如果是俄罗斯地区，返回 LestaGame，否则返回 WarGaming
        return 'LestaGame' if region_id == 4 else 'WarGaming'

    def get_region_id_from_input(input: str) -> Optional[int]:
        """
        处理用户输入的 region 参数，返回对应的区域 ID。

        根据用户输入的区域名称，返回对应的区域 ID。

        参数:
            input (str): 用户输入的区域名称，如 'asia', 'eu', 'na' 等。

        返回:
            Optional[int]: 匹配的区域 ID，如果没有匹配，返回 None。
        """
        region_dict = {
            'asia': 1, 'apac': 1, 'aisa': 1, '亚服': 1,
            'eu': 2, 'europe': 2, '欧服': 2,
            'na': 3, 'northamerica': 3, 'america': 3, '美服': 3,
            'ru': 4, 'russia': 4, '俄服': 4, '莱服': 4,
            'cn': 5, 'china': 5, '国服': 5
        }
        return region_dict.get(input.lower())

    def get_region_by_id(region_id: int) -> Optional[str]:
        """
        获取区域 ID 对应的区域名称。

        根据区域 ID 返回对应的区域名称，如 'asia', 'eu', 'na' 等。

        参数:
            region_id (int): 区域 ID。

        返回:
            Optional[str]: 区域名称，如果没有匹配的区域，返回 None。
        """
        region_dict = {
            1: 'asia',
            2: 'eu',
            3: 'na',
            4: 'ru',
            5: 'cn'
        }
        return region_dict.get(region_id)
