from flask import Flask
from app.routes.paths_blueprint import bp as bp_paths
from app.routes.user_blueprint import bp as bp_user

def init_app(app: Flask):
    app.register_blueprint(bp_paths)
    app.register_blueprint(bp_user)