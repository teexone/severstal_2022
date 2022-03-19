import datetime
import math

import scipy
import sklearn.linear_model as skl
import sklearn.metrics as skm
import numpy as np
import scipy.stats as st

from appparser.ParserModule import ParserModule
from appformat.date import int_to_date, date_to_int


class Predictor:
    def __predict_linear__(self, time_array: list, data_array: list):
        pass

    def __predict_square__(self, time_array: list, data_array: list):
        pass

    def __predict_cubic__(self, time_array: list, data_array: list):
        pass

    def __predict_exp__(self, time_array: list, data_array: list):
        pass

    def predict(self, time_array: list, data_array: list):
        pass


class PricePredictor:
    class TrainingData:
        """
        Training data. Contains two vectors: the matrix X and the
        vector of variables y
        """

        def __init__(self, prices: list[float], data: list[list[float]]):
            self.X = data
            self.y = prices

    def __init__(self, prices: [(datetime.time, float)]):
        self.__training_data__ = PricePredictor.TrainingData([], [])
        self.__times__ = []
        self.__modules__: list[ParserModule] = []
        for time, price in prices:
            self.__times__.append(time)
            self.__training_data__.y.append(price)
            self.__training_data__.X.append([])

    @staticmethod
    def __linear_regression__(t: list[float], f_t: list[float]):
        slope, intercept, r, p, std_err = st.linregress(t, f_t)

        def f(time: float):
            return time * slope + intercept

        return f, r,

    @staticmethod
    def __quadratic_regression__(t: list[float], f_t: list[float]):
        model = np.poly1d(np.polyfit(t, f_t, 2))
        return model, skm.r2_score(f_t, model(t))

    @staticmethod
    def __cubic_regression__(t: list[float], f_t: list[float]):
        model = np.poly1d(np.polyfit(t, f_t, 3))
        return model, skm.r2_score(f_t, model(t))

    @staticmethod
    def __exponential_regression__(t: list[float], f_t: list[float]):
        fit = np.polyfit(t, np.log(f_t), 1)

        def exp(time):
            return math.exp(fit[1] + fit[0] * time)

        return exp, skm.r2_score(f_t, [exp(_) for _ in t])

    def __predict_external_sep__(self, date: datetime.date):
        result = []
        for module in self.__modules__:
            result.append([])
            data = module.get_data()
            length = min(len(_) for _ in data.values())
            for i in range(length):
                arr = [PricePredictor.__linear_regression__
                       ([date_to_int(_) for _ in data.keys()], [_[i] for _ in data.values()]),
                       PricePredictor.__quadratic_regression__
                       ([date_to_int(_) for _ in data.keys()], [_[i] for _ in data.values()]),
                       PricePredictor.__exponential_regression__
                       ([date_to_int(_) for _ in data.keys()], [_[i] for _ in data.values()]),
                       PricePredictor.__cubic_regression__
                       ([date_to_int(_) for _ in data.keys()], [_[i] for _ in data.values()])]
                time = [date_to_int(_) for _ in data.keys()]
                tval = [_[i] for _ in data.values()]
                func, r = max(arr, key=lambda x: x[1])
                e = np.square(np.subtract(tval, [func(t) for t in time]))
                el, er = np.sqrt(scipy.stats.t.interval(.95, len(e) - 1, loc=np.mean(e), scale=scipy.stats.sem(e)))
                i = func(date_to_int(date))
                result[-1].append((i - el, i, i + er,))
        return result

    def __predict_external__(self, date: datetime.date):
        return sum(self.__predict_external_sep__(date), [])

    def attach_parser(self, parser: ParserModule):
        """
        Attaches new data and adds the information to the training data matrix

        :param parser: ParserModule
            The parser of an additional information
        """
        self.__modules__.append(parser)
        for i, time in enumerate(self.__times__):
            self.__training_data__.X[i] += parser.get_data_at(int_to_date(time))

    def predict_price(self, date: datetime.date):
        """
        Main prediction method. Exploits sklearn...LinearRegressionModel to predict
        the future price

        :param date: datetime.date
            The future date
        :return:
            Predicted price
        """
        model = skl.LinearRegression()
        model.fit(self.__training_data__.X, self.__training_data__.y)
        external = self.__predict_external__(date)
        return model.predict([[_[0] for _ in external]]), model.predict([[_[1] for _ in external]]), model.predict(
            [[_[2] for _ in external]])
