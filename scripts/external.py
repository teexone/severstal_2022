from datetime import timedelta

import pandas as pd
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import scripts.app_format.date as dateformat


class Indices:
    ore = 'Ore'
    gas = 'Gas'
    disel = 'Disel'
    steel = 'Steel'
    metal = 'Sheet metal'
    profiles = 'Profiles'
    rails = 'Rails wheels'
    machines = "Machines"
    vehicles = "Vehicle"


xlsx = pd.ExcelFile('data/external/indices.xlsx')

def get_data(index: str):
    dt = pd.read_excel(xlsx, index)
    rt = []
    for i in range(1, len(dt.index) + 1, 2):
        rt.append([])
        listed_data = list(dt.iloc[i, 2:].to_dict().items())
        print(listed_data)
        for i in range(len(listed_data) - 1):
            k, v = listed_data[i]
            next_v = listed_data[i + 1][1]
            t = dateformat.from_external_date(str(k))
            it = timedelta(days=0)
            while it.days != 365:
                rt[-1].append((t + it, v + it.days / 365 * (next_v - v)))
                it = it + timedelta(days=1)
            print(it)
    return rt
