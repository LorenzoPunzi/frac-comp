"""
Module containing the custom exceptions used by the frac-comp program.
"""


class FileFormatError(Exception):
    """
    Exception that gives an error message if an input file is not correctly formatted.
    """

    def __init__(self, msg):
        """
        :param source: Message to be printed as the error.
        :type source: str
        """
        super().__init__(msg)