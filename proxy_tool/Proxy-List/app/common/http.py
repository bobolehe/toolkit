from flask import jsonify


# 返回响应方法

def success_api(msg: str = "成功"):
    """ 成功响应 默认值“成功” """
    res = {
        'code': 0,
        'content': "",
        'message': msg,
    }
    return jsonify(res)


def fail_api():
    """ 失败响应 默认值“失败” """
    res = {
        'code': -2,
        'message': '/proxy/get:Retrieve a single proxy from the proxy pool; '
                   '/proxy/all:Retrieve all proxies from the proxy pool; '
                   '/success/get:Retrieve available proxies. '
                   '/success/all:Retrieve all available proxies. ',
    }
    return jsonify(res)


def err_api(msg: str = "失败"):
    """ 失败响应 默认值“失败” """
    res = {
        'code': -4,
        'content': "",
        'message': msg,
    }
    return jsonify(res)


def table_api(msg: str = "", data=None):
    """ 动态表格渲染响应 """
    res = {
        'message': msg,
        'code': 0,
        'content': data,
    }
    return jsonify(res)
