import pandas as pd
import datetime as dt
from permanent.permanent import *

def refine(path: str) -> pd.DataFrame:
    '''
    # Summary

    Reads the source data and apply the following finements:
    
    1.  Reshape ill-formed date fields
    2.  Drop all records with N/A dates

    # Args

       - path: str - Path to the source file

    # Returns:
       
        Refined data as pandas.DataFrame
    '''
    # Reads the file explicitly given in path variable
    data = pd.read_excel(path)
    data[arrival_date_column] = data[arrival_date_column].apply(lambda field: pd.to_datetime(field)).dropna
    data[arrival_date_column].dropna()
    data[order_date_column] = data[order_date_column].apply(lambda field: pd.to_datetime(field))
    data[order_date_column].dropna()
    return data

# If the script launched on top-level with argument -d <file-path>
# then it will produce refined XLSX file in directory ./temp/<file-path>
if __name__ == '__main__': 
    import sys
    if len(sys.argv) >= 3:
        if sys.argv[1] == '-d':
            refine('data/severstal/datamon.xlsx').to_excel(f'.temp/{sys.argv[2]}')
