from flask import Blueprint
from app.controllers.activities_controller import create, update, delete

bp = Blueprint('bp_activities', __name__, url_prefix='/activities')

bp.post('')(create)
bp.patch('/<int:id>')(update)
bp.delete('/<int:id>')(delete)
