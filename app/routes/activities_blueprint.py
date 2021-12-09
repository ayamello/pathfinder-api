from flask import Blueprint
from app.controllers.activities_controller import create_activity, delete_activity, update_activity

bp = Blueprint('bp_activities', __name__, url_prefix='/activities')

bp.post('')(create_activity)
bp.patch('/<int:id>')(update_activity)
bp.delete('/<int:id>')(delete_activity)
