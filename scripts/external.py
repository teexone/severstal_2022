import pandas as pd
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt



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


def get_data(index: str) -> pd.DataFrame:
    dt = pd.read_excel(xlsx, index)
    for i in range(1, len(dt.index) + 1, 2):
        yield dt.iloc[i, 2:].to_dict()
    pass
