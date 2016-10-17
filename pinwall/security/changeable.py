# coding:utf-8

from flask import current_app as app
from werkzeug.local import LocalProxy

from .signals import password_changed
from .utils import encrypt_password, config_value

_security = LocalProxy(lambda: app.security)
_datastore = LocalProxy(lambda: _security.datastore)


def change_user_password(user, password):
    user.password = encrypt_password(password)
    _datastore.put(user)
    password_changed.send(app._get_current_object(), user=user)