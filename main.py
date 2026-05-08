import asyncio
from pathlib import Path
from typing import Iterator

from aiohttp import ClientSession

from inout import get_ad_content, get_advertisement_page, write_description
from parsing import get_advertisement_details, scrape_hrefs
from settings import PAGE_COUNT


async def main():
    Path("output.txt").unlink(missing_ok=True)
    async with ClientSession() as session:
        for page in range(PAGE_COUNT):
            contents = await get_advertisement_page(session, page)
            if contents is None:
                print("reached the end", page)
                return
            hrefs: Iterator[str] = scrape_hrefs(contents)
            async with asyncio.TaskGroup() as tg:
                for href in hrefs:
                    task = get_advertisement_details(get_ad_content(href, session))
                    tg.create_task(write_description(task))
                    await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
