import os
import json
from ..config import MOCK_DIR

class Mock:
    def read_data(file_name: str) -> dict:
        "读取MOCK文件数据"
        mock_file_path = os.path.join(MOCK_DIR, file_name)
        temp = open(mock_file_path, "r", encoding="utf-8")
        mock_data = json.load(temp)
        temp.close()
        return mock_data