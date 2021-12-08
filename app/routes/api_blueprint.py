from flask import Blueprint
from app.routes.activities_blueprint import bp as bp_activities

bp = Blueprint("bp_api", __name__, url_prefix="/api")

bp.register_blueprint(bp_activities)
