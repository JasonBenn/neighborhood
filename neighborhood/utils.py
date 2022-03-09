import re

import datetime


def currency_to_int(dollars: str) -> int:
    if isinstance(dollars, float):
        return int(dollars)
    return int(float(dollars.replace('$', '').replace(',', '')))


def clamp(val, smallest, largest):
    return min(max(smallest, val), largest)


def parse_date(date: str):
    if match := re.match('(2\d{3})(\d{2})(\d{2})', date):
        return datetime.date(year=int(match.group(1)), day=clamp(int(match.group(2)), 1, 31), month=clamp(int(match.group(3))+1, 1, 12))

    return datetime.datetime.strptime(date, "%m/%d/%Y").date()


def format_address(addr: str) -> str:
    return re.sub("^([^,]*),? San Francisco", "\g<1>, San Francisco", re.sub("\s", " ", addr.title())).replace(" Ca ", " CA ")