# coding:utf-8


from flask import current_app, redirect, request, jsonify, Blueprint, after_this_request, abort, session, make_response
from flask_login import current_user
from werkzeug.datastructures import MultiDict
from werkzeug.local import LocalProxy


from .decorators import anonymous_user_required, login_required
from .utils import login_user, logout_user, get_url, do_flash, get_message, config_value
from .registerable import register_user
from .changeable import change_user_password
from .confirmable import send_confirmation_instructions, confirm_email_token_status, confirm_user
from .recoverable import send_reset_password_instrucions, reset_password_token_status, update_password
from ..errors import PinwallError

# Convenient reference
_security = LocalProxy(lambda: current_app.security)

_datastore = LocalProxy(lambda: _security.datastore)


def _render_json(form, include_user=True, error_code=None):
    has_errors = len(form.errors) > 0 or error_code
    response = dict()
    if has_errors:
        # code = 400
        response["success"] = False
        response["error_code"] = "VALIDATION_ERROR" if form.errors else error_code
    else:
        # code = 200
        response["success"] = True
        if include_user:
            response["user"] = form.user

    return jsonify(response)


def _commit(response=None):
    _datastore.commit()
    return response


def _ctx(endpoint):
    return _security._run_ctx_processor(endpoint)


def identify_email():
    email = request.args.get("email", None)
    user = None
    if email:
        user = _datastore.get_user(email)
    return jsonify({"success": True, "exist": True if user else False})


def get_captcha():
    if _security.captchable and _security.captcha_func:
        img_chars, img_buf = _security.captcha_func()
        session[_security.captcha_session_key] = img_chars
        response = make_response(img_buf)
        response.headers['Content-Type'] = 'image/jpeg'
        return response


@anonymous_user_required
def login():
    """View function for login view"""
    form_class = _security.login_form
    error_code = None
    if request.json:
        form = form_class(MultiDict(request.json))
        try:
            if form.validate_on_submit():
                login_user(form.user, remember=form.remember.data)
                after_this_request(_commit)
        except PinwallError, e:
            error_code = e.code

        return _render_json(form, error_code=error_code)


def logout():
    """view function which handles a logout request."""
    if current_user.is_authenticated():
        logout_user()

    return redirect(request.args.get("next", None) or
                    get_url(_security.post_logout_view))


@anonymous_user_required
def register():
    """View function which handles a registration requests."""
    form_class = _security.register_form
    error_code = None
    if request.json:
        form_data = MultiDict(request.json)
        form = form_class(form_data)
        try:
            if form.validate_on_submit():
                user = register_user(**form.to_dict())
                form.user = user

                if not _security.confirmable or _security.login_without_confirmation:
                    after_this_request(_commit)
                    login_user(user)
        except PinwallError, e:
            error_code = e.code

        return _render_json(form, error_code=error_code)
    else:
        abort(406)


@login_required
def change_password():
    form_class = _security.change_password_form
    error_code = None
    if request.json:
        form = form_class(MultiDict(request.json))
        try:
            if form.validate_on_submit():
                after_this_request(_commit)
                change_user_password(current_user, form.new_password.data)
        except PinwallError, e:
            error_code = e.code

        return _render_json(form, include_user=False, error_code=error_code)
    else:
        abort(406)


def send_confirmation():
    """ View function which sends confirmation instructions. """

    form_class = _security.send_confirmation_form
    error_code = None
    if request.json:
        form = form_class(MultiDict(request.json))
        try:
            if form.validate_on_submit():
                send_confirmation_instructions(form.user)
        except PinwallError, e:
            error_code = e.code

    return _render_json(form, include_user=False, error_code=error_code)


def confirm_email(token):
    """ View function which handles a email confirmation request. """

    expired, invalid, user = confirm_email_token_status(token)

    if not user or invalid:
        invalid = True
        do_flash(*get_message("INVALID_CONFIRMATION_TOKEN"))
    if expired:
        send_confirmation_instructions(user)
        do_flash(*get_message("CONFIRMATION_EXPIRED", email=user.email,
                              within=_security.confirm_email_within))
    if invalid or expired:
        return redirect(get_url(_security.confirm_error_view))

    if user != current_user:
        logout_user()
        login_user(user)

    if confirm_user(user):
        after_this_request(_commit)
        msg = "EMAIL_CONFIRMED"
    else:
        msg = "ALREADY_CONFIRMED"

    do_flash(*get_message(msg))
    return redirect(get_url(_security.post_confirm_view))


def forgot_pasword():
    """View function that handles a forgotten password request."""
    form_class = _security.forgot_password_form
    error_code = None

    if request.json:
        form = form_class(MultiDict(request.json))
        try:
            if form.validate_on_submit():
                send_reset_password_instrucions(form.user)
        except PinwallError, e:
            error_code = e.code

        return _render_json(form, include_user=False, error_code=error_code)


@anonymous_user_required
def reset_password(token):
    """View function that handles a reset password request."""
    expired, invalid, user = reset_password_token_status(token)

    if invalid:
        do_flash(*get_message("INVALID_RESET_PASSWORD_TOKEN"))
    if expired:
        do_flash(*get_message("PASSWORD_RESET_EXPIRED", email=user.email,
                              within=_security.reset_password_within))
    if invalid or expired:
        return redirect(get_url(_security.reset_error_view))

    form = _security.reset_password_form()

    if form.validate_on_submit():
        after_this_request(_commit)
        update_password(user, form.password.data)
        do_flash(*get_message("PASSWORD_RESET"))
        login_user(user)
        return redirect(get_url(_security.post_reset_view))
    elif form.errors:
        do_flash(*get_message("PASSWORD_RESET_ERROR"))

    return _security.render_template(config_value("RESET_PASSWORD_TEMPLATE"),
                                     reset_password_form=form,
                                     reset_password_token=token,
                                     **_ctx("reset_password"))


def create_blueprint(state, import_name):
    bp = Blueprint(state.blueprint_name, import_name, url_prefix=state.url_prefix, subdomain=state.subdomain,
                   template_folder="templates")
    if state.logoutable:
        bp.route(state.logout_url, methods=["GET", "POST"], endpoint="logout")(logout)
    if state.loginable:
        bp.route(state.login_url, methods=["POST"], endpoint="login")(login)
    if state.registerable:
        bp.route(state.register_url, methods=["PUT"], endpoint="register")(register)
    if state.changeable:
        bp.route(state.change_url, methods=["POST"], endpoint="change_password")(change_password)
    if state.confirmable:
        bp.route(state.confirm_url, methods=["POST"], endpoint="send_confirmation")(send_confirmation)
        bp.route(state.confirm_url + "/<token>", methods=["GET", "POST"], endpoint="confirm_email")(confirm_email)
    if state.recoverable:
        bp.route(state.reset_url, methods=["POST"], endpoint="forgot_password")(forgot_pasword)
        bp.route(state.reset_url + "/<token>", methods=["GET", "POST"], endpoint="reset_password")(reset_password)
    if state.identifiable:
        bp.route(state.identify_email_url, methods=["GET"], endpoint="identify_email")(identify_email)
    if state.captchable:
        bp.route(state.captcha_url, methods=["GET"], endpoint="captcha_image")(get_captcha)

    return bp
