"""HTTP 请求工具:基于 aiohttp 的异步上下文管理器封装。

用法(与 util/go_fast.py 保持一致):
    async with HttpRequest.request(
            session=session, method='post', url=url, data=form, ssl=False) as resp:
        resp.raise_for_status()
        result = await resp.json(content_type=None)
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional

import aiohttp
from aiohttp.client_reqrep import ClientResponse


class HttpRequest:
    """aiohttp 请求封装,以异步上下文管理器方式发起请求并托管响应。"""

    @staticmethod
    @asynccontextmanager
    async def request(
            session: aiohttp.ClientSession,
            method: str,
            url: str,
            data: Any = None,
            ssl: Optional[bool] = None,
            **kwargs: Any,
    ) -> AsyncIterator[ClientResponse]:
        """发起请求并返回响应上下文。

        Args:
            session: 调用方持有的 aiohttp.ClientSession(由调用方负责生命周期)
            method: 请求方法,如 'get' / 'post'
            url: 请求地址
            data: 请求体,可为 bytes / FormData / dict 等 aiohttp 支持的类型
            ssl: 是否校验 SSL,内网服务通常传 False 跳过
            **kwargs: 透传给 session.request 的其他参数(如 headers、params、timeout)

        Returns:
            ClientResponse,退出上下文时自动释放连接
        """
        async with session.request(
                method=method,
                url=url,
                data=data,
                ssl=ssl,
                **kwargs,
        ) as resp:
            yield resp
