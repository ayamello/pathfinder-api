from flask import Blueprint
from app.controllers.points_controller import create_point, update_point,delete_point, list_all_points, all_point_activities


bp = Blueprint('bp_point', __name__, url_prefix='/point')

bp.post('')(create_point)
bp.get('')(list_all_points)
bp.get('/<int:id>')(all_point_activities)
bp.patch('/<int:id>')(update_point)
bp.delete('/<int:id>')(delete_point)
