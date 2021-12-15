from flask import Blueprint
from app.controllers.points_controller import create_point, points_by_path, update_point,delete_point
from app.routes.activities_blueprint import bp as bp_activities


bp = Blueprint('bp_point', __name__, url_prefix='/')

bp.post('/points')(create_point)
bp.get('/<int:path_id>/points')(points_by_path)
bp.patch('/points/<int:id>')(update_point)
bp.delete('/points/<int:id>')(delete_point)
bp.register_blueprint(bp_activities, url_prefix="/points")