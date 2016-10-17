# coding:utf-8

from flask import request, Blueprint
from . import *
from .reqparser import parse_artifact
from ..models import Artifact, ArtifactAsset, ArtifactComment, ArtifactScore
from ..resultproxy import ArtifactResultProxy, ResultProxyList, CommentResultProxy
from ..services import artifactService, topicService
from ..es import es_client

bp = Blueprint("artifacts", __name__, url_prefix="/artifacts")


@anonymous_route(bp, "/", methods=["GET"])
def list_firstpage_artifact():
    size = int(request.args.get("count", "10"))
    offset = (int(request.args.get("page", "1")) - 1) * size
    total, artifact_ids = es_client.list_firstpage_artifact(start=offset, size=size)
    artifact_list = []
    if artifact_ids:
        for artifact_id in artifact_ids:
            artifact = ArtifactResultProxy(artifact_id).result()
            artifact_list.append(artifact)

    return {"success": True, "artifacts": artifact_list}


@route(bp, "/", methods=["PUT"])
def create_artifact():
    user_id = current_user._get_current_object().id
    args = parse_artifact(request)
    artifactService.create_artifact(user_id=user_id, **args)
    return {"success": True}


@anonymous_route(bp, "/<int:artifact_id>", methods=["GET"])
def show_artifact(artifact_id):
    artifact = ArtifactResultProxy(artifact_id).result()
    praised = False
    if current_user.is_authenticated():
        me = current_user._get_current_object()
        praised = artifactService.artifact_praised_by_userid(artifact_id, me.id)
    artifact["success"] = True
    artifact["praised"] = True if praised else False
    return artifact


@route(bp, "/<int:artifact_id>", methods=["POST"])
def update_artifact(artifact_id):
    artifact = artifactService.get_or_404(artifact_id)
    me = current_user._get_current_object()
    topic = None
    if artifact.topic_id is not None:
        topic = topicService.get_or_404(artifact.topic_id)

    if me.has_role("admin") or (
                    me.id == artifact.user_id and (topic is None or (topic is not None and topic.status == 0))):
        args = parse_artifact(request)
        artifactService.update_artifact(artifact, **args)
        return {"success": True}
    elif me.id == artifact.user_id and topic is not None and topic.status == 1:
        raise PinwallError(msg="The topic is closed.", code="TOPIC_CLOSED")
    else:
        abort(403)


@route(bp, "/<int:artifact_id>/visible/toggle", methods=["POST"])
@roles_required("admin")
def change_artifact_visible(artifact_id):
    artifact = artifactService.get_or_404(artifact_id)
    artifactService.update_artifact(artifact, post_update=False, visible=not artifact.visible)
    return {"success": True}


@route(bp, "/<int:artifact_id>", methods=["DELETE"])
def delete_artifact(artifact_id):
    artifact = artifactService.get_or_404(artifact_id)
    me = current_user._get_current_object()
    topic = None
    if artifact.topic_id is not None:
        topic = topicService.get_or_404(artifact.topic_id)

    if me.has_role("admin") or (
                    me.id == artifact.user_id and (topic is None or (topic is not None and topic.status == 0))):
        artifactService.delete_artifact(artifact)
        return {"success": True}
    elif me.id == artifact.user_id and topic is not None and topic.status == 1:
        raise PinwallError(msg="The topic is closed.", code="TOPIC_CLOSED")
    else:
        abort(403)


@anonymous_route(bp, "/<int:artifact_id>/comments", methods=["GET"])
def artifact_comments(artifact_id):
    comments = ArtifactComment.query.filter(ArtifactComment.artifact_id == artifact_id,
                                            ArtifactComment.visible == True).order_by(
        db.asc(ArtifactComment.commented_at)).all()
    comment_list = []
    if comments:
        comment_list = ResultProxyList()
        for comment in comments:
            comment_list.append(CommentResultProxy(comment))
    return {"success": True, "comments": comment_list}


@route(bp, "/<int:artifact_id>/comments/append", methods=["PUT"])
def append_artifact_comment(artifact_id):
    me = current_user._get_current_object()
    if me.setting.comment_active:
        content = request.json.get("content")
        artifact_comment = ArtifactComment(artifact_id=artifact_id, commenter_id=me.id, content=content)
        artifactService.append_comment(artifact_id, artifact_comment)
        return {"success": True, "comment_id": artifact_comment.id}
    else:
        raise PinwallError(msg="The user comment disable", code="COMMENT_DISABLE")


@route(bp, "/<int:artifact_id>/comments/<int:comment_id>/remove", methods=["DELETE"])
def remove_artifact_comment(artifact_id, comment_id):
    me = current_user._get_current_object()
    artifact_comment = ArtifactComment.query.get_or_404(comment_id)
    if me.has_role("admin") or me.id == artifact_comment.commenter_id:
        artifactService.remove_comment(artifact_id, artifact_comment)
        return {"success": True}
    else:
        abort(403)


@route(bp, "/<int:artifact_id>/scores/toggle", methods=["POST"])
def toggle_artifact_score(artifact_id):
    me = current_user._get_current_object()
    artifact_score = ArtifactScore.query.filter(ArtifactScore.artifact_id == artifact_id,
                                                ArtifactScore.scorer_id == me.id).first()

    if artifact_score is None:

        score = 1 if me.has_role("vip") else 0
        artifact_score = ArtifactScore(artifact_id=artifact_id, scorer_id=me.id, score=score)
        artifactService.append_score(artifact_id, artifact_score)
    else:
        artifactService.remove_score(artifact_id, artifact_score)
    return {"success": True}










