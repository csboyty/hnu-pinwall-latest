# coding:utf-8

import inspect
from flask import request, current_app, session
from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, BooleanField, validators, \
    ValidationError, Field
from flask_login import current_user
from werkzeug.local import LocalProxy
from .utils import config_value, verify_password
from ..errors import PinwallError

_security = LocalProxy(lambda: current_app.security)
_datastore = LocalProxy(lambda: current_app.security.datastore)


def unique_user_email(form, field):
    if _datastore.find_user(email=field.data) is not None:
        raise PinwallError(code="EMAIL_ALREADY_ASSOCIATED")


def valid_user_email(form, field):
    form.user = _datastore.find_user(email=field.data)
    if form.user is None:
        raise PinwallError(code="USER_NOT_EXIST")


def valid_captcha(form, field):
    input_captcha = field.data
    saved_captcha = session.get(_security.captcha_session_key, '')
    if input_captcha.lower() != saved_captcha.lower():
        raise PinwallError(code="CAPTCHA_NOT_MATCH")


class LoginForm(Form):
    """ The login form  """
    email = TextField(validators=[validators.Email(message="INVALID_EMAIL_ADDRESS")])
    password = PasswordField(validators=[validators.Length(min=6, max=20, message="PASSWORD_LENGTH_NOT_MATCH")])
    remember = BooleanField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.remember.default = config_value("DEFAULT_REMEMBER_ME")


    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        self.user = _datastore.get_user(self.email.data)

        if self.user is None:
            raise PinwallError(code="USER_NOT_EXIST")
        if not self.user.password:
            raise PinwallError(code="PASSWORD_NOT_SET")
        if not verify_password(self.password.data, self.user.password):
            raise PinwallError(code="INVALID_PASSWORD")
        return True


class RegisterForm(Form):
    """ The register form """
    captcha = TextField(validators=[validators.length(min=6, max=6, message="CAPTCHA_LENGTH_NOT_MATCH"), valid_captcha])
    email = TextField(validators=[validators.Email(message="INVALID_EMAIL_ADDRESS"), unique_user_email])
    password = PasswordField(validators=[validators.Length(min=6, max=20, message="PASSWORD_LENGTH_NOT_MATCH")])
    fullname = TextField(validators=[validators.Length(min=2, max=32, message="FULLNAME_LENGTH_NOT_MATCH")])

    def validate(self):
        if not super(RegisterForm, self).validate():
            return False
        return True

    def to_dict(form):
        def is_field_and_user_attr(member):
            return isinstance(member, Field) and \
                   hasattr(_datastore.user_model, member.name)

        fields = inspect.getmembers(form, is_field_and_user_attr)
        return dict((key, value.data) for key, value in fields)


class ChangePasswordForm(Form):
    password = PasswordField(validators=[validators.Length(min=6, max=20, message="PASSWORD_LENGTH_NOT_MATCH")])
    new_password = PasswordField(validators=[validators.Length(min=6, max=20, message="PASSWORD_LENGTH_NOT_MATCH")])

    def validate(self):
        if not super(ChangePasswordForm, self).validate():
            return False
        if not verify_password(self.password.data, current_user.password):
            raise PinwallError(code="PASSWORD_NOT_MATCH")
        return True


class SendConfirmationForm(Form):
    email = TextField(validators=[validators.Email(message="INVALID_EMAIL_ADDRESS"), valid_user_email])

    def validate(self):
        if not super(SendConfirmationForm, self).validate():
            return False
        if self.user.confirmed_at is not None:
            raise PinwallError(code="USER_ALREADY_CONFIRMED")
        return True


class ForgotPasswordForm(Form):
    email = TextField(validators=[validators.Email(message="INVALID_EMAIL_ADDRESS"), valid_user_email])


class ResetPasswordForm(Form):
    password = PasswordField("Password",
                             validators=[validators.Length(min=6, max=20, message="PASSWORD_LENGTH_NOT_MATCH")])
    password_confirm = PasswordField("Retype password",
                                     validators=[validators.EqualTo("password", message="RETYPE_PASSWORD_MISMATCH")])
    submit = SubmitField("Reset password")
