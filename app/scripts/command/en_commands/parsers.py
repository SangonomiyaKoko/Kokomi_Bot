# 解析指令参数的方法
import re

from ...api import BasicAPI
from ...schemas import JSONResponse

def get_region_id_from_aid(account_id: int):
    account_id = str(account_id)
    account_id_len = len(account_id)
    # 俄服 1-9 [~5字段]
    if account_id_len < 9:
        return 4
    elif (
        account_id_len == 9 and 
        account_id[0] in ['1', '2', '3']
    ):
        return 4
    # 欧服 9 [5~字段] 
    if (
        account_id_len == 9 and
        account_id[0] in ['5', '6', '7']
    ):
        return 2
    # 亚服 10 [2-3字段]
    if (
        account_id_len == 10 and
        account_id[0] in ['2', '3']
    ):
        return 1
    # 美服 10 [1字段]
    if (
        account_id_len == 10 and
        account_id[0] in ['1']
    ):
        return 3
    # 国服 10 [7字段]
    if (
        account_id_len == 10 and
        account_id[0] in ['7']
    ):
        return 5
    return None

def extract_mention_id(text: str) -> str | None:
    """从 @ 中提取 ID"""
    match = re.search(r"<@!([a-zA-Z0-9]+)>", text)
    return match.group(1) if match else None

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

async def search_user(region_id: int, nickname: str):
    result = await BasicAPI.search_user(region_id, nickname)
    if result['code'] != 1000:
        return result
    if len(result['data']) != 1:
        return JSONResponse.API_9003_NameNotFound
    return result

async def check_user(region_id: int,account_id: int):
    result = await BasicAPI.check_user(region_id, account_id)
    if result['code'] != 1000:
        return result
    return result