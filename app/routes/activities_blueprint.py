from flask import Blueprint
from app.controllers.activities_controller import create_activity, delete_activity, update_activity, activities_by_point

bp = Blueprint('bp_activities', __name__)

bp.post('/activities')(create_activity)
bp.get('/<int:path_id>/activities')(activities_by_point)
bp.patch('/activities/<int:id>')(update_activity)
bp.delete('/activities/<int:id>')(delete_activity)
