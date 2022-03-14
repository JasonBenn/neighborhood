import re

import datetime

from django.db import connection


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


def fetchall(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    raw_results = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    return [dict(zip(colnames, x)) for x in raw_results]


def execute_sql(sql):
    cursor = connection.cursor()
    return cursor.execute(sql)


def chunks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def sliding_window(lst, n=2):
    return [lst[i:i + n] for i in range(0, len(lst) - 1)]


def flatten(t):
    return [item for sublist in t for item in sublist]
