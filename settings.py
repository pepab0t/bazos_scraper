import datetime

BASE_URL = "https://reality.bazos.cz"
HOME_URL = f"{BASE_URL}/prodam/byt/"
SEP = "------------------------------------------------------------------"
PAGE_COUNT: int = 5

STORE_FILE = "visited.txt"

BLACKLIST = [
    "realitní",
    "realitka",
    "nabízíme",
    "ve výhradním zastoupení",
]

DATETIME_FORMAT = "%H:%M:%S_%d-%m-%Y"

NOW = datetime.datetime.now()
