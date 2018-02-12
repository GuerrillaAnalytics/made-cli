"""
Based on tips at
https://julien.danjou.info/blog/2016/python-exceptions-guide
"""


class MadeException(Exception):
    """Base exception for errors raised by made CLI"""

    def __init__(self, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = "An exception occured with made"
        super(MadeException, self).__init__(msg)


class InputException(MadeException):
    """Problems with inputs"""
