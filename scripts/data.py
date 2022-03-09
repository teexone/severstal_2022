import pandas as pd
from permanent.permanent import *


def refine(path: str, drop=True) -> pd.DataFrame:
    """
    Reads the source data and apply the following refinements:
        1.  Reshape ill-formed date fields
        2.  Drop all records with N/A dates

    :param path: The path to the source file
    :param drop: Whether to drop bad records or not
    :return:  Refined data as pandas.DataFrame
    """

    # Reads the file explicitly given in path variable
    data = pd.read_excel(path)
    if drop:
        data = data.dropna(subset=[order_date_column])
    data[arrival_date_column] = data[arrival_date_column].apply(lambda field: pd.to_datetime(field, infer_datetime_format=True)).dropna
    data[order_date_column] = data[order_date_column].apply(lambda field: pd.to_datetime(field, infer_datetime_format=True))
    return data


def dictate(dt: pd.DataFrame, key: str, value: str, agg=lambda x: sum(x) / len(x)):
    """
    Returns the dictionary constructed from the data in the following manner:
    The keys are the `key` column and values are the values for this key
    :param dt: The source data frame
    :param key: The column for 'keys' in the dict
    :param value: The column for 'values' in the dict
    :param agg: Aggregator function will be applied of the arrays of the values if their keys coincided
    :return:
    """
    split = dt.loc[:, [key, value]].to_dict('split')['data']
    d = dict()
    for _ in split:
        if _[0] not in d:
            d[_[0]] = [_[1]]
        else:
            d[_[0]].append(_[1])
    for _ in d.keys():
        d[_] = sum(d[_]) / len(d[_])
    return d
