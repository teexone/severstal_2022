import datetime
import numpy as np
from external import get_data, merge_flattened_indices, sieve, get_flattened_indices, \
    get_inverted_indices

from data import refine, dictate
from filters import *
from appformat.date import date_to_int, int_to_date
from predictions.prices import PricePredictor
from predictions.indices import predict_all_indices


def calculate(product: str, date: datetime.date, include_indices: list, method: str, return_steps=False):
    """
    The main function for the prediction of the price

    :param product The name of the product
    :date date The date to predictions at
    :include_indices The indices to include into calculation (the available ones can be find in external.py)
    """

    data = refine('data/severstal/datamon.xlsx').sort_values(order_date_column)
    search_data = by_name(data, product, [order_price_column, order_date_column])
    search_data.sort_values(by=[order_date_column])
    search_data[order_date_column] = search_data[order_date_column].apply(lambda x: date_to_int(x.date()))
    dictated = dictate(search_data, order_date_column, order_price_column)
    sieved = sieve(merge_flattened_indices(include_indices), dictated.keys())
    X = [sieved[_] for _ in dictated.keys()]
    y = [int(dictated[_] * 100) / 100 for _ in sorted(dictated.keys())]
    raw_predicted_indices = [predict_all_indices(get_data(_), date_to_int(date), method) for _ in include_indices]
    predicted_indices = sum(raw_predicted_indices, [])
    model = PricePredictor(X, y)
    r2 = [_.r2 for _ in predicted_indices]
    min_r2 = min(r2)
    if not return_steps:
        return model.predict([[x.predicted for x in predicted_indices]]), min_r2
    else:
        n_sieved = [list(x.values()) for x in (sieve(get_flattened_indices(_), dictated.keys()) for _ in include_indices)]
        n_sieved = [[int(sum(_) / len(_) * 100) / 100 for _ in x] for x in n_sieved]
        data = np.array([list(dictated.keys())] + [*n_sieved] + [list(dictated.values())])
        df = pd.DataFrame(data=data.T, columns=['Дата', *[get_inverted_indices()[_] for _ in include_indices], 'Цена'])
        df['Дата'] = df['Дата'].apply(lambda x: int_to_date(x))
        df.index += 1
        predicted_indices_mean = [[_.predicted for _ in x] for x in raw_predicted_indices]
        predicted_indices_mean = [sum(_) / len(_) for _ in predicted_indices_mean]
        df2 = pd.DataFrame([
            [date, *predicted_indices_mean, model.predict([[x.predicted for x in predicted_indices]])[0]]
        ],
                           columns=df.columns)
        df = pd.concat([df, df2], ignore_index=True)
        return df

# calculate(product="Колесо 3519.05.02.006", include_indices=[Indices.gas, Indices.steel], date=datetime.date.today(), return_steps=True, method='linear')