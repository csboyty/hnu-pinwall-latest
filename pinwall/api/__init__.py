# coding: utf-8

from functools import wraps
from werkzeug.local import LocalProxy
from flask import jsonify, current_app, abort
import os

from ..settings import basedir
from .. import factory, angulars
from ..errors import *
from ..core import cache_registry, db
from ..jsoning import JSONEncoder
from ..security import login_required, roles_required, roles_accepted, current_user
from ..resultproxy import ResultProxyMixin


_logger = LocalProxy(lambda: current_app.logger)


def create_app(settings_override=None, register_security_blueprint=False):
    app = factory.create_app(__name__, __path__, settings_override,
                             register_security_blueprint=register_security_blueprint)

    import logging
    from logging.handlers import RotatingFileHandler

    log_file = os.path.join(basedir, "logs/api_error.log")
    if not os.path.exists(os.path.dirname(log_file)):
        os.mkdir(os.path.dirname(log_file))
    file_handler = RotatingFileHandler(log_file, 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    app.json_encoder = JSONEncoder

    app.errorhandler(PinwallError)(on_pinwall_error)
    app.errorhandler(Exception)(on_exception)
    app.errorhandler(400)(on_400)
    app.errorhandler(401)(on_401)
    app.errorhandler(403)(on_403)
    app.errorhandler(404)(on_404)

    return app


def on_pinwall_error(e):
    return jsonify(dict(success=False, error_code=e.code, error=e.msg))


def on_exception(e):
    _logger.exception(e)
    return jsonify(dict(success=False, error_code="UNEXPECTED_ERROR"))


def on_400(e):
    return jsonify(dict(success=False, error_code="BAD_REQUEST"))


def on_401(e):
    return jsonify(dict(success=False, error_code="UNAUTHORIZED"))


def on_403(e):
    return jsonify(dict(success=False, error_code="FORBIDDEN"))


def on_404(e):
    return jsonify(dict(success=False, error_code="NOT_FOUND"))


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(rv), sc

        return f

    return decorator


def anonymous_route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(rv), sc

        return f

    return decorator



