from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    Migrate(app, app.db)

    from app.models.users_model import UserModel
    from app.models.paths_model import PathModel
    from app.models.users_paths_table import users_paths
    from app.models.adresses_model import AdressModel
    from app.models.points_model import PointModel
    from app.models.points_paths_table import points_paths
    from app.models.adresses_model import AdressModel

    