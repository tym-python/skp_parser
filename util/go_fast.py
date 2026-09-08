import uuid
from typing import Optional

import aiohttp

from util.http.http_request_util import HttpRequest
from util.log_util import get_logger

logger = get_logger(__file__)


class GoFast:
    UPLOAD_PATH = "http://192.168.1.91:8087/group7/upload"

    @classmethod
    async def upload(
            cls,
            bs: bytes,
            file_type: str,
            upload_path: str = UPLOAD_PATH,
            *,
            session: Optional[aiohttp.ClientSession] = None,
            timeout_sec: int = 3600,
    ) -> str:
        try:
            if not bs:
                return ""

            filename = f"{uuid.uuid4()}.{file_type or 'bin'}"

            owns_session = session is None
            if owns_session:
                session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout_sec))

            form = aiohttp.FormData()
            form.add_field("file", bs, filename=filename, content_type="application/octet-stream")
            form.add_field("output", "json")

            async with HttpRequest.request(
                    session=session,
                    method='post',
                    url=upload_path,
                    data=form,
                    ssl=False) as resp:
                resp.raise_for_status()
                result = await resp.json(content_type=None)  # 容忍服务端没写 application/json
                return str(result.get("url", "")) if result else ""
        except Exception as ex:
            logger.error(f"上传文件出现错误！异常信息：{ex}", exc_info=True)
            return ""
        finally:
            if session is not None and "owns_session" in locals() and owns_session:
                await session.close()
