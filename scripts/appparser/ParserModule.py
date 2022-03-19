import datetime


class ParserModule:
    def get_data_at(self, time: datetime.date) -> list[float]:
        """
        Retrieves the data at the given time
        :param time: The time to get data at
        :return: The numerical data in the array form
        """
        pass

    def get_data(self) -> dict[datetime.date, list[float]]:
        """
        Retrieve all the data available
        :return: Dictionary with time keys and array values
        """
        pass

