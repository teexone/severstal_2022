from collections import defaultdict
from typing import Union
from appparser.ParserModule import ParserModule
import appformat.date as dateformat
# from .. import dateformat
from datetime import timedelta, date
import pandas as pd


class IndicesParserModule(ParserModule):

    def __init__(self, filepath: str, sheet: Union[int, str], header_columns_count=0, header_rows_count=2):
        df = pd.read_excel(filepath, sheet_name=sheet)
        self.__data__ = []
        for i in range(header_columns_count, len(df.index)):
            self.__data__.append([])
            index_data = list(df.iloc[i, header_rows_count:].to_dict().items())
            coefficient_data = []
            _2020, last = None, None
            for j in range(1, len(index_data)):
                k, v = index_data[j]
                nk, nv = index_data[j - 1]
                t, nt = dateformat.from_external_date(str(k)), dateformat.from_external_date(str(nk))
                if t.year < 2016:
                    continue
                if t.year == 2020:
                    if _2020 is None:
                        _2020 = v
                if len(coefficient_data) == 0:
                    coefficient_data.append((t, 1))
                    continue
                if t.year == 2021:
                    coefficient_data.append((t, int(coefficient_data[-1][1] * _2020) / 100))
                else:
                    coefficient_data.append((t, int(coefficient_data[-1][1] * nv) / 100))
            for j in range(1, len(coefficient_data) - 1):
                t, v = coefficient_data[j - 1][0], coefficient_data[j - 1][1]
                nt, nv = coefficient_data[j][0], coefficient_data[j][1]
                if t.year < 2016:
                    continue
                m_delta = (nt - t).days
                it = timedelta(days=0)
                while it.days != m_delta:
                    self.__data__[-1].append((dateformat.date_to_int(t + it), int((v + (nv - v) * it.days / m_delta) * 10) / 10))
                    last = t + it
                    it = it + timedelta(days=1)
            while last < date.today():
                self.__data__[-1].append((dateformat.date_to_int(last), self.__data__[-1][-1][1]))
                last += timedelta(days=1)
        pass

    def get_data(self):
        fl = defaultdict(list)
        for index in self.__data__:
            for k, v in index:
                fl[dateformat.int_to_date(k)].append(v)
        return fl

    def get_data_at(self, t: date):
        vector = []
        for i in self.__data__:
            for time, v in i:
                if dateformat.date_to_int(t) == time:
                    vector.append(v)
        return vector
