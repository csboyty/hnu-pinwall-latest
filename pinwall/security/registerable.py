# coding:utf-8

from flask import current_app as app
from werkzeug.local import LocalProxy

from .signals import user_registered
from .utils import config_value, encrypt_password, send_mail
from .confirmable import generate_confirmation_link

_security = LocalProxy(lambda: app.security)
_datastore = LocalProxy(lambda: _security.datastore)


def register_user(**kwargs):
    kwargs['password'] = encrypt_password(kwargs['password'])
    kwargs.update(roles=['user'])
    kwargs.update(setting=_default_user_setting())
    user = _datastore.create_user(**kwargs)
    _datastore.commit()

    if not config_value('LOGIN_WITHOUT_CONFIRMATION'):
        confirmation_link, token = generate_confirmation_link(user)
        send_mail(config_value('EMAIL_SUBJECT_REGISTER'), user.email, 'welcome', user=user,
                  confirmation_link=confirmation_link)
        user_registered.send(app._get_current_object(), user=user, confirm_token=token)
    return user


def _default_user_setting():
    from ..settings import default_user_profile
    from ..users.models import UserSetting

    user_setting = UserSetting()
    user_setting.profile_image = default_user_profile
    return user_setting

