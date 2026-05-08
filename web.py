import aiofiles
from aiohttp import ClientSession

from advertisement_utils import create_url
from settings import HOME_URL

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    # Modern Chrome headers
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    # Optional but often present
    "Cache-Control": "max-age=0",
}

not_interesting_counter: int = 0


async def get_advertisement_page(session: ClientSession, page: int) -> bytes | None:
    offset = page * 20
    response = await session.get(HOME_URL + (f"{offset}/" if offset > 0 else ""), headers=HTTP_HEADERS)
    if not (200 <= response.status <= 299):
        return
    return await response.content.read()


async def read_advertisement_page_from_file():
    async with aiofiles.open("list.html", "rb") as file:
        return await file.read()


async def get_ad_content(path: str, session: ClientSession) -> tuple[bytes, str]:
    response = await session.get(create_url(path), headers=HTTP_HEADERS)
    url = str(response.url)
    content = await response.content.read()
    return (content, url)
