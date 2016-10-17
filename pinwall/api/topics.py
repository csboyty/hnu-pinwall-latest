# coding:utf-8

from flask import request, Blueprint, abort
from . import *
from .reqparser import parse_topic, parse_artifact
from ..services import topicService
from ..models import Topic, Artifact, ArtifactAsset
from ..resultproxy import TopicResultProxy, ArtifactResultProxy
from ..es import es_client

bp = Blueprint("topics", __name__, url_prefix="/topics")


@anonymous_route(bp, "/", methods=["GET"])
def list_topic():
    scope = request.args.get('scope', None)
    keyword = request.args.get('keyword', None)
    size = int(request.args.get("count", '10'))
    offset = (int(request.args.get("page", "1")) - 1) * size

    # filter_conditions = []
    # if scope == 'me' and current_user.is_authenticated():
    # filter_conditions.append(Topic.user_id == current_user._get_current_object().id)
    # elif scope == 'open':
    # filter_conditions.append(Topic.status == 0)
    # elif scope == 'closed':
    # filter_conditions.append(Topic.status == 1)
    #
    # if keyword:
    # filter_conditions.append(Topic.name.startswith(keyword))
    #
    # topic_ids = topicService.list_topic_id(last_topic_id, page_size, *filter_conditions)
    user_id = None
    status = -1
    if scope == 'me' and current_user.is_authenticated():
        user_id = current_user._get_current_object().id
    elif scope == 'open':
        status = 0
    elif scope == 'closed':
        status = 1

    total, topic_ids = es_client.search_topic(keyword, user_id=user_id, status=status, start=offset,
                                              size=size)

    topic_list = []
    if topic_ids:
        for topic_id in topic_ids:
            topic = TopicResultProxy(topic_id).result()
            topic_list.append(topic)
    return {"success": True, "topics": topic_list}


@route(bp, "/", methods=["PUT"])
# @roles_accepted("admin", "vip")
def create_topic():
    user_id = current_user._get_current_object().id
    print request.json
    args = parse_topic(request)
    topicService.create_topic(user_id=user_id, **args)
    return {"success": True}


@anonymous_route(bp, "/<int:topic_id>", methods=["GET"])
def show_topic(topic_id):
    result = {"success": True}
    result.update(TopicResultProxy(topic_id).result())
    return result


@route(bp, "/<int:topic_id>", methods=["POST"])
# @roles_accepted("admin", "vip")
def update_topic(topic_id):
    topic = topicService.get_or_404(topic_id)
    me = current_user._get_current_object()
    if me.has_role("admin") or me.id == topic.user_id:
        args = parse_topic(request)
        topicService.update_topic(topic, **args)
        return {"success": True}
    else:
        abort(403)


@route(bp, "/<int:topic_id>/change_status", methods=["POST"])
# @roles_accepted("admin", "vip")
def change_topic_status(topic_id):
    topic = topicService.get_or_404(topic_id)
    status = int(request.json.get("status", '0'))
    me = current_user._get_current_object()
    if me.has_role("admin") or me.id == topic.user_id:
        topicService.update_topic(topic, status=status)
        return {"success": True}
    else:
        abort(403)


@route(bp, "/<int:topic_id>", methods=["DELETE"])
# @roles_accepted("admin", "vip")
def delete_topic(topic_id):
    topic = topicService.get_or_404(topic_id)
    me = current_user._get_current_object()
    if me.has_role("admin") or me.id == topic.user_id:
        topicService.delete_topic(topic)
        return {"success": True}
    else:
        abort(403)


@anonymous_route(bp, "/<int:topic_id>/artifacts", methods=["GET"])
def list_topic_artifacts(topic_id):
    last_artifact_id = int(request.args.get("last_id", '0'))
    page_size = int(request.args.get("count", '10'))
    artifact_ids = topicService.list_artifact_id(topic_id, last_artifact_id, page_size)
    artifact_list = []
    if artifact_ids:
        for artifact_id in artifact_ids:
            artifact = ArtifactResultProxy(artifact_id, show_topic=False).result()
            artifact_list.append(artifact)

    return {"success": True, "artifacts": artifact_list}


@route(bp, "/<int:topic_id>/artifacts/append", methods=["PUT"])
def append_topic_artifact(topic_id):
    topic = topicService.get_or_404(topic_id)
    if topic.status == 1:
        raise PinwallError(msg="The topic is closed.", code="TOPIC_CLOSED")
    args = parse_artifact(request)
    user_id = current_user._get_current_object().id
    artifact = Artifact(user_id=user_id, **args)
    topicService.append_artifact(topic, artifact)
    return {"success": True}


@route(bp, "/<int:topic_id>/artifacts/remove", methods=["DELETE"])
@roles_accepted("admin", "vip")
def remove_topic_artifact(topic_id):
    me = current_user._get_current_object()
    artifact_id = request.form.get("artifact_id", None)
    topic = topicService.get_or_404(topic_id)
    if me.has_role("admin") or me.id == topic.user_id:
        topicService.remove_artifact(topic, artifact_id)
        return {"success": True}
    else:
        abort(403)




