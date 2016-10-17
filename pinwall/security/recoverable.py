# coding:utf-8

from flask import current_app as app
from werkzeug.local import LocalProxy

from .signals import password_reset, reset_password_instructions_sent
from .utils import send_mail, md5, encrypt_password, url_for_security, get_token_status, config_value

_security = LocalProxy(lambda: app.security)
_datastore = LocalProxy(lambda: _security.datastore)


def send_reset_password_instrucions(user):
    token = generate_reset_password_token(user)
    reset_link = url_for_security('reset_password', token=token)
    send_mail(config_value('EMAIL_SUBJECT_PASSWORD_RESET'), user.email,
              'reset_instructions', user=user, reset_link=reset_link)
    reset_password_instructions_sent.send(app._get_current_object(), user=user, token=token)


def generate_reset_password_token(user):
    data = [str(user.id), md5(user.password)]
    return _security.reset_serializer.dumps(data)


def reset_password_token_status(token):
    return get_token_status(token, 'reset', 'RESET_PASSWORD')


def update_password(user, password):
    user.password = encrypt_password(password)
    _datastore.put(user)
    send_password_reset_notice(user)


def send_password_reset_notice(user):
    if config_value('SEND_PASSWORD_RESET_NOTICE_EMAIL'):
        send_mail(config_value('EMAIL_SUBJECT_PASSWORD_NOTICE'), user.email,
                  'reset_notice', user=user)
