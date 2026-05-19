import datetime

BASE_URL = "https://reality.bazos.cz"
HOME_URL = f"{BASE_URL}/prodam/byt/"
SEP = "------------------------------------------------------------------"
START_PAGE: int = 88
PAGE_COUNT: int = 20

STORE_FILE = "visited.txt"

BLACKLIST = [
    "realitní",
    "realitka",
    "nabízíme",
    "ve výhradním zastoupení",
    "nevolat",
    "nevolejte",
    "bez provize"
]

DATETIME_FORMAT = "%d-%m-%Y_%Hh%Mm%Ss"

NOW = datetime.datetime.now()
