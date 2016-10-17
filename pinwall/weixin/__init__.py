# coding:utf-8

import os
from werkzeug.local import LocalProxy
from flask import current_app
from .. import factory
from ..settings import basedir


_logger = LocalProxy(lambda: current_app.logger)


def create_app(settings_override=None,register_security_blueprint=False):
    app = factory.create_app(__name__, __path__, settings_override, register_security_blueprint,use_robot=True)

    import logging
    from logging.handlers import RotatingFileHandler

    log_file = os.path.join(basedir, "logs/weixin.log")
    if not os.path.exists(os.path.dirname(log_file)):
        os.mkdir(os.path.dirname(log_file))
    file_handler = RotatingFileHandler(log_file, 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)
    return app



