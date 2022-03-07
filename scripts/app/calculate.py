import pandas as pd
from time import mktime
import sklearn.linear_model as skl


def predict_price(prices: dict, external: list[dict] = None):
    time = set(_ for _ in prices.keys())
    if external is not None:
        x = []
        for t in time:
            x.append([t] + [prices[t]] + [_[t] for _ in external])
        linear = skl.LinearRegression()
        return linear.predict(x)
    else:
        x = list(prices.values())
        linear = skl.LinearRegression()
        data = [[mktime(x.timetuple()), y] for x, y in prices.items()]
        linear.fit(data[:-2], data[-1:])
        return linear.predict(x)

