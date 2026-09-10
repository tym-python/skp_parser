import aiohttp
import ssl
from util.log_util import get_logger

logger = get_logger(__file__)

_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

CompanyIDUrl = 'http://192.168.1.213:8013/es/getdata'
import re
GROUP_SINGLE_SUFFIX_RE = re.compile(
    r'(人民政府|政府|厅|局|委|办|管委会|县|州|盟|省|联合会|农业科学院|广播电视台|物理所|服务中心|各相关建设单位|办公室|委员会|学校|学院|大学|管理中心|残联|市|区)$')
PUNCT_RE = re.compile(r'[，。；;:：,、]')

async def get_company_id(company_name: str = '') -> int:
    company_name = re.sub(r'\s+', '', company_name)
    if not company_name:
        return 0
    elif GROUP_SINGLE_SUFFIX_RE.search(company_name) or PUNCT_RE.search(company_name):
        return 0

    params = {"companyname": company_name}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CompanyIDUrl, params=params, ssl=_SSL_CTX, timeout=10) as resp:
                resp.raise_for_status()
                result = await resp.json()
    except (aiohttp.ClientError, ValueError) as e:
        # logger.error('====== 获取【%s】公司id失败: %s ======', company_name, e)
        return 0

    data = result.get('data') or []
    if not data:
        # logger.error('====== 获取【%s】公司id失败，data 为空 ======', company_name)
        return 0

    return data[0].get('company_id', 0)
