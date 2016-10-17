# coding:utf-8

import os
from werkzeug.local import LocalProxy
from werkzeug.exceptions import HTTPException
from functools import wraps
from flask import render_template, current_app, request, jsonify, redirect

from .. import factory
from ..settings import basedir
from ..security import login_required, roles_required, roles_accepted, anonymous_user_required, current_user
from ..jsoning import JSONEncoder
from .. import settings

_logger = LocalProxy(lambda: current_app.logger)


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    import logging
    from logging.handlers import RotatingFileHandler

    log_file = os.path.join(basedir, "logs/front_error.log")
    if not os.path.exists(os.path.dirname(log_file)):
        os.mkdir(os.path.dirname(log_file))
    file_handler = RotatingFileHandler(log_file, 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

    app.json_encoder = JSONEncoder
    # app.jinja_loader = jinja2.ChoiceLoader([
    # app.jinja_loader,
    # jinja2.FileSystemLoader("views"),
    # ])
    app.errorhandler(Exception)(on_exception)
    for e in [401, 403, 404, 500]:
        app.errorhandler(e)(handle_error)

    return app


def handle_error(e):
    if request.headers.get("Content-Type", "").startswith("application/json"):
        if e.code == 500:
            error_code = "UNEXPECTED_ERROR"
        else:
            error_code = e.name.replace(' ', '_').upper()
        return jsonify({"success": False, "error_code": error_code})
    else:
        if isinstance(e, HTTPException) and hasattr(e, "code") and e.code == 401:
            return redirect("/", 302)
        elif isinstance(e, HTTPException) and hasattr(e, "code"):
            return render_template('errors/%s.html' % e.code)
        else:
            return render_template('errors/500.html')

        return render_template('errors/%s.html' % e.code)


def on_exception(e):
    _logger.exception(e)
    if request.headers.get("Content-Type", "").startswith("application/json"):
        return jsonify(dict(success=False, error_code="UNEXPECTED_ERROR"))
    else:
        return render_template("errors/500.html")


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return f

    return decorator


def anonymous_route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return f

    return decorator



