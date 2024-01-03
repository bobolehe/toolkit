from flask import Flask
from .get import ID


def register_id_views(app: Flask):
    app.register_blueprint(ID)
