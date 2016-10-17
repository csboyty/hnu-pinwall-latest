# coding:utf-8

from flask import request


def ng_table_parameter(req=None, filter_prefix="filter"):
    if req is None:
        req = request
    args = req.args
    parameter = {'filter': {}}

    for key in args.iterkeys():
        value = args.getlist(key)
        value = value[0] if len(value) == 1 else value
        if key.startswith(filter_prefix):
            parameter['filter'].setdefault(key[len(filter_prefix) + 1:-1], value)
        else:
            parameter.setdefault(key, value)
    return parameter
