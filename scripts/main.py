from collections import defaultdict

import numpy as np
import pandas

from appparser.IndicesParserModule.IndicesParserModule import IndicesParserModule
from apppredict.Predictor import PricePredictor

import datetime as dt

from filters import by_name
from data import refine
from appformat.date import date_to_int, int_to_date
from permanent.permanent import order_date_column, order_price_column
from external import Indices, russian_indices

external = "../data/external/indices.xlsx"


def plot(x: list, y: list):
    import matplotlib.pyplot as plt
    import pandas as pd
    import random
    save_dir = '../.temp'
    print(x, y)
    df = pd.DataFrame({
        'Время': x, 'Цена, руб': y
    })
    print(df)
    df.to_excel(save_dir + '/' + str(random.randint(0, 10**20)) + '.xlsx')


def calculate(product: str, date: dt.date, include_indices: list):
    data = by_name(refine('../data/severstal/datamon.xlsx'),
                   product,
                   [order_date_column, order_price_column])
    prices = [(date_to_int(k.date()), v) for k, v in data.to_numpy().tolist()][:-1]
    parsers = [IndicesParserModule(external, i) for i in include_indices]
    predictor = PricePredictor(prices)
    for parser in parsers:
        predictor.attach_parser(parser)
    predicted, predicted_indices, = predictor.predict_price(date)
    dict_dt = defaultdict(list)
    dict_dt['Дата'] = list(map(lambda x: int_to_date(x), predictor.__times__)) + [date]
    for i, ext in enumerate(predictor.__modules__):
        for t in predictor.__times__:
            dict_dt[russian_indices[include_indices[i]]].append(np.mean(ext.get_data_at(int_to_date(t))))
        dict_dt[russian_indices[include_indices[i]]].append(np.mean(predicted_indices[i]))
    dict_dt['Цена продукта'] = predictor.__training_data__.y + [predicted[1][0]]
    df = pandas.DataFrame(data=dict_dt, columns=['Дата', *[russian_indices[i] for i in include_indices], 'Цена продукта'])
    return predicted[0], predicted[2], df
