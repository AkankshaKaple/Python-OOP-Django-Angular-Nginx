class Error(Exception):

    """
    It will act as Base class for other exceptions
    """

class DataNotFound(Error):

    """
    This Exception will be raised when user does not enter data while post request

    """
class KeyNotFound(Error):

    """
    This Exception will be raised in case of required key is not found
    """

class InvalidCredentials(Error):

    """
    This Exception will be raised in case of invalid credentials entered by user
    """

