# coding:utf-8

from flask import request, Blueprint
from . import *
from ..services import userService, artifactService, topicService
from ..models import User, UserSetting
from ..resultproxy import UserResultProxy, TopicResultProxy, ArtifactResultProxy

bp = Blueprint("users", __name__, url_prefix="/users")


@anonymous_route(bp, '/whoami', methods=["GET"])
def whoami():
    user_id = None
    if current_user.is_authenticated():
        me = current_user._get_current_object()
        user_id = me.id
    user = UserResultProxy(user_id).result() if user_id else {}
    return {"success": True, "user": user.get("user")}


@route(bp, "/", methods=["GET"])
def list_user():
    pass


@anonymous_route(bp, "/<int:user_id>")
def show_user(user_id):
    user = UserResultProxy(user_id, load_top_10_artifacts=True).result()
    result = {"success": True}
    result.update(user)
    return result


@route(bp, "/<int:user_id>/role", methods=["POST"])
# @roles_required("admin")
def update_user_role(user_id):
    role = request.json.get("role")
    me = current_user._get_current_object()
    if me.id != user_id:
        userService.change_user_role_by_id(user_id, [role])
        return {"success": True}
    else:
        return {"success": False}


@route(bp, "/<int:user_id>/setting", methods=["POST"])
def update_user_setting(user_id):
    me = current_user._get_current_object()
    if me.has_role("admin") or me.id == user_id:
        setting_dict = request.json
        if me.id == user_id:
            if "comment_active" in setting_dict: setting_dict.pop('comment_active')

        user_setting = UserSetting(**setting_dict)
        user_setting.user_id = user_id
        userService.update_user(user_id, setting=user_setting)
        return {"success": True}
    else:
        abort(403)


@route(bp, "/<int:user_id>", methods=["DELETE"])
@roles_required("admin")
def delete_user(user_id):
    me = current_user._get_current_object()
    if me.id != user_id:
        userService.delete_user_by_id(user_id)
        return {"success": True}


@anonymous_route(bp, "/<int:user_id>/topics", methods=["GET"])
def list_user_topics(user_id):
    topic_ids = topicService.topic_ids_by_userid(user_id)
    topic_list = []
    if topic_ids:
        for topic_id in topic_ids:
            topic = TopicResultProxy(topic_id).result()
            topic_list.append(topic)

    return {"success": True, "topics": topic_list}


@anonymous_route(bp, "/<int:user_id>/artifacts", methods=["GET"])
def list_user_artifacts(user_id):
    last_artifact_id = int(request.args.get("last_id", '0'))
    page_size = int(request.args.get("count", '10'))
    _show_user = bool(int(request.args.get("show_user", 0)))
    user_artifacts = artifactService.artifact_by_userid(user_id)
    artifact_ids = user_artifacts.get("artifact_ids")
    contains = last_artifact_id in artifact_ids
    if last_artifact_id and contains:
        pos = artifact_ids.index(last_artifact_id) + 1
        part_artifacts_ids = artifact_ids[pos:pos + page_size]
    else:
        part_artifacts_ids = artifact_ids[0:page_size]

    artifact_list = []
    if part_artifacts_ids:
        for artifact_id in part_artifacts_ids:
            artifact = ArtifactResultProxy(artifact_id, _show_user).result()
            artifact_list.append(artifact)

    return {"success": True, "artifacts": artifact_list}

















