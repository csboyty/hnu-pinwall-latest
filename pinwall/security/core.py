# coding:utf-8

from flask import current_app, render_template, abort
from flask.ext.login import AnonymousUserMixin, UserMixin as BaseUserMixin, LoginManager, current_user
from flask.ext.principal import Principal, RoleNeed, UserNeed, Identity, identity_loaded
from itsdangerous import URLSafeTimedSerializer
from werkzeug.datastructures import ImmutableList
from werkzeug.local import LocalProxy
from werkzeug.security import safe_str_cmp

from .utils import config_value as cv, get_config, url_for_security, string_types
from .views import create_blueprint
from .forms import LoginForm, SendConfirmationForm, RegisterForm, ChangePasswordForm, ForgotPasswordForm, \
    ResetPasswordForm
from .password_context import PasswordContext

_security = LocalProxy(lambda: current_app.security)

_default_config = {
    'BLUEPRINT_NAME': 'security',
    'URL_PREFIX': None,
    'SUBDOMAIN': None,
    'FLASH_MESSAGES': True,
    'LOGINABLE': False,
    'LOGOUTABLE': False,
    'CONFIRMABLE': False,
    'REGISTERABLE': False,
    'RECOVERABLE': False,
    'TRACKABLE': False,
    'CHANGEABLE': False,
    'IDENTIFIABLE': False,
    'CAPTCHABLE': False,
    'LOGIN_URL': '/login',
    'LOGOUT_URL': '/logout',
    'REGISTER_URL': '/register',
    'CHANGE_URL': '/change_password',
    'CONFIRM_URL': '/confirm',
    'RESET_URL': '/reset',
    'IDENTIFY_EMAIL_URL': '/email_exists',
    'CAPTCHA_URL': "/captcha.jpg",
    'POST_LOGIN_VIEW': '/',
    'POST_LOGOUT_VIEW': '/',
    'CONFIRM_ERROR_VIEW': None,
    'RESET_ERROR_VIEW': "/reset",
    'POST_REGISTER_VIEW': '/',
    'POST_CONFIRM_VIEW': '/',
    'POST_RESET_VIEW': '/',
    'POST_CHANGE_VIEW': '/',
    'LOGIN_WITHOUT_CONFIRMATION': False,
    'DEFAULT_REMEMBER_ME': False,
    'USER_IDENTITY_ATTRIBUTES': ['email'],
    'PASSWORD_PREFIX': None,
    'REMEMBER_SALT': 'remember-salt',
    'CONFIRM_SALT': 'confirm-salt',
    'CONFIRM_EMAIL_WITHIN': '3 days',
    'RESET_SALT': 'reset-salt',
    'RESET_PASSWORD_WITHIN': '3 days',
    'SEND_PASSWORD_RESET_NOTICE_EMAIL': True,
    'EMAIL_SUBJECT_REGISTER': 'Welcome',
    'EMAIL_SUBJECT_CONFIRM': 'Please confirm your email',
    'EMAIL_SUBJECT_PASSWORD_NOTICE': 'Your password has been reset',
    'EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE': 'Your password has been changed',
    'EMAIL_SUBJECT_PASSWORD_RESET': 'Password reset instructions',
    'FORGOT_PASSWORD_TEMPLATE': 'security/forgot_password.html',
    'REGISTER_USER_TEMPLATE': 'security/register_user.html',
    'RESET_PASSWORD_TEMPLATE': 'security/reset_password.html',
    'CHANGE_PASSWORD_TEMPLATE': 'security/change_password.html',
    'SEND_CONFIRMATION_TEMPLATE': 'security/send_confirmation.html',
    'CAPTCHA_SESSION_KEY': 'captcha_chars',
    'CAPTCHA_FUNC': None,
}

_default_forms = {
    'login_form': LoginForm,
    'register_form': RegisterForm,
    'send_confirmation_form': SendConfirmationForm,
    'change_password_form': ChangePasswordForm,
    'forgot_password_form': ForgotPasswordForm,
    'reset_password_form': ResetPasswordForm,
}

_default_messages = {
    'EMAIL_CONFIRMED': (
        'Thank you. Your email has been confirmed.', 'success'),
    'ALREADY_CONFIRMED': (
        'Your email has already been confirmed.', 'info'),
    'INVALID_CONFIRMATION_TOKEN': (
        'Invalid confirmation token.', 'error'),
    'CONFIRMATION_EXPIRED': (
        'You did not confirm your email within %(within)s. New instructions to confirm your email '
        'have been sent to %(email)s.', 'error'),
    'PASSWORD_RESET_REQUEST': (
        'Instructions to reset your password have been sent to %(email)s.', 'info'),
    'INVALID_RESET_PASSWORD_TOKEN': (
        'Invalid reset password token.', 'error'),
    'PASSWORD_RESET_EXPIRED': (
        'You did not reset your password within %(within)s. New instructions have been sent '
        'to %(email)s.', 'error'),
    'PASSWORD_RESET': (
        'You successfully reset your password and you have been logged in automatically.',
        'success'),
    'PASSWORD_RESET_ERROR': (
        'You input password length must more 6 and password confirm must be the same as password',
        'error')
}


