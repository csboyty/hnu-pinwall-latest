# coding: utf-8

from flask import current_app
from ..core import db, cache, cache_registry, Service
from .models import User, UserSetting, Role
from ..signals import user_update_signal, user_delete_signal, user_confirmed, qiniu_unregister_key_signal
from ..settings import cache_timeout


class RoleService(Service):
    __model__ = Role


class UserService(Service):
    __model__ = User

    @cache.memoize(timeout=cache_timeout)
    def user_by_id(self, user_id):
        user = self.get(user_id)
        if user:
            return user.to_cache_dict()
        else:
            return None


    @cache.memoize(timeout=cache_timeout)
    def first_load_artifact_ids(self, user_id, limit=10):
        user = self.get(user_id)
        if user:
            return user.first_load_artifact_id(limit)
        else:
            return None

    @cache.memoize(timeout=cache_timeout)
    def user_comment_count(self, user_id):
        user = self.get(user_id)
        if user:
            return user.comment_query.with_entities(db.func.count("*")).scalar()
        else:
            return None

    def change_user_role_by_id(self, user_id, roles):
        user = self.get_or_404(user_id)
        user.roles = roles
        self.save(user)
        user_update_signal.send(current_app._get_current_object(), user_id=user_id)

    def update_user(self, user_id, **kwargs):
        user = self.get_or_404(user_id)
        setting = kwargs.pop("setting", None)
        if setting:
            setting = db.session.merge(setting)
            kwargs['setting'] = setting
        self.update(user, **kwargs)
        user_update_signal.send(current_app._get_current_object(), user_id=user_id)
        if setting:
            qiniu_unregister_key_signal.send(current_app._get_current_object(), qiniu_keys=[setting.profile_image])

    def delete_user_by_id(self, user_id):
        user = self.get_or_404(user_id)
        self.delete(user)
        user_delete_signal.send(current_app._get_current_object(), user_id=user_id)

    def __repr__(self):
        return "pinwall.users.UserService"


roleService = RoleService()

userService = UserService()
cache_registry.register("pinwall.users.UserService.user_by_id", userService.user_by_id)
cache_registry.register("pinwall.users.UserService.first_load_artifact_ids", userService.first_load_artifact_ids)
cache_registry.register("pinwall.users.UserService.user_comment_count", userService.user_comment_count)


















