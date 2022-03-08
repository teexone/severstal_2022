from datetime import date


def from_external_date(s: str):
    """
    Translates the data from external source file to the datetime.date object

    :param s: String representation of a date
    :return: The datetime.date object
    """
    if '/' in s:
        year, month = [int(x) for x in s.split('/')]
        return date(year=year, month=month, day=1)
    else:
        return date(year=int(s), month=1, day=1)


base = date(year=1998, month=1, day=1)


def date_to_int(dt: date):
    """
    Uniformly transforms any date in the file into the int

    :param dt: the datetime.date object
    :return: int representation of the date
    """
    return (dt - base).days
