import asyncio
import re
from dataclasses import dataclass
from itertools import islice
from pathlib import Path
from typing import Any, Coroutine, Iterable, Iterator

import aiofiles
import bs4
from aiohttp import ClientSession

BASE_URL = "https://reality.bazos.cz"
HOME_URL = f"{BASE_URL}/prodam/byt/"
SEP = "------------------------------------------------------------------"
PAGE_COUNT: int = 50
not_interesting_counter: int = 0

PSC_PATTERN = re.compile(".*((\\d)\\d\\d \\d\\d).*")

headers = {
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


def create_url(path: str) -> str:
    return f"{BASE_URL}{('/' if not path.startswith('/') else '') + path}"


async def get_advertisement_list(session: ClientSession, page: int) -> bytes | None:
    offset = page * 20
    response = await session.get(HOME_URL + (f"{offset}/" if offset > 0 else ""), headers=headers)
    return await response.content.read()


async def read_advertisement_list_from_file():
    async with aiofiles.open("list.html", "rb") as file:
        return await file.read()


def find_href(title_tag: bs4.Tag) -> Iterable[str]:
    a_tag = title_tag.find("a")
    if a_tag is None:
        return
    for href in a_tag.get_attribute_list("href"):
        yield href


def scrape_hrefs(content: bytes):
    soup = bs4.BeautifulSoup(content, "html.parser")
    ads = soup.find_all("div", class_="inzeraty inzeratyflex")
    for ad in ads:
        location_element = ad.find("div", class_="inzeratylok")
        if location_element is None:
            continue
        m = PSC_PATTERN.match(location_element.text)
        if m is None:
            continue
        if m.group(2) in {"1", "2", "5"}:
            title_tag = ad.find("h2", class_="nadpis")
            if title_tag is None:
                continue
            yield from find_href(title_tag)


@dataclass(frozen=True, slots=True)
class Advertisement:
    url: str
    title: str
    description: str
    name: str = ""
    location: str = ""
    seen: str = ""

    def to_text(self) -> str:
        return f"""url: {self.url}
name: {self.name}
seen: {self.seen}
title: {self.title}
description: {self.description}
        """

    @property
    def searchable_text(self) -> str:
        return f"{self.title}{self.description}".lower()


async def get_advertisement_details(session: ClientSession, url: str) -> Advertisement | str:
    response = await session.get(url, headers=headers)
    if response.status > 299:
        return f"{url}: {response.status}"

    html = await response.content.read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    title_tag = soup.find("h1", class_="nadpisdetail")
    description_tag = soup.find("div", class_="popisdetail")
    left_info = soup.find("td", class_="listadvlevo")

    name_tag = left_info.find("span", class_="paction") if left_info else None
    seen_tag = left_info.select_one('tr:has(td:-soup-contains("Vidělo")) > td:last-child') if left_info else None

    SEEN_PATTERN = re.compile("(\\d+) lidí")
    if seen_tag:
        seen = m.group(1) if (m := SEEN_PATTERN.match(seen_tag.text)) is not None else ""
    else:
        seen = ""

    return Advertisement(
        url,
        title_tag.text if title_tag is not None else "no title found (<h1 class='nadpisdetail'>)",
        description_tag.text
        if description_tag is not None
        else f"{url}: no description found (<div class='popisdetail'>)",
        name=name_tag.text if name_tag is not None else "unknown",
        seen=seen,
    )


async def write_description(details_coro: Coroutine[Any, Any, Advertisement | str]):
    details = await details_coro
    if isinstance(details, Advertisement):
        if not is_interesting(details):
            global not_interesting_counter
            not_interesting_counter += 1
            return
        text = details.to_text()
    else:
        text = details
    async with aiofiles.open("output.txt", "a") as file:
        await file.write(text + f"\n{SEP}\n")
        print(f"written: {details.title}")


BLACKLIST = [
    "realitní",
    "realitka",
    "nabízíme",
    "ve výhradním zastoupení",
]


def is_interesting(ad: Advertisement) -> bool:
    name: str = ad.name.lower()
    if "real" in name:
        return False

    text = ad.searchable_text
    if "nevolat" in text:
        return True

    for blacklist_word in BLACKLIST:
        if blacklist_word in text:
            return False
    return True


async def main():
    Path("output.txt").unlink(missing_ok=True)
    async with ClientSession() as session:
        for page in range(PAGE_COUNT):
            contents = await get_advertisement_list(session, page)
            if contents is None:
                print("reached the end", page)
                return
            hrefs: Iterator[str] = scrape_hrefs(contents)
            async with asyncio.TaskGroup() as tg:
                for href in hrefs:
                    task = get_advertisement_details(session, create_url(href))
                    tg.create_task(write_description(task))
                    await asyncio.sleep(2)

    print(f"zahozeno: {not_interesting_counter}")


if __name__ == "__main__":
    asyncio.run(main())
