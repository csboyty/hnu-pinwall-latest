# coding:utf-8

from flask import request, Blueprint
from ..qinius import upload_token, key_from_url
from ..redis_tool import register_qiniu_key
from . import *

bp = Blueprint("qiniu", __name__, url_prefix="/qiniu")


@route(bp, "/uptoken", methods=["GET"])
def get_upload_token():
    up_token = upload_token()
    return {"success": True, "uptoken": up_token}


@route(bp, "/add_key", methods=["PUT"])
def add_qiniu_key():
    key = request.json.get("key")
    qiniu_key = key_from_url(key)
    register_qiniu_key(qiniu_key)
    return {"success": True}


