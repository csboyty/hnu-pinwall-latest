# coding:utf-8

from datetime import datetime

from flask import current_app as app
from werkzeug.local import LocalProxy
from .utils import send_mail, md5, url_for_security, get_token_status, config_value
from .signals import user_confirmed, confirm_instructions_sent

_security = LocalProxy(lambda: app.security)
_datastore = LocalProxy(lambda: _security.datastore)


def generate_confirmation_link(user):
    token = generate_confirmation_token(user)
    return url_for_security('confirm_email', token=token), token


def generate_confirmation_token(user):
    data = [str(user.id), md5(user.email)]
    return _security.confirm_serializer.dumps(data)


def send_confirmation_instructions(user):
    confirmation_link, token = generate_confirmation_link(user)
    send_mail(config_value('EMAIL_SUBJECT_CONFIRM'), user.email,
              'confirmation_instructions', user=user,
              confirmation_link=confirmation_link)
    confirm_instructions_sent.send(app._get_current_object(), user=user)
    return token


def confirm_email_token_status(token):
    return get_token_status(token, 'confirm', 'CONFIRM_EMAIL')


def confirm_user(user):
    if user.confirmed_at is not None:
        return False
    user.active = True
    user.confirmed_at = datetime.now()
    _datastore.put(user)
    user_confirmed.send(app._get_current_object(), user=user)
    return True