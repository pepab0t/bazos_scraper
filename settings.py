import datetime

BASE_URL = "https://reality.bazos.cz"
HOME_URL = f"{BASE_URL}/prodam/byt/"
SEP = "------------------------------------------------------------------"
PAGE_COUNT: int = 1

STORE_FILE = "visited.txt"

BLACKLIST = [
    "realitní",
    "realitka",
    "nabízíme",
    "ve výhradním zastoupení",
]

DATETIME_FORMAT = "%d-%m-%Y_%Hh%Mm%Ss"

NOW = datetime.datetime.now()
