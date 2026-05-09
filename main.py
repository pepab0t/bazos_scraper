import asyncio

from aiohttp import ClientSession

from advertisement_utils import is_interesting
from parsing import parse_advertisement_details, parse_links
from settings import PAGE_COUNT, SEP, STORE_FILE
from store import VisitStore
from web import get_ad_content, get_advertisement_page
from writer import HtmlWriter


async def main():
    async with ClientSession() as session, VisitStore(STORE_FILE) as store, HtmlWriter() as w:
        for page in range(PAGE_COUNT):
            print(f"reading page: {page + 1}/{PAGE_COUNT}")
            contents = await get_advertisement_page(session, page)
            if contents is None:
                print("reached the end", page)
                return
            hrefs = list(filter(lambda h: not store.is_visited(h), parse_links(contents)))
            print(f"advertisements to check: {len(hrefs)}")
            interesting: int = 0
            for href in hrefs:
                await asyncio.sleep(1)
                store.visit(href)
                ad = await parse_advertisement_details(get_ad_content(href, session))
                if isinstance(ad, str):
                    print(ad)
                    continue
                if not is_interesting(ad):
                    continue
                interesting += 1
                await w.add_advertisement(ad)
                break
            print(f"total {interesting} of them was interesting")
            print(SEP)


if __name__ == "__main__":
    asyncio.run(main())
