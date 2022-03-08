from sklearn.linear_model import LinearRegression


class PricePredictor:
    """
    The class for multiple regression model used for
    price prediction
    """
    def __init__(self, indices: list, prices: list):
        """
        :param indices: Training indices
        :param prices: Corresponding prices
        """
        self._prices = prices
        self._indices = indices
        self._model = LinearRegression()
        self._model.fit(indices, prices)

    def predict(self, predicted_indices: list):
        """
        Predict the price for the given values of indices
        :param predicted_indices: The values of indices
        :return: Predicted price
        """
        return self._model.predict(predicted_indices)



