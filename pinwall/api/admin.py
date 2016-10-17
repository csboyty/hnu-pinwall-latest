# coding:utf-8

from flask import request, Blueprint
from . import *
from ..resultproxy import UserResultProxy, ResultProxyList, CommentResultProxy, ArtifactResultProxy
from ..angulars import ng_table_parameter
from ..models import ArtifactComment
from ..es import es_client


bp = Blueprint("admin", __name__, url_prefix="/admin")


@route(bp, "/users/", methods=["GET"])
@roles_required("admin")
def manage_user():
    """
        type: user_name
        args like {'filter': {'type': u'username', 'keyword': u'ty'}, 'count': u'10', 'page': u'1'}
        {'filter': {}, 'count': u'10', 'page': u'1'}
    """

    args = ng_table_parameter(request)
    keyword = args["filter"].get("keyword", "")
    if keyword:
        keyword=keyword.lower()
    size = int(args.get("count", "10"))
    offset = (int(args.get("page", "1")) - 1) * size
    total, user_ids = es_client.search_user(keyword, start=offset, size=size)
    users = ResultProxyList()
    for user_id in user_ids:
        users.append(UserResultProxy(user_id))

    return {"success": True, "users": users, "total": total}


@route(bp, "/comments/", methods=["GET"])
@roles_required("admin")
def manage_comment():
    """
       type: user_name;artifact_name,comment_content
       args like {'filter': {'type': u'13', 'keyword': u'ty'}, 'count': u'10', 'page': u'1'}
       {'filter': {}, 'count': u'10', 'page': u'1'}
   """
    args = ng_table_parameter(request)
    user_name = args["filter"].get("keyword") if args["filter"].get("type") == "user_name" else None
    artifact_name = args["filter"].get("keyword") if args["filter"].get("type") == "artifact_name" else None
    comment_content = args["filter"].get("keyword") if args["filter"].get("type") == "comment_content" else None

    size = int(args.get("count", "10"))
    offset = (int(args.get("page", "1")) - 1) * size

    total, comment_ids = es_client.search_comment(user_name, artifact_name, comment_content, start=offset, size=size)
    comments = []
    comment_list = []
    if comment_ids:
        comments = ArtifactComment.query.filter(ArtifactComment.id.in_(comment_ids)).all()

    if comments:
        comment_list = ResultProxyList()
        for comment in comments:
            comment_list.append(CommentResultProxy(comment, show_artifact=True))
    return {"success": True, "comments": comment_list, "total": total}


@route(bp, "/artifacts/", methods=["GET"])
@roles_required("admin")
def manage_artifact():
    """
       type: artifact_name;artifact_term
       args like {'filter': {'type': u'13', 'keyword': u'ty'}, 'count': u'10', 'page': u'1'}
       {'filter': {}, 'count': u'10', 'page': u'1'}
   """
    args = ng_table_parameter(request)
    artifact_name = args["filter"].get("keyword", "") if args["filter"].get("type") == "artifact_name" else None
    if artifact_name:
        artifact_name = artifact_name.lower()
    artifact_term = args["filter"].get("keyword", "") if args["filter"].get("type") == "artifact_term" else None
    if artifact_term:
        artifact_term = artifact_term.lower()
    size = int(args.get("count", "10"))
    offset = (int(args.get("page", "1")) - 1) * size
    total, artifact_ids = es_client.search_artifact_by(artifact_name=artifact_name, term=artifact_term,
                                                             start=offset, size=size)
    artifact_list = []
    if artifact_ids:
        for artifact_id in artifact_ids:
            artifact = ArtifactResultProxy(artifact_id).result()
            artifact_list.append(artifact)
    return {"success": True, "artifacts": artifact_list, "total": total}
