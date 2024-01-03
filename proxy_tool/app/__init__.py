import os
from flask import Flask

from .routes import init_view
from .extensions import init_plugs
from .config import BaseConfig
from .common.http import fail_api


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    # 定义处理 404 错误的函数
    @app.errorhandler(404)
    def handle_not_found_error(e):
        return fail_api()

    # 引入数据库配置
    app.config.from_object(BaseConfig)

    # 注册插件
    init_plugs(app)
    # 注册路由
    init_view(app)

    return app
