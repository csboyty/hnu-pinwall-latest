# coding: utf-8

import pypinyin
import blinker

from core import cache, db, cache_registry
from security import user_confirmed
from settings import show_boxview_uri

from utils import format_datetime

signals = blinker.Namespace()

user_update_signal = signals.signal("user_update")

user_delete_signal = signals.signal("user_delete")

user_top_10_artifacts_signal = signals.signal("user_top_10_artifacts")

artifact_create_signal = signals.signal("artifact_create")

artifact_update_signal = signals.signal("artifact_update")

artifact_delete_signal = signals.signal("artifact_delete")

artifact_asset_html5_url_update_signal = signals.signal("artifact_asset_html5_url_update")

artifact_asset_boxview_url_update_signal = signals.signal("artifact_asset_boxview_url_update")

artifact_praised_signal = signals.signal("artifact_praised_signal")

artifact_comment_append_signal = signals.signal("artifact_comment_append_signal")

artifact_comment_remove_signal = signals.signal("artifact_comment_remove_signal")

topic_create_signal = signals.signal("topic_create")

topic_update_signal = signals.signal("topic_update")

topic_delete_signal = signals.signal("topic_delete")

qiniu_unregister_key_signal = signals.signal("qiniu_unregister_key")


@user_confirmed.connect
@user_update_signal.connect
def on_user_update(app, user_id=None, user=None):
    from services import userService

    user_id = user_id or user.id
    cache.delete_memoized(userService.user_by_id, userService, user_id)
    es_index_user(user_id)


@user_delete_signal.connect
def on_user_deleted(app, user_id=None):
    from services import userService, topicService, artifactService

    cache.delete_memoized(userService.user_by_id, userService, user_id)
    cache.delete_memoized(userService.first_load_artifact_ids, userService, user_id, 10)
    cache.delete_memoized(userService.user_comment_count, userService, user_id)
    es_delete_user(user_id)

    topic_ids = topicService.topic_ids_by_userid(user_id)
    if topic_ids:
        for topic_id in topic_ids:
            cache.delete_memoized(topicService.topic_by_id, topicService, topic_id)

        cache.delete_memoized(topicService.topic_ids_by_userid, topicService, user_id)

    user_artifact = artifactService.artifact_by_userid(user_id)
    if user_artifact["artifact_ids"]:
        for artifact_id in user_artifact["artifact_ids"]:
            cache.delete_memoized(artifactService.artifact_by_id, artifactService, artifact_id)

    cache.delete_memoized(artifactService.artifact_by_userid, artifactService, user_id)


@artifact_create_signal.connect
def on_artifact_create(app, artifact=None):
    from services import artifactService

    cache.delete_memoized(artifactService.artifact_by_userid, artifactService, artifact.user_id)
    es_index_artifact(artifact.id)


@artifact_update_signal.connect
def on_artifact_update(app, artifact=None):
    from services import artifactService

    cache.delete_memoized(artifactService.artifact_by_id, artifactService, artifact.id)
    cache.delete_memoized(artifactService.artifact_by_userid, artifactService, artifact.user_id)
    es_index_artifact(artifact.id)


@artifact_delete_signal.connect
def on_artifact_delete(app, artifact=None):
    from services import artifactService

    cache.delete_memoized(artifactService.artifact_by_id, artifactService, artifact.id)
    cache.delete_memoized(artifactService.artifact_by_userid, artifactService, artifact.user_id)
    es_delete_artifact(artifact.id)

@artifact_asset_boxview_url_update_signal.connect
def on_asset_boxview_url_update(app, artifact_id=None, media_file=None, view_url=None):
    from services import artifactService
    from models import ArtifactAsset

    # print "artifact_asset_view_url_update_signal:", artifact_id, media_file, view_url
    if artifact_id and media_file and view_url:
        boxview_url = show_boxview_uri + "?" + view_url
        db.session.query(ArtifactAsset). \
            filter(ArtifactAsset.artifact_id == artifact_id, ArtifactAsset.media_file == media_file). \
            update({'view_url': boxview_url})
        db.session.commit()
        cache.delete_memoized(artifactService.artifact_by_id, artifactService, artifact_id)


@artifact_asset_html5_url_update_signal.connect
def on_asset_html5_url_update(app, artifact_id=None, media_file=None, view_url=None):
    from services import artifactService
    from models import ArtifactAsset

    if artifact_id and media_file and view_url:
        db.session.query(ArtifactAsset). \
            filter(ArtifactAsset.artifact_id == artifact_id, ArtifactAsset.media_file == media_file). \
            update({'view_url': view_url})
        db.session.commit()
        cache.delete_memoized(artifactService.artifact_by_id, artifactService, artifact_id)




@artifact_praised_signal.connect
def on_artifact_praised(app, artifact_id=None, scorer_id=None):
    from services import artifactService

    cache.delete_memoized(artifactService.artifact_praised_by_userid, artifactService, artifact_id, scorer_id)


@topic_create_signal.connect
def on_topic_create(app, topic=None):
    from services import topicService

    cache.delete_memoized(topicService.topic_ids_by_userid, topicService, topic.user_id)
    es_index_topic(topic.id)


@topic_update_signal.connect
def on_topic_update(app, topic=None):
    from services import topicService

    cache.delete_memoized(topicService.topic_by_id, topicService, topic.id)
    cache.delete_memoized(topicService.first_load_artifact_ids, topicService, topic.id, 10)
    es_index_topic(topic.id)


@topic_delete_signal.connect
def on_topic_delete(app, topic=None):
    from services import topicService

    cache.delete_memoized(topicService.topic_by_id, topicService, topic.id)
    cache.delete_memoized(topicService.topic_ids_by_userid, topicService, topic.user_id)
    cache.delete_memoized(topicService.first_load_artifact_ids, topicService, topic.id, 10)
    es_delete_topic(topic.id)


@user_top_10_artifacts_signal.connect
def on_user_top_10_artifact_update(app, user_id=None):
    from services import userService

    cache.delete_memoized(userService.first_load_artifact_ids, userService, user_id, 10)


@artifact_comment_append_signal.connect
def on_user_comment_append(app, comment=None):
    from services import userService

    cache.delete_memoized(userService.user_comment_count, userService, comment.commenter_id)
    es_index_comment(comment)


@artifact_comment_remove_signal.connect
def on_user_comment_remove(app, comment=None):
    from services import userService

    cache.delete_memoized(userService.user_comment_count, userService, comment.commenter_id)
    es_delete_comment(comment)


@qiniu_unregister_key_signal.connect
def unregister_qiniu_key(app, qiniu_keys=None):
    from redis_tool import r, qiniu_temp_keys
    from qinius import key_from_url

    if qiniu_keys:
        r.zrem(qiniu_temp_keys, *[key_from_url(key_or_url) for key_or_url in qiniu_keys])


def es_index_user(user_id):
    from tasks import es_index_doc

    user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(user_id)
    setting_dict = user.pop("setting")
    if setting_dict is not None:
        user["description"] = setting_dict.get("description")
        user["lang"] = setting_dict.get("lang")
        user["tz"] = setting_dict.get("tz")
        user["comment_active"] = setting_dict.get("comment_active")

    user["confirmed_at"] = format_datetime(user.get("confirmed_at"))
    user["registered_at"] = format_datetime(user.get("registered_at"))
    user["suggest_field"] = {
        "input": gen_suggest(user.get("fullname")),
        "output": user.get("fullname"),
        "payload": {"id": user_id}
    }
    es_index_doc.delay("user", user_id, user)


def es_delete_user(user_id):
    from tasks import es_delete_doc

    es_delete_doc.delay("user", user_id)


def es_index_topic(topic_id):
    from tasks import es_index_doc

    topic = cache_registry.lookup("pinwall.artifacts.TopicService.topic_by_id")(topic_id)
    user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(topic["user_id"])
    del topic["artifact_count"]
    topic.get("terms", []).append(user.get("fullname"))
    topic["created_at"] = format_datetime(topic.get("created_at"))
    topic["suggest_field"] = {
        "input": gen_suggest(topic.get("name")),
        "output": topic.get("name"),
        "payload": {"id": topic_id}
    }
    es_index_doc.delay("topic", topic_id, topic)


def es_delete_topic(topic_id):
    from tasks import es_delete_doc

    es_delete_doc.delay("topic", topic_id)


def es_index_artifact(artifact_id):
    from tasks import es_index_doc

    artifact = cache_registry.lookup("pinwall.artifacts.ArtifactService.artifact_by_id")(artifact_id)

    user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(artifact["user_id"])
    del artifact["profile_image"]
    del artifact["comment_count"]
    del artifact["praise_count"]
    del artifact["assets"]
    artifact.get("terms", []).append(user.get("fullname"))
    artifact["created_at"] = format_datetime(artifact.get("created_at"))
    artifact["suggest_field"] = {
        "input": gen_suggest(artifact.get("name")),
        "output": artifact.get("name"),
        "payload": {"id": artifact_id}
    }
    es_index_doc.delay("artifact", artifact["id"], artifact,
                       parent_id=artifact.get("topic_id") if artifact.get("topic_id") else -1)


def es_delete_artifact(artifact_id):
    from tasks import es_delete_doc

    es_delete_doc.delay("artifact", artifact_id)


def es_index_comment(comment):
    from tasks import es_index_doc

    user = cache_registry.lookup("pinwall.users.UserService.user_by_id")(comment.commenter_id)
    artifact = cache_registry.lookup("pinwall.artifacts.ArtifactService.artifact_by_id")(comment.artifact_id)
    comment_doc = {"id": comment.id,
                   "user_id": comment.commenter_id,
                   "user_name": user.get("fullname"),
                   "content": comment.content,
                   "commented_at": format_datetime(comment.commented_at),
                   "artifact_id": artifact.get("id"),
                   "artifact_name": artifact.get("name")
    }
    es_index_doc.delay("comment", comment.id, comment_doc)


def es_delete_comment(comment):
    from tasks import es_delete_doc

    es_delete_doc.delay("comment", comment.id)


def gen_suggest(name):
    py_string_list = [s[0] for s in pypinyin.pinyin(name, style=pypinyin.STYLE_NORMAL)]
    py_normal = ''.join(py_string_list)
    if py_normal == name:
        return [name]
    else:
        return [name, py_normal]