def _user_loader(user_id):
    return _security.datastore.find_user(id=user_id)


def _identity_loader():
    if not isinstance(current_user._get_current_object(), AnonymousUser):
        identity = Identity(current_user.id)
        return identity


def _on_identity_loaded(sender, identity):
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    for role in current_user.roles:
        identity.provides.add(RoleNeed(role))

    identity.user = current_user


def _get_login_manager(app):
    lm = LoginManager()
    lm.anonymous_user = AnonymousUser
    lm.login_view = '%s.login' % cv('BLUEPRINT_NAME', app=app)
    lm.user_loader(_user_loader)
    lm.login_message = None
    lm.needs_refresh_message = None
    lm.unauthorized_callback = lambda: abort(401)
    lm.init_app(app)
    return lm


def _get_principal(app):
    p = Principal(app, use_sessions=False)
    p.identity_loader(_identity_loader)
    return p


def _get_pwd_context(app):
    password_prefix = cv('PASSWORD_PREFIX', app=app)
    return PasswordContext(password_prefix)


def _get_serializer(app, name):
    secret_key = app.config.get('SECRET_KEY')
    salt = app.config.get('SECURITY_%s_SALT' % name.upper())
    return URLSafeTimedSerializer(secret_key=secret_key, salt=salt)


def _get_state(app, datastore, **kwargs):
    for key, value in get_config(app).items():
        kwargs[key.lower()] = value

    kwargs.update(dict(
        app=app,
        datastore=datastore,
        login_manager=_get_login_manager(app),
        principal=_get_principal(app),
        pwd_context=_get_pwd_context(app),
        remember_token_serializer=_get_serializer(app, 'remember'),
        confirm_serializer=_get_serializer(app, 'confirm'),
        reset_serializer=_get_serializer(app, 'reset'),
        _context_processors={},
        _send_mail_task=None
    ))

    for key, value in _default_forms.items():
        if key not in kwargs or not kwargs[key]:
            kwargs[key] = value

    return _SecurityState(**kwargs)


def _context_processor():
    return dict(url_for_security=url_for_security, security=_security)


class AnonymousUser(AnonymousUserMixin):
    """AnonymousUser definition"""

    def __init__(self):
        self.roles = ImmutableList()

    def has_role(self, *args):
        """Returns `False`"""
        return False


class _SecurityState(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)

    def _add_ctx_processor(self, endpoint, fn):
        group = self._context_processors.setdefault(endpoint, [])
        fn not in group and group.append(fn)

    def _run_ctx_processor(self, endpoint):
        rv = {}
        for g in [None, endpoint]:
            for fn in self._context_processors.setdefault(g, []):
                rv.update(fn())
        return rv

    def send_confirmation_context_processor(self, fn):
        self._add_ctx_processor('send_confirmation', fn)

    def reset_password_context_processor(self, fn):
        self._add_ctx_processor('reset_password', fn)

    def mail_context_processor(self, fn):
        self._add_ctx_processor('mail', fn)

    def send_mail_task(self, fn):
        self._send_mail_task = fn


class Security(object):
    """
    :param app: The application.
    :param datastore: An instance of a user datastore.

    """

    def __init__(self, app=None, datastore=None, **kwargs):
        self.app = app
        self.datastore = datastore

        if app is not None and datastore is not None:
            self._state = self.init_app(app, datastore, **kwargs)

    def init_app(self, app, datastore=None, register_blueprint=True, **kwargs):
        """
        :param app: The application.
        :param datastore: An instance of a user datastore.
        :param register_blueprint: to register the Security blueprint or not.
        """
        datastore = datastore or self.datastore
        for key, value in _default_config.items():
            app.config.setdefault('SECURITY_' + key, value)

        for key, value in _default_messages.items():
            app.config.setdefault('SECURITY_MSG_' + key, value)

        identity_loaded.connect_via(app)(_on_identity_loaded)

        state = _get_state(app, datastore, **kwargs)

        if register_blueprint:
            app.register_blueprint(create_blueprint(state, __name__))
            app.context_processor(_context_processor)

        state.render_template = self.render_template
        app.security = state
        return state

    def render_template(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._state, name, None)