import datetime

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

from scripts import external
from scripts.data import refine
from scripts.filters import by_name
import scripts.app_format.date
import scripts.data
import scripts.external
from scripts.permanent.permanent import order_date_column, \
                                        order_price_column


def predict(name: str, date: datetime.time) -> int:

    prediction = 0
    df = by_name(refine('data/severstal/datamon.xlsx'), name, [order_date_column, order_price_column])
    price, date_s = df[order_price_column], df[order_date_column]
    args = []
    for date in date_s:
        index_s = []
        for i in dir(external.Indices):
            if i[0] == '_':
                continue
            tmp = scripts.external.get_data(getattr(scripts.external.Indices, i))
            print(tmp)
            index_s.append(predict_indices(tmp, date))
        args.append((price, index_s))
    print(args)
    return prediction

def predict_indices(data: list, date: datetime.date) -> int:
    t =
    i_t =
    print(t[0], i_t[0], sep='\n\n')
    model = np.poly1d(np.polyfit(t, i_t, 3))
    val = model(date)
    # Error estimation
    # print(r2_score(i_t, model(t)))
    return val