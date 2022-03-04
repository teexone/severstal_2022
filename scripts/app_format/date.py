from datetime import date


def from_external_date(s: str):
    if '/' in s:
        year, month = [int(x) for x in s.split('/')]
        return date(year=year, month=month, day=1)
    else:
        return date(year=int(s), month=1, day=1)
