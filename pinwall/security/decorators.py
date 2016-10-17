# coding:utf-8

from collections import namedtuple
from functools import wraps

from flask import current_app, request, redirect, Response, abort
from flask.json import dumps
from flask.ext.login import current_user, login_required
from flask.ext.principal import RoleNeed, Permission, Identity, identity_changed
from werkzeug.local import LocalProxy

from . import utils

# Convenient reference
_security = LocalProxy(lambda: current_app.security)


def roles_required(*roles):
    """Decorator which specifies that a user must have all the specified roles.
    Example::

        @app.route('/dashboard')
        @roles_required('admin', 'editor')
        def dashboard():
            return 'Dashboard'

    The current user must have both the `admin` role and `editor` role in order
    to view the page.

    :param args: The required roles.
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perms = [Permission(RoleNeed(role)) for role in roles]
            for perm in perms:
                if not perm.can():
                    abort(403)
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def roles_accepted(*roles):
    """Decorator which specifies that a user must have at least one of the
    specified roles. Example::

        @app.route('/create_post')
        @roles_accepted('editor', 'author')
        def create_post():
            return 'Create Post'

    The current user must have either the `editor` role or `author` role in
    order to view the page.

    :param args: The possible roles.
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*[RoleNeed(role) for role in roles])
            if perm.can():
                return fn(*args, **kwargs)
            abort(403)

        return decorated_view

    return wrapper


def anonymous_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print "anonymous_user_required"
        if current_user.is_authenticated() and request.headers.get("Content-Type",None) != "application/json":
            return redirect(utils.get_url(_security.post_login_view))
        return f(*args, **kwargs)

    return wrapper