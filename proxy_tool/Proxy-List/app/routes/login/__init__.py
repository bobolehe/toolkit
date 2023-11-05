from flask import Flask
from app.routes.login.login import login_bp


def register_login_views(app: Flask):
    app.register_blueprint(login_bp)
