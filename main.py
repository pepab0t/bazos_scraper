import asyncio
from typing import Iterator

from aiohttp import ClientSession

from parsing import parse_advertisement_details, parse_links
from settings import PAGE_COUNT, STORE_FILE
from store import VisitStore
from web import get_ad_content, get_advertisement_page
from writer import HtmlWriter


async def main():
    async with ClientSession() as session, VisitStore(STORE_FILE) as store, HtmlWriter() as w:
        for page in range(PAGE_COUNT):
            contents = await get_advertisement_page(session, page)
            if contents is None:
                print("reached the end", page)
                return
            hrefs: Iterator[str] = parse_links(contents)
            for href in filter(lambda h: not store.is_visited(h), hrefs):
                ad = await parse_advertisement_details(get_ad_content(href, session))
                if isinstance(ad, str):
                    print(ad)
                    continue
                await w.add_advertisement(ad)
                store.visit(href)
                await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
