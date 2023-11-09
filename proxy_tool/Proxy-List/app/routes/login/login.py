import json
import random

from app.common.http import success_api, fail_api
from app.extensions import redis_store
from flask import Blueprint

login_bp = Blueprint('proxy', __name__, url_prefix='/')


@login_bp.route('/')
def index():
    return fail_api()


@login_bp.route('/success/<id>', methods=["GET"])
def success(id):
    # redis中读取
    proxy_list = json.loads(redis_store.get("success_proxy"))
    proxy_list = proxy_list['success']

    if id == "get":
        msg = random.choice(proxy_list)
        return success_api(msg=msg)
    elif id == "all":
        msg = proxy_list
        return success_api(msg=msg)
    else:
        return fail_api()


@login_bp.route('/proxy/<id>', methods=["GET"])
def proxy(id):
    # redis中读取
    proxy_list = json.loads(redis_store.get("proxy_list"))
    proxy_list = proxy_list['success']

    if id == "get":
        msg = random.choice(proxy_list)
        return success_api(msg=msg)
    elif id == "all":
        msg = proxy_list
        return success_api(msg=msg)
    else:
        return fail_api()
