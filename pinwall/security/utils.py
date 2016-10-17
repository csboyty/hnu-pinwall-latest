# coding:utf-8

import sys
from contextlib import contextmanager
from datetime import datetime, timedelta
import hashlib

from flask import url_for, current_app, request, session, render_template, flash
from werkzeug.local import LocalProxy
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from flask.ext.login import login_user as _login_user, logout_user as _logout_user
from itsdangerous import BadSignature, SignatureExpired
from flask.ext.mail import Message

from ..settings import domain_name


_security = LocalProxy(lambda: current_app.security)
_datastore = LocalProxy(lambda: _security.datastore)
_pwd_context = LocalProxy(lambda: _security.pwd_context)

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    text_type = str
else:
    string_types = basestring
    text_type = unicode


def get_config(app):
    items = app.config.items()
    prefix = "SECURITY_"

    def strip_prefix(tup):
        return tup[0].replace(prefix, ''), tup[1]

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def config_value(key, app=None, default=None):
    app = app or current_app
    return get_config(app).get(key.upper(), default)


def get_message(key, **kwargs):
    rv = config_value('MSG_' + key)
    return rv[0] % kwargs, rv[1]


def get_max_age(key, app=None):
    td = get_within_delta(key + "_WITHIN", app)
    return td.seconds + td.days * 24 * 3600


def get_within_delta(key, app=None):
    """Get a timedelta object from the application configuration following
    the internal convention of::

        <Amount of Units> <Type of Units>

    Examples of valid config values::

        5 days
        10 minutes

    :param key: The config value key without the 'SECURITY_' prefix
    :param app: Optional application to inspect. Defaults to Flask's
                `current_app`
    """
    txt = config_value(key, app=app)
    values = txt.split()
    return timedelta(**{values[1]: int(values[0])})


def encode_string(string):
    if isinstance(string, text_type):
        string = string.encode('utf-8')
    return string


def md5(data):
    return hashlib.md5(encode_string(data)).hexdigest()


def do_flash(message, category=None):
    """Flash a message depending on if the `FLASH_MESSAGES` configuration
    value is set.

    :param message: The flash message
    :param category: The flash message category
    """
    if config_value('FLASH_MESSAGES'):
        flash(message, category)


def get_url(endpoint_or_url):
    """Return a URL if a valid endpoint is found.Otherwise,returns the
    provided value.

    :param endpoint_or_url: The endpoint name or URL to default to
    """
    try:
        return url_for(endpoint_or_url)
    except:
        return endpoint_or_url


def get_security_endpoint_name(endpoint):
    return "%s.%s" % (_security.blueprint_name, endpoint)


def url_for_security(endpoint, **values):
    endpoint = get_security_endpoint_name(endpoint)
    return domain_name + url_for(endpoint, **values)


def send_mail(subject, recipient, template, **context):
    context.setdefault('security', _security)
    context.update(_security._run_ctx_processor('mail'))
    msg = Message(subject, sender=_security.email_sender, recipients=[recipient])
    ctx = ('security/email', template)
    msg.body = render_template('%s/%s.txt' % ctx, **context)
    msg.html = render_template('%s/%s.html' % ctx, **context)

    if _security._send_mail_task:
        _security._send_mail_task(msg)
        return
    mail = current_app.extensions.get('mail')
    mail.send(msg)


def get_token_status(token, serializer, max_age=None):
    """Get the status of a token.

    :param token: The token to check
    :param serializer: The name of the seriailzer. Can be one of the
                       following: ``confirm``,  ``reset``
    :param max_age: The name of the max age config option. Can be on of
                    the following: ``CONFIRM_EMAIL``,  ``RESET_PASSWORD``
    """
    serializer = getattr(_security, serializer + "_serializer")
    max_age = get_max_age(max_age)
    user, data = None, None
    expired, invalid = False, False

    try:
        data = serializer.loads(token, max_age=max_age)
    except SignatureExpired:
        d, data = serializer.loads_unsafe(token)
        expired = True
    except (BadSignature, TypeError, ValueError):
        invalid = True

    if data:
        user = _datastore.find_user(id=data[0])

    expired = expired and (user is not None)
    return expired, invalid, user


def get_identity_attributes(app=None):
    app = app or current_app
    attrs = app.config['SECURITY_USER_IDENTITY_ATTRIBUTES']
    try:
        attrs = [f.strip() for f in attrs.split(',')]
    except AttributeError:
        pass
    return attrs


def login_user(user, remember=None):
    """  Performs the login routine.

    :param user: The user to login
    :param remember: Flag specifying if the remember cookie should be set. Defaults to ``False``
    """
    if remember is None:
        remember = config_value('DEFAULT_REMEMBER_ME')

    if not _login_user(user, remember):
        return False

    if _security.trackable and hasattr(user, "track"):
        user_track = getattr(user, "track")
        # if 'X-Forwarded-For' not in request.headers:
        # remote_addr = request.remote_addr or 'untracable'
        # else:
        #     remote_addr = request.headers.getlist("X-Forwarded-For")[0]
        remote_addr = request.remote_addr or 'untracable'
        old_current_login, new_current_login = user_track.current_login_at, datetime.now()
        old_current_ip, new_current_ip = user_track.current_login_ip, remote_addr

        user_track.last_login_at = old_current_login or new_current_login
        user_track.current_login_at = new_current_login
        user_track.last_login_ip = old_current_ip or new_current_ip
        user_track.current_login_ip = new_current_ip
        user_track.login_count = user_track.login_count + 1 if user_track.login_count else 1

        _datastore.put(user)

    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))
    return True


def logout_user():
    """logs out the current.This will alse clean up the remember me cookie if it exists """
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    _logout_user()


def encrypt_password(password):
    """Encrypts th specified plaintext password  """
    return _pwd_context.encrypt(password)


def verify_password(password, password_hash):
    return _pwd_context.verify_password(password, password_hash)


