import datetime

from scripts.data import refine, get_prices_indices
from scripts.filters import *
from scripts.permanent.permanent import *
from scripts.app_format.date import from_external_date
from scripts.external import get_data, Indices
from scripts.app.calculate import predict_price
import pandas as pd
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
import scripts.predictions.price_predictions

top = [_[0] for _ in pd.read_excel('data/severstal/toplist.xlsx').to_numpy()]
data = refine('data/severstal/datamon.xlsx').sort_values(order_date_column)
prices = get_prices_indices(data, top[0])
external = list(get_data(Indices.steel))
pr = scripts.predictions.price_predictions.predict('СОВОК 1085.02.00СБ', datetime.date(year=2002, month=7, day=21))
# print(external)
# predict_price(prices, external)
