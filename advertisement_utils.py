from entity import Advertisement
from settings import BASE_URL, BLACKLIST


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


def create_url(path: str) -> str:
    return f"{BASE_URL}{('/' if not path.startswith('/') else '') + path}"
