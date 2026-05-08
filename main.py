import asyncio
from pathlib import Path
from typing import Iterator

from aiohttp import ClientSession

from inout import get_ad_content, get_advertisement_page, write_description
from parsing import get_advertisement_details, parse_links
from settings import PAGE_COUNT, STORE_FILE
from store import VisitStore
from writer import HtmlWriter


async def main():
    Path("output.txt").unlink(missing_ok=True)
    async with ClientSession() as session, VisitStore(STORE_FILE) as store, HtmlWriter() as w:
        for page in range(PAGE_COUNT):
            contents = await get_advertisement_page(session, page)
            if contents is None:
                print("reached the end", page)
                return
            hrefs: Iterator[str] = parse_links(contents)
            async with asyncio.TaskGroup() as tg:
                for href in hrefs:
                    ad = await get_advertisement_details(get_ad_content(href, session))
                    if isinstance(ad, str):
                        print(ad)
                        continue
                    tg.create_task(w.add_advertisement(ad))
                    await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
