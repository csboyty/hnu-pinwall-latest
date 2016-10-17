# coding:utf-8

from flask import Blueprint, render_template, current_app, url_for, abort, request
from . import route, anonymous_route, roles_required, roles_accepted, anonymous_user_required, current_user
from ..services import topicService, artifactService


bp = Blueprint("dashboard", __name__, static_folder="static", static_url_path="")


@anonymous_route(bp, "/", methods=["GET"])
def index():
    return bp.send_static_file("index.html")


@anonymous_route(bp, "/projects", methods=["GET"], endpoint="projects")
@anonymous_route(bp, "/artifacts", methods=["GET"])
def artifacts():
    return bp.send_static_file("index.html")

@anonymous_route(bp, "/boxview", methods=["GET"], endpoint="boxview")
def show_boxview():
    return bp.send_static_file("showSlide/index.html")


@anonymous_route(bp, "/projects/<artifact_id>", methods=["GET"], endpoint="show_project")
@anonymous_route(bp, "/artifacts/<artifact_id>", methods=["GET"])
def show_artifact(artifact_id):
    if "micromessenger" in request.headers.get("User-Agent", "").lower(): 
        return bp.send_static_file("wechat_template/index.html")
    else:
        return bp.send_static_file("index.html")


@route(bp, "/projects/create", methods=["GET"], endpoint="create_project")
@route(bp, "/artifacts/create", methods=["GET"])
def create_artifact():
    return bp.send_static_file("index.html")


@route(bp, "/projects/<artifact_id>/update", methods=["GET"], endpoint="update_project")
@route(bp, "/artifacts/<artifact_id>/update", methods=["GET"])
def update_artifact(artifact_id):
    return bp.send_static_file("index.html")


@route(bp, "/topic/<topic_id>/project", methods=["GET"], endpoint="topic_append_project")
@route(bp, "/topic/<topic_id>/artifact", methods=["GET"])
def topic_append_artifact(topic_id):
    return bp.send_static_file("index.html")


@anonymous_route(bp, "/topics", methods=["GET"])
def topics():
    return bp.send_static_file("index.html")


@anonymous_route(bp, "/topics/<topic_id>", methods=["GET"])
def show_topic(topic_id):
    return bp.send_static_file("index.html")


@route(bp, "/topics/create", methods=["GET"])
# @roles_accepted("admin", "vip")
def create_topic():
    return bp.send_static_file("index.html")


@route(bp, "/topics/<topic_id>/update", methods=["GET"])
# @roles_accepted("admin", "vip")
def update_topic(topic_id):
    topic = topicService.get_or_404(topic_id)
    me = current_user._get_current_object()
    if me.has_role("admin") or me.id == topic.user_id:
        return bp.send_static_file("index.html")
    else:
        abort(403)


@anonymous_route(bp, "/search", methods=["GET"])
def search():
    return search_content(content=None)


@anonymous_route(bp, "/search/<content>", methods=["GET"])
def search_content(content=None):
    return bp.send_static_file("index.html")


@anonymous_route(bp, "/users/<user_id>", methods=["GET"])
def show_user(user_id):
    return bp.send_static_file("index.html")


@route(bp, "/users/<user_id>/topics", methods=["GET"])
def show_user_topics(user_id):
    return bp.send_static_file("index.html")


@route(bp, "/users/<user_id>/update", methods=["GET"])
def update_user(user_id):
    return bp.send_static_file("index.html")


@anonymous_route(bp, "/login", methods=["GET"])
@anonymous_user_required
def login():
    return bp.send_static_file("index.html")


@anonymous_route(bp, "/register", methods=["GET"])
@anonymous_user_required
def register():
    return bp.send_static_file("index.html")


@anonymous_route(bp, "/forget_password", methods=["GET"])
@anonymous_user_required
def forget_password():
    return bp.send_static_file("index.html")


@route(bp, "/change_password", methods=["GET"])
def change_password():
    return bp.send_static_file("index.html")


@route(bp, "/admin/users", methods=["GET"])
# @roles_required("admin")
def admin_users():
    return bp.send_static_file("index.html")


@route(bp, "/admin/projects", methods=["GET"], endpoint="admin_project")
# @route(bp, "/admin/artifacts", methods=["GET"])
def admin_artifact():
    return bp.send_static_file("index.html")


@route(bp, "/admin/comments", methods=["GET"])
# @roles_required("admin")
def admin_comments():
    return bp.send_static_file("index.html")



@anonymous_route(bp, "/index-artifact", methods=["GET"])
def index_artifacts():
    from ..models import Artifact
    from ..signals import es_index_artifact
    from ..core import db
    artifact_ids =Artifact.query.with_entities(Artifact.id).order_by(db.desc(Artifact.created_at)).all()
    for artifact_id in artifact_ids:
        es_index_artifact(artifact_id[0])

    return "ok"
