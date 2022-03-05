import pandas as pd
import datetime as dt
from scripts.permanent.permanent import *

def refine(path: str, drop=True) -> pd.DataFrame:
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
    if drop:
        data = data.dropna(subset=[order_date_column])
    data[arrival_date_column] = data[arrival_date_column].apply(lambda field: pd.to_datetime(field, infer_datetime_format=True)).dropna
    data[order_date_column] = data[order_date_column].apply(lambda field: pd.to_datetime(field, infer_datetime_format=True))
    return data

# If the script launched on top-level with argument -d <file-path>
# then it will produce refined XLSX file in directory ./temp/<file-path>
if __name__ == '__main__': 
    import sys
    if len(sys.argv) >= 3:
        if sys.argv[1] == '-d':
            refine('data/severstal/datamon.xlsx').to_excel(f'.temp/{sys.argv[2]}')
