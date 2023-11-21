"""
密钥验证
"""
from functools import wraps
from flask import request
from ...app.common.http import err_api
from ...app.config import BaseConfig


def authorize(power: bool = BaseConfig.RIGHTS):
    def jwt_required_with_redirect(f):
        # 校验是否携带jwt
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                key = request.args.get(BaseConfig.RIGHTS_GET)
            except Exception as e:
                return err_api(msg='权限不足')
            # 不需要验证权限，返回用户通过
            if not power:
                return f(*args, **kwargs)
            if not key:
                return err_api(msg='权限不足')
            if key == BaseConfig.RIGHTS_KEY:
                return f(*args, **kwargs)
            return err_api(msg='权限不足')

        return decorated_function

    return jwt_required_with_redirect
