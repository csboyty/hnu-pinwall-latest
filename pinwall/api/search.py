# coding:utf-8

from flask import request, Blueprint
from . import *
from ..resultproxy import ArtifactResultProxy
from ..es import es_client

bp = Blueprint("search", __name__, url_prefix="/search")


@anonymous_route(bp, "/text_like", methods=["GET"])
def text_like_this():
    text = request.args.get("text", None)
    if text:
        items = es_client.get_suggestion(text)
    else:
        items = []
    return {"success": True, "items": items}


@anonymous_route(bp, "/", methods=["GET"])
def search_artifact():
    q = request.args.get("q", None)
    if q:
        q = q.lower()
    offset = int(request.args.get("offset", "0"))
    size = int(request.args.get("count", '10'))
    total, artifact_ids = es_client.search_artifact(q, start=offset, size=size)
    artifact_list = []
    if artifact_ids:
        for artifact_id in artifact_ids:
            artifact = ArtifactResultProxy(artifact_id).result()
            artifact_list.append(artifact)

    return {"success": True, "artifacts": artifact_list}







