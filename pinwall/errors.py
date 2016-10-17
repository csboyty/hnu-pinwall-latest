# coding:utf-8
from functools import wraps
import simplejson as json


class PinwallError(Exception):
    """ Base application error class """

    def __init__(self, msg=None, code=None):
        self.msg = msg
        self.code = code


class PinwallFormError(Exception):
    """
    Raise when an error processing a form occurs.
    """

    def __init__(self, errors=None):
        self.errors = errors


class BoxViewError(Exception):
    def __init__(self, response=None):
        Exception.__init__(self)
        self.status_code = response.status_code if response and hasattr(response, "status_code") else None

        if response is not None and response.headers.get('content-type') == 'application/json':
            self.response_json = response.json()
        else:
            self.response_json = '{}'



def raise_for_view_error(func):
    @wraps(func)
    def checked_for_view_error(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            result.raise_for_status()
            return result
        except Exception, e:
            print e
            raise BoxViewError()

    return checked_for_view_error


