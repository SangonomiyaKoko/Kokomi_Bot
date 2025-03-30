import os
import json
from ..config import MOCK_DIR

class Mock:
    """
    Mock 类用于读取模拟数据文件并返回相应的内容。
    """

    @staticmethod
    def read_data(file_name: str) -> dict:
        """
        读取模拟数据文件，并返回其内容。

        根据给定的文件名，从 `MOCK_DIR` 目录加载对应的 JSON 文件并返回其内容。
        
        参数:
            file_name (str): 模拟数据文件的名称。该文件必须是 JSON 格式。
        
        返回:
            dict: 从文件中读取并解析后的数据字典。

        异常处理：
            如果文件不存在或无法读取，将抛出文件相关的异常。
        """
        # 构建文件路径
        mock_file_path = os.path.join(MOCK_DIR, file_name)

        try:
            # 打开并读取文件
            with open(mock_file_path, "r", encoding="utf-8") as temp:
                mock_data = json.load(temp)
        except FileNotFoundError:
            raise FileNotFoundError(f"Mock file '{file_name}' not found in {MOCK_DIR}")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from the mock file '{file_name}'")
        
        return mock_data
