from flask import Flask
from environs import Env
from app.configs import database, migrations, jwt
from app import routes
from flask_cors import CORS

env = Env()
env.read_env()


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = env("SECRET_KEY")
    app.config["JSON_SORT_KEYS"] = False

    
    database.init_app(app)
    migrations.init_app(app)
    jwt.init_app(app)
    routes.init_app(app)

    return app
