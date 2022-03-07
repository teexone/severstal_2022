
from scripts.permanent.permanent import *
import pandas as pd

def by_name(source: pd.DataFrame, name: str, columns) -> pd.DataFrame:
    '''
    # Summary:

    Retrieves all the fields with product name being equal to the passed name argument.
    Optionally (if `columns` is not None) drops all the columns not specified by the argument

    # Args:
        
    - source:  `pandas.DataFrame` -- The source data to filter
    - name: `str` -- The name of the product 
    - columns: `list of strings or None` -- The columns to preserve

    # Returns

    Filtered data as `pandas.DataFrame`
    '''
    pre = source[source[product_name_column] == name].copy()
    return pre if columns is None else pre.loc[:, columns]


def by_order_price(source: pd.DataFrame, lbound: int, rbound: int, columns) -> pd.DataFrame:
    '''
    # Summary:

    Retrieves all the fields with order price corresponding to the range [lbound, rbound]
    Optionally (if `columns` is not None) drops all the columns not specified by the argument

    # Args:
        
    - source:  `pandas.DataFrame` -- The source data to filter
    - lbound: `int` -- The lower bound of the price (inclusively)
    - rbound: 'int' -- The upper bound of the price (inclusively)
    - columns: `list of strings or None` -- The columns to preserve

    # Returns

    Filtered data as `pandas.DataFrame`
    '''
    pre = source[(source[order_price_column] <= rbound) & (lbound <= source[order_price_column])].copy()
    return pre if columns is None else pre.loc[:, columns]
