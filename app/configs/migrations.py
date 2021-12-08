from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    Migrate(app, app.db)

    from app.models.users_model import UserModel
    from app.models.paths_model import PathModel
    from app.models.subscribers_model import SubscriberModel
    from app.models.addresses_model import AddressModel
    from app.models.points_model import PointModel
    from app.models.points_paths_table import points_paths
    from app.models.activities_model import ActivityModel

    