class MovieDoesNotExist(ValueError):
    """
    Error raised by the service layer when the movie is not present
    """

    pass


class MultipleMoviesExist(ValueError):
    """
    Error raised by the service layer when the multiple values are returned by External API
    """

    pass


class DataMappingError(ValueError):
    pass
