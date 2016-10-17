# coding: utf-8
"""
    User models
"""
from datetime import datetime
from itsdangerous import text_type

from ..core import db
from ..security import BaseUserMixin
from ..jsoning import JsonSerializer
from ..caching import CacheableMixin, cached_property


user_role_table = db.Table('user_role',
                           db.Column("user_id", db.Integer(), db.ForeignKey("users.id", ondelete="cascade"),
                                     primary_key=True),
                           db.Column("role_id", db.Integer(), db.ForeignKey("roles.id", ondelete="cascade"),
                                     primary_key=True))


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return self.name == other or self.name == getattr(other, "name", None)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class UserCacheMinxin(CacheableMixin):
    __cache_properties__ = ["id", "email", "fullname", "active", "confirmed_at", "registered_at", "roles", "setting"]


class UserJsonSerializer(JsonSerializer):
    __json_public__ = ["id", "email", "fullname", "active", "confirmed_at", "registered_at", "roles", "setting"]


class User(UserCacheMinxin, BaseUserMixin, UserJsonSerializer, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(32))
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    registered_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    setting = db.relationship("UserSetting", uselist=False)
    _roles = db.relationship("Role", secondary=user_role_table, passive_deletes=True)
    _track = db.relationship("UserTrack", uselist=False)

    def is_active(self):
        return self.active

    def has_role(self, role):
        return role in self.roles

    @property
    def roles(self):
        return [role.name for role in self._roles]

    @roles.setter
    def roles(self, value):
        self._roles = []
        for role in value:
            if isinstance(role, Role):
                self._roles.append(role)
            elif isinstance(role, text_type):
                role = Role.query.filter(Role.name == role).first()
                if role is not None:
                    self._roles.append(role)

    def add_role(self, role):
        if isinstance(role, Role):
            self._roles.append(role)
        elif isinstance(role, text_type):
            role = Role.query.filter(Role.name == role).first()
            if role is not None:
                self._roles.append(role)


    def remove_role(self, role):
        if isinstance(role, Role):
            self._roles.remove(role)
        elif isinstance(role, text_type):
            role = Role.query.filter(Role.name == role).first()
            if role is not None:
                self._roles.remove(role)

    @cached_property
    def track(self):
        user_track = self._track
        if user_track is None:
            user_track = self._track = UserTrack()
        return user_track

    def first_load_artifact_id(self, limit=10):
        sql = """select artifacts.id,sum(case artifact_scores.score when 1 then 1 else 0 end) as scores
                    from artifacts
                    left join artifact_scores on  artifacts.id=artifact_scores.artifact_id
                    where artifacts.user_id=:user_id
                    group by artifacts.id
                    order by scores desc,artifacts.created_at desc limit :limit;
                """
        cursor = db.session.execute(sql, {"user_id": self.id, "limit": limit})
        return map(lambda row: row[0], cursor)


    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class UserTrackJsonSerializer(JsonSerializer):
    __json_public__ = ['user_id', 'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip',
                       'login_count']


class UserTrack(UserTrackJsonSerializer, db.Model):
    __tablename__ = "user_tracks"

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="cascade"), primary_key=True)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer())


class UserSettingCacheableMixin(CacheableMixin):
    __cache_properties__ = ["profile_image", "description", "lang", "tz", "comment_active"]


class UserSettingJsonSerializer(JsonSerializer):
    __json_public__ = ["profile_image", "description", "lang", "tz", "comment_active"]


class UserSetting(UserSettingCacheableMixin, UserSettingJsonSerializer, db.Model):
    __tablename__ = "user_settings"

    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="cascade"), primary_key=True)
    profile_image = db.Column(db.String(256))
    description = db.Column(db.String(512))
    lang = db.Column(db.String(5), nullable=False, default="zh_CN")
    tz = db.Column(db.String(20), nullable=False, default="Asia/Shanghai")
    comment_active = db.Column(db.Boolean(), nullable=False, default=True)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)







