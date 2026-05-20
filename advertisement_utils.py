from entity import Advertisement
from settings import BASE_URL, BLACKLIST, NAME_BLACKLIST


def is_interesting(ad: Advertisement) -> bool:
    name: str = ad.name.lower()
    for name_blacklist_word in NAME_BLACKLIST:
        if name_blacklist_word in name:
            return False

    text = ad.searchable_text
    for blacklist_word in BLACKLIST:
        if blacklist_word in text:
            return False

    return True


def create_url(path: str) -> str:
    return f"{BASE_URL}{('/' if not path.startswith('/') else '') + path}"
