from permanent import *
import pandas as pd


def by_name(source: pd.DataFrame, name: str, columns: list) -> pd.DataFrame:
    """
    Retrieves all the fields with product name being equal to the passed name argument.
    Optionally (if `columns` is not None) drops all the columns not specified by the argument

    :param source: `pandas.DataFrame` -- The source data to filter
    :param name: `str` -- The name of the product
    :param columns: `list of strings or None` -- The columns to preserve
    :return:  Filtered data as `pandas.DataFrame`
    """

    pre = source[source[product_name_column] == name].copy()
    return pre if columns is None else pre.loc[:, columns]
