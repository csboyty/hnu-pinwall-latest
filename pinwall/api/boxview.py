# coding:utf-8

from flask import request, Blueprint
from ..core import db
from ..models import BoxViewFile
from ..utils import utc_to_localtime
from ..tasks import gen_boxview_session_url

bp = Blueprint("boxview", __name__, url_prefix="/boxview")


@bp.route("/webhook", methods=["POST", "GET"])
def webhook_success():
    """
    [
        {
        "type": "document.done",
        "data": {
        "id": "4cca28f1159c4f368193d5014fabc16e"
        },
        "triggered_at": "2014-01-30T20:33:04.798Z"
        },
        {
        "type": "document.error",
        "data": {
        "id": "4cca27e4159c4f368193d5014fabc16e"
        },
        "triggered_at": "2014-01-30T20:33:04.798Z"
        }
    ]
    """

    return {"success":True}
