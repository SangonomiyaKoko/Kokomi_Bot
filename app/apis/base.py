import httpx
from typing import Dict, Optional

from ..core import Config
from ..loggers import logging, ExceptionLogger

class KokomiAPI:
    async def get(
        path: str,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        access_token: bool = False
    ) -> Dict:
        """
        发送 HTTP GET 请求并返回 JSON 响应数据。

        该方法根据传入的 `path`、`path_params` 和 `query_params`
        构建完整请求 URL：
        - `path_params` 用于替换路径中的占位符（如 `/users/{id}`）
        - `query_params` 会被拼接为 URL 查询字符串
        - 当 `access_token=True` 时，会自动在请求头中携带 Access-Token

        请求将使用异步方式发送，并在请求完成后记录请求路径及返回状态码。

        参数:
            path (str): API 端点路径，支持 `{key}` 形式的路径占位符。
            path_params (Dict[str, str], optional): 路径参数映射，
                用于替换 `path` 中的占位符。默认为空字典。
            query_params (Dict[str, str], optional): 查询参数字典，
                将被拼接为 URL 查询字符串。默认为空字典。
            access_token (bool, optional): 是否在请求头中携带 Access-Token。
                默认为 False。

        返回:
            Dict: 接口返回的 JSON 数据。

        异常:
            httpx.HTTPStatusError:
                当接口返回的 HTTP 状态码非 200 时抛出。
            httpx.RequestError:
                当发生网络异常或请求超时时抛出。
        """
        for key, value in path_params.items():
            path = path.replace(f"{{{key}}}", value)
        # 构建带查询参数的 URL
        url = f'http://{Config.api.host}:{Config.api.port}' + path
        # url = f'{base_url}?{"&".join([f"{key}={value}" for key, value in query_params.items()])}' if query_params else base_url
        headers = {
            'accept': 'application/json'
        }
        if access_token:
            headers['Access-Token'] = Config.api.token
        
        async with httpx.AsyncClient() as client:
            res = await client.get(
                url=url,
                params=query_params,
                headers=headers,
                timeout=Config.api.timeout
            )
            request_code = res.status_code
            logging.debug(f"GET {url} {request_code}")
            result = res.json()
        
        if request_code == 200:
            return result
        else:
            res.raise_for_status()
