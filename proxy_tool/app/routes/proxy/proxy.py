"""
获取代理接口
"""

import json
import random

from proxy_tool.app.common.rights import authorize
from proxy_tool.app.common.http import success_api, fail_api, table_api, err_api
from proxy_tool.app.extensions import redis_store
from flask import Blueprint, request
from proxy_tool.check_proxy.check_proxy import run_check
from task_tool import apscheduler_task
from task_tool.apscheduler_task import scheduler

proxy_bp = Blueprint('proxy', __name__, url_prefix='/proxy')


@proxy_bp.route('/')
@authorize()
def index():
    return fail_api()


# 获取初级代理需要自行验证
@proxy_bp.route('/<way>', methods=["GET"])
@authorize()
def success(way):
    """
    获取一级代理
    :param way: 获取方式 all/get
    :return:
    """
    if not way:
        return err_api(msg='请求失败，请检查必需参数')

    # redis中读取
    proxy_list = redis_store.hgetall("primary_proxy")
    data_list = []
    for d in proxy_list:
        temp = json.loads(redis_store.hget("primary_proxy", d).decode('utf-8'))
        data_list.append(temp)
    if way == "get":
        msg = random.choice(data_list)
        return success_api(msg=msg)
    elif way == "all":
        msg = data_list
        return table_api(data=msg)
    else:
        return fail_api()


@proxy_bp.route('/verify/', methods=["GET"])
@authorize()
def proxy():
    url = request.args.get('url')
    if url:
        # redis中读取
        job, event = apscheduler_task.assignments(scheduler, run_check, parameters=[url])
        msg = f"已提交验证，稍后进行获取即可通过id{job.id}id可查询任务状态"
        return table_api(msg=msg, data=event)
    else:
        msg = '需要携带url参数进行校验'
        return success_api(msg=msg)


@proxy_bp.route('/verify_task/', methods=["GET"])
@authorize()
def verify_task():
    jod_id = request.args.get('id')
    if not jod_id:
        return err_api(msg='请求失败，请检查必需参数')
    task = scheduler.get_job(jod_id)
    if task:
        msg = '需要携带url参数进行校验'
        return success_api(msg=msg)
    else:
        return success_api(msg="无法查询到此id任务")


@proxy_bp.route('/confirm/<way>/', methods=["GET"])
@authorize()
def confirm(way):
    url = request.args.get('url')
    if not url:
        return err_api(msg='请求失败，请检查必需参数')
    proxy_list = redis_store.hgetall(url)
    data_list = []
    for d in proxy_list:
        temp = json.loads(redis_store.hget(url, d).decode('utf-8'))
        data_list.append(temp)

    if not data_list:
        return err_api(msg=f"{url}无测试代理")
    if way == 'all':
        msg = f'指定url测试可用代理列表,数量{len(data_list)}'
        return table_api(msg=msg, data=data_list)
    elif way == 'get':
        d = random.choice(data_list)
        data_list = [d]
        msg = '指定url测试可用代理'
        return table_api(msg=msg, data=data_list)
    else:
        return err_api(msg='请求失败，请检查必需参数')
