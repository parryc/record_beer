from database import db
from flask import Flask


def create_app(name=__name__):
    app = Flask(name)
    app.config.from_object("config.DevelopmentConfig")
    # https://help.pythonanywhere.com/pages/UsingSQLAlchemywithMySQL#configuring-sqlalchemy
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 280}
    db.init_app(app)
    return app
