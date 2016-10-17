# coding:utf-8

import pkgutil
import importlib
from flask import Flask, Blueprint
import os
from celery import Celery

from security import SQLAlchemyUserDatastore
from .core import db, security, cache, mail, cache_registry, robot
from .users.models import User, Role


if "PSYCOGREEN" in os.environ:
    # Do our monkey patching

    from gevent.monkey import patch_all

    patch_all()
    from psycogreen.gevent import patch_psycopg

    patch_psycopg()


def create_app(package_name, package_path, settings_override=None, register_security_blueprint=True,use_robot=False):
    """Returns a :cloass: `Flask` application instance

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary of setting to override
    :param register_security_blueprint: flag to specify if the security blueprint should be registered
    """
    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('pinwall.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    if isinstance(settings_override, dict):
        app.config.update(settings_override)
    else:
        app.config.from_object(settings_override)

    db.init_app(app)

    if "PSYCOGREEN" in os.environ:
        with app.app_context():
            db.engine.pool._use_threadlocal = True

    security_state = security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                                       register_blueprint=register_security_blueprint)

    if register_security_blueprint:
        from tasks import send_email

        def do_send_mail(msg):
            send_email.delay(msg)

        security_state.send_mail_task(do_send_mail)

    mail.init_app(app)
    cache.init_app(app)
    cache_registry.init_app(app)

    if use_robot:
        robot.init_app(app)

    blueprints = find_blueprints(package_name, package_path)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app


def find_blueprints(package_name, package_path):
    blueprints = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module("%s.%s" % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                blueprints.append(item)

    return blueprints


def create_celery_app(app=None):
    app = app or create_app('pinwall', os.path.dirname(__file__), register_security_blueprint=False)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    #celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_BACKEND_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery










