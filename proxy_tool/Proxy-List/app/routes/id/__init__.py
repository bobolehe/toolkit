from flask import Flask
from app.routes.id.get import ID


def register_id_views(app: Flask):
    app.register_blueprint(ID)