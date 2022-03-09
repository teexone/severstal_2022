from collections import defaultdict
from datetime import timedelta, date

import pandas as pd
import appformat.date as dateformat


class Indices:
    """
    Names of the available product categories
    """
    ore = 'Ore'
    gas = 'Gas'
    disel = 'Disel'
    steel = 'Steel'
    metal = 'Sheet metal'
    profiles = 'Profiles'
    rails = 'Rails wheels'
    machines = 'Machines'
    vehicles = 'Vehicle'


xlsx = pd.ExcelFile('../data/external/indices.xlsx')


def get_data(index: str):
    """
    Retrieves the data from external source by the name of the product category
    Additionally adds values of the indices for each day to make the work with
    external data more handy

    :param index: The name of the product category
    :return: Retrieved values

    """
    dt = pd.read_excel(xlsx, index)
    rt = []
    for i in range(1, len(dt.index) + 1, 2):
        rt.append([])
        listed_data = list(dt.iloc[i, 2:].to_dict().items())
        last = None
        for i in range(len(listed_data) - 1):
            k, v = listed_data[i]
            nk, nv = listed_data[i + 1]
            t, nt = dateformat.from_external_date(str(k)), dateformat.from_external_date(str(nk))
            if t.year < 2016:
                continue
            m_delta = (nt - t).days
            it = timedelta(days=0)
            while it.days != m_delta:
                rt[-1].append((dateformat.date_to_int(t + it), int((v + (nv - v) * it.days / m_delta) * 10) / 10))
                last = t + it
                it = it + timedelta(days=1)
        while last < date.today():
            rt[-1].append((dateformat.date_to_int(last), rt[-1][-1][1]))
            last += timedelta(days=1)
    return rt


def get_flattened_indices(index: str):
    """
    Returns the indices for the category in the format of dict where keys are integer dates
    and keys are arrays of the values that corresponds to these dates

    :param index: The name of the category to retrieve the index
    :return: The dict representation for data
    """
    data = get_data(index)
    fl = defaultdict(list)
    for index in data:
        for k, v in index:
            fl[k].append(v)
    return fl


def merge_flattened_indices(indices):
    """
    Merges the arrays of the flattened indices

    :param indices: The flattened indices
    :return:
    """
    flat = [get_flattened_indices(_) for _ in indices]
    fl = defaultdict(list)
    for flattened_vector in flat:
        for k, vector in flattened_vector.items():
            fl[k] += vector
    return fl


def sieve(indices, dates):
    """
    Filters the indices using the dates
    :param indices: The indices values to filter
    :param dates: The dates used to filter
    :return: Filtered indices
    """
    rt = dict()
    for _ in dates:
        if len(indices[_]) > 0:
            rt[_] = indices[_]
    return rt


def get_indices():
    return {
            'Бензин': Indices.gas,
            'Сталь': Indices.steel,
            'Стальной прокат': Indices.metal,
            'Дизель': Indices.disel,
            'Автотранспорт': Indices.vehicles,
            'Станки': Indices.machines,
            'Стальные профили': Indices.profiles,
            'Цельнокатаные колёса': Indices.rails,
            'Железная руда': Indices.ore,
    }


def get_inverted_indices():
    return {v: k for k, v in get_indices().items()}

