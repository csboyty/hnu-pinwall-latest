# coding:utf-8

from functools import partial, wraps
from core import cache_registry
from utils import format_date


class ResultProxyMixin(object):
    def result(self):
        raise NotImplementedError()


class ResultProxyList(ResultProxyMixin, list):
    def result(self):
        rv = []
        for item in self:
            if isinstance(item, ResultProxyMixin):
                rv.append(item.result())
            else:
                rv.append(item)

        return rv


class ResultProxyDict(ResultProxyMixin, dict):
    def result(self):
        rv = {}
        for key, value in self.iteritems():
            if isinstance(value, ResultProxyMixin):
                rv[key] = value.result()
            else:
                rv[key] = value

        return rv


class LazyResultProxy(ResultProxyMixin):
    def __init__(self, callable_object):
        if not callable(callable_object):
            raise TypeError("Not callable")
        self.callable_object = callable_object

    def result(self):
        return self.callable_object()


class PartialableResultProxy(LazyResultProxy):
    def __init__(self, func, *args, **kwargs):
        partial_object = partial(func, *args, **kwargs)
        super(PartialableResultProxy, self).__init__(partial_object)


def result_proxy_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sc = 200
        rv = func(*args, **kwargs)
        if isinstance(rv, tuple):
            sc = rv[1]
            rv = rv[0]
        if isinstance(rv, ResultProxyMixin):
            rv = rv.result()
        return rv, sc

    return wrapper


class UserResultProxy(ResultProxyMixin):
    def __init__(self, user_id, load_top_10_artifacts=False):
        self.user_id = user_id
        self.load_top_10_artifacts = load_top_10_artifacts

    def result(self):
        rv = {}
        user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(self.user_id)
        user_artifact = cache_registry.lookup("pinwall.artifacts.ArtifactService.artifact_by_userid")(self.user_id)
        rv['user'] = user if user else None
        rv['artifact_count'] = len(user_artifact.get("artifact_ids")) if user_artifact else 0
        rv['honor_sum'] = user_artifact.get("honor_sum") if user_artifact else 0
        comment_count = cache_registry.lookup("pinwall.users.UserService.user_comment_count")(self.user_id)
        rv['comment_count'] = comment_count if comment_count else 0
        if self.load_top_10_artifacts:
            first_load_artifact_ids = cache_registry.lookup("pinwall.users.UserService.first_load_artifact_ids")(
                self.user_id)
            artifacts = []
            if first_load_artifact_ids:
                for artifact_id in first_load_artifact_ids:
                    artifact = ArtifactResultProxy(artifact_id, show_user=False).result()
                    if artifact:
                        artifact["created_at"] = format_date(artifact.get("created_at"))
                        artifacts.append(artifact)

            rv["artifacts"] = artifacts

        return rv


class TopicResultProxy(ResultProxyMixin):
    def __init__(self, topic_id):
        self.topic_id = topic_id

    def result(self):
        rv = {}
        topic = cache_registry.lookup("pinwall.artifacts.TopicService.topic_by_id")(self.topic_id)
        first_load_artifacts = []
        if topic:
            user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(topic["user_id"])
            first_load_artifact_ids = cache_registry.lookup("pinwall.artifacts.TopicService.first_load_artifact_ids")(
                self.topic_id)
            if first_load_artifact_ids:
                for artifact_id in first_load_artifact_ids:
                    artifact = ArtifactResultProxy(artifact_id, show_topic=False).result()
                    if artifact:
                        artifact["created_at"] = format_date(artifact.get("created_at"))
                        first_load_artifacts.append(artifact)

        rv["topic"] = topic if topic else None
        rv["user"] = user if user else None
        rv["artifacts"] = first_load_artifacts
        return rv


class ArtifactResultProxy(ResultProxyMixin):
    def __init__(self, artifact_id, show_user=True, show_topic=True):
        self.artifact_id = artifact_id
        self.show_user = show_user
        self.show_topic = show_topic

    def result(self):
        rv = {}
        artifact = cache_registry.lookup("pinwall.artifacts.ArtifactService.artifact_by_id")(self.artifact_id)
        if artifact:
            artifact["created_at"] = format_date(artifact.get("created_at"))
            rv["artifact"] = artifact
            if self.show_user:
                user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(artifact["user_id"])
                rv["user"] = user if user else None
            if artifact.get("topic_id", None) and self.show_topic:
                topic = cache_registry.lookup("pinwall.artifacts.TopicService.topic_by_id")(artifact["topic_id"])
                if topic:
                    topic["created_at"] = format_date(topic.get("created_at"))
                rv["topic"] = topic if topic else None
        return rv


class CommentResultProxy(ResultProxyMixin):
    def __init__(self, comment, show_artifact=False):
        self.comment = comment
        self.show_artifact = show_artifact

    def result(self):
        rv = {}
        user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(self.comment.commenter_id)
        rv["comment"] = self.comment
        rv["user"] = user if user else None
        if self.show_artifact:
            artifact = cache_registry.lookup("pinwall.artifacts.ArtifactService.artifact_by_id")(
                self.comment.artifact_id)
            if artifact:
                artifact["created_at"] = format_date(artifact["created_at"])
            rv["artifact"] = artifact if artifact else None
        return rv













