import json
import random

from proxy_tool.app.common.http import success_api, fail_api, table_api
from proxy_tool.app.extensions import redis_store
from flask import Blueprint, request
from proxy_tool.check_proxy.check_proxy import run_check
from proxy_tool.app.extensions import scheduled, apscheduler_task

proxy_bp = Blueprint('proxy', __name__, url_prefix='/')


@proxy_bp.route('/')
def index():
    return fail_api()


# 获取初级代理需要自行验证
@proxy_bp.route('/success/<id>', methods=["GET"])
def success(id):
    # redis中读取
    proxy_list = redis_store.hgetall("primary_proxy")
    data_list = []
    for d in proxy_list:
        temp = json.loads(redis_store.hget("primary_proxy", d).decode('utf-8'))
        data_list.append(temp)

    if id == "get":
        msg = random.choice(data_list)
        return success_api(msg=msg)
    elif id == "all":
        msg = data_list
        return table_api(data=msg)
    else:
        return fail_api()


@proxy_bp.route('/verify/', methods=["GET"])
def proxy():
    url = request.args.get('url')
    if url:
        # redis中读取
        apscheduler_task.assignments(scheduled, run_check(url))
        msg = "已提交验证，稍后进行获取即可"
        return success_api(msg=msg)
    else:
        msg = '需要携带url参数进行校验'
        return success_api(msg=msg)
