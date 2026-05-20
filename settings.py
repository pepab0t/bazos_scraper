import datetime

BASE_URL = "https://reality.bazos.cz"
HOME_URL = f"{BASE_URL}/prodam/byt/"
SEP = "------------------------------------------------------------------"
START_PAGE: int = 0
PAGE_COUNT: int = 20

STORE_FILE = "visited.txt"

NAME_BLACKLIST = [
    "real",
]

BLACKLIST = [
    "realitní",
    "realitka",
    "nabízíme",
    "ve výhradním zastoupení",
    "nevolat",
    "nevolejte",
    "bez provize",
    "nevolejte",
    "nevolat"
]

DATETIME_FORMAT = "%d-%m-%Y_%Hh%Mm%Ss"

NOW = datetime.datetime.now()
