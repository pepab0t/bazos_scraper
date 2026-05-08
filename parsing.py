import re
from typing import Awaitable, Iterable

import bs4

from entity import Advertisement

PSC_PATTERN = re.compile(".*((\\d)\\d\\d \\d\\d).*")


def _find_href_in_title(title_tag: bs4.Tag) -> Iterable[str]:
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
            yield from _find_href_in_title(title_tag)


async def get_advertisement_details(response: Awaitable[tuple[bytes, str]]) -> Advertisement | str:
    html, url = await response
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
