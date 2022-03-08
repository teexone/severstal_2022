
import numpy as np
import math

from sklearn.metrics import r2_score
from scipy import stats


class IndexPredictionResult:
    """
    Class for index prediction results
    """
    def __init__(self, predicted=None, r2=None):
        """
        :param predicted: Predict value of the index
        :param r2: R2 metric
        """
        self.predicted = predicted
        self.r2 = r2


def predict_all_indices(indices: list, date: int, method: str):
    """
    Produces predictions for all the indices categories

    :param indices: Indices data through years (list of index data)
    :param date: The date to predict
    :param method: The prediction method
    :return: The array of the predicted intervals for each of the given index
    """
    return [predict_indices(_, date, method) for _ in indices]


def predict_indices(data: list, date: int, method: str):
    """
    Predict the index using one of the following regression modules:
    -- Linear regression
    -- Polynomial regression (quadratic and cubic)
    -- Exponential regression

    :param data: Index data through time
    :param date: The date to predict at
    :param method: Which method to use
    :return: Predicted index
    """
    t = [_[0] for _ in data]
    i_t = [_[1] for _ in data]
    if method == 'exponential':
        return predict_indices_exponential(t, i_t, date)
    elif method == 'linear':
        return predict_indices_linear(t, i_t, date)
    elif method == 'quadratic':
        return predict_indices_polynomial(t, i_t, date, 2)
    elif method == 'cubic':
        return predict_indices_polynomial(t, i_t, date, 3)


def predict_indices_linear(t, i_t, date: int) -> IndexPredictionResult:
    """
    Linear prediction for index

    :param t: The time array
    :param i_t: Known values of indices for time entries
    :param date: The date to predict the value at
    :return: The predict value as IndexPredictionResult
    """
    slope, intercept, r, p, std_err = stats.linregress(t, i_t)

    def f(x):
        return slope * x + intercept
    return IndexPredictionResult(predicted=f(date), r2=r)


def predict_indices_polynomial(t, i_t,  date: int, degree: int) -> IndexPredictionResult:
    """
    Polynomial prediction for index

    :param t: The time array
    :param i_t: Known values of indices for time entries
    :param date: The date to predict the value at
    :param degree: The degree of the polynomial approximation
    :return: The predict value as IndexPredictionResult
    """
    model = np.poly1d(np.polyfit(t, i_t, degree))
    return IndexPredictionResult(predicted=model(date), r2=r2_score(i_t, model(t)))


def predict_indices_exponential(t, i_t, date: int) -> IndexPredictionResult:
    """
    Exponential prediction for index

    :param t: The time array
    :param i_t: Known values of indices for time entries
    :param date: The date to predict the value at
    :return: The predict value as IndexPredictionResult
    """
    fit = np.polyfit(t, np.log(i_t), 1)

    def exp(time):
        return math.exp(fit[1] + fit[0] * time)
    val = exp(date)
    return IndexPredictionResult(predicted=val, r2=r2_score(i_t, [exp(_) for _ in t]))

