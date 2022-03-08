import datetime
from scripts.external import get_data, Indices, merge_flattened_indices, sieve

from scripts.data import refine, dictate
from scripts.filters import *
from scripts.permanent.permanent import *
from scripts.app_format.date import date_to_int
from scripts.predictions.prices import PricePredictor
from scripts.predictions.indices import predict_all_indices


def calculate(product: str, date: datetime.date, include_indices: list, method: str):
    """
    The main function for the prediction of the price

    :param product The name of the product
    :date date The date to predict at
    :include_indices The indices to include into calculation (the available ones can be find in external.py)
    """

    data = refine('data/severstal/datamon.xlsx').sort_values(order_date_column)
    search_data = by_name(data, product, [order_price_column, order_date_column])
    search_data.sort_values(by=[order_date_column])
    search_data[order_date_column] = search_data[order_date_column].apply(lambda x: date_to_int(x.date()))
    dictated = dictate(search_data, order_date_column, order_price_column)
    sieved = sieve(merge_flattened_indices(include_indices), dictated.keys())
    X = [sieved[_] for _ in dictated.keys()]
    y = [dictated[_] for _ in sorted(dictated.keys())]
    predicted_indices = sum([predict_all_indices(get_data(_), date_to_int(date), method) for _ in include_indices], [])
    model = PricePredictor(X, y)

    return model.predict([[x.predicted for x in predicted_indices]])
