from flask import Blueprint
from app.routes.activities_blueprint import bp as bp_activities
from app.routes.user_blueprint import bp as bp_user

bp = Blueprint("bp_api", __name__, url_prefix="/api")

bp.register_blueprint(bp_activities)
bp.register_blueprint(bp_user)

