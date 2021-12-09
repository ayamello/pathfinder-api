from flask import Blueprint
from app.controllers.points_controller import create_point, update_point,delete_point, activities_by_point


bp = Blueprint('bp_point', __name__, url_prefix='/points')

bp.post('')(create_point)
bp.get('/<int:id>')(activities_by_point)
bp.patch('/<int:id>')(update_point)
bp.delete('/<int:id>')(delete_point)
