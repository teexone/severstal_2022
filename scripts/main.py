from appparser.IndicesParserModule.IndicesParserModule import IndicesParserModule
from apppredict.Predictor import PricePredictor

import pandas as pd
import datetime as dt

from filters import by_name
from data import refine
from appformat.date import date_to_int
from permanent.permanent import order_date_column, order_price_column
import matplotlib.pyplot as plt

external = "../data/external/$indices.xlsx"

gas_parser = IndicesParserModule(external, 'Gas')
ore_parser = IndicesParserModule(external, 'Ore')
data = by_name(refine('../data/severstal/datamon.xlsx'),
                 "Колесо 3519.05.02.006",
                 [order_date_column, order_price_column])
prices = [(date_to_int(k.date()), v) for k, v in data.to_numpy().tolist()]
predictor = PricePredictor(prices)
predictor.attach_parser(gas_parser)
predictor.attach_parser(ore_parser)
for i in gas_parser.__data__:
    plt.plot([_[0] for _ in i], [_[1] for _ in i])
plt.show()
