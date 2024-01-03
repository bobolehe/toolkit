from flask import Flask
from .proxy import proxy_bp


def register_proxy_views(app: Flask):
    app.register_blueprint(proxy_bp)
