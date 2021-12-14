from flask import Flask
from app.routes.paths_blueprint import bp as bp_paths
from app.routes.user_blueprint import bp as bp_user
from app.routes.points_blueprint import bp as bp_points

def init_app(app: Flask):
    app.register_blueprint(bp_paths)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_points)
