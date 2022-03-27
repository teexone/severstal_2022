import numpy as np

from appparser.IndicesParserModule.IndicesParserModule import IndicesParserModule
from apppredict.Predictor import PricePredictor

import datetime as dt

from filters import by_name
from data import refine
from appformat.date import date_to_int, int_to_date
from permanent.permanent import order_date_column, order_price_column
from external import Indices

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
    data = parsers[0].get_data()
    for key, value in data.items():
        data[key] = sum(data[key]) / len(data[key])
    predictor = PricePredictor(prices)
    for parser in parsers:
        predictor.attach_parser(parser)
    predicted = predictor.predict_price(date)
    return predicted[0], predicted[2],
