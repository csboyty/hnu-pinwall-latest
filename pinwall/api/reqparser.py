# coding:utf-8

from flask import request, abort
from ..models import ArtifactAsset
from ..utils import parse_datetime


def parse_topic(req=None):
    if req is None:
        req = request
    data = req.json
    args = {}
    if "name" in data:
        args["name"] = data['name'].strip()
    else:
        abort(400)

    if "terms" in data:
        args["terms"] = map(lambda term: term.strip(), data["terms"])
    else:
        abort(400)

    if "description" in data:
        args["description"] = data["description"].strip()

    if "status" in data:
        args["status"] = data["status"]

    return args


def parse_artifact(req=None):
    if req is None:
        req = request
    data = req.json
    args = {}

    if "name" in data:
        args["name"] = data["name"].strip()
    else:
        abort(400)

    if "profile_image" in data:
        args["profile_image"] = data["profile_image"]
    else:
        abort(400)

    if "terms" in data:
        args["terms"] = map(lambda term: term.strip(), data["terms"])
    else:
        abort(400)

    if "assets" in data:
        assets = []
        for asset_dict in data["assets"]:
            if asset_dict.get('type') == '128':
                asset_dict.update(view_url=asset_dict.get('media_file'))

            assets.append(ArtifactAsset(**asset_dict))
        args["assets"] = assets
    else:
        abort(400)

    if "visible" in data:
        args["visible"] = data["visible"]

    if "description" in data:
        args["description"] = data["description"].strip()

    if "created_at" in data:
        args["created_at"] = parse_datetime(data["created_at"])

    return args









