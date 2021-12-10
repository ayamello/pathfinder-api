from flask import Blueprint
from app.routes.points_blueprint import bp as bp_points
from app.routes.subscribers_blueprint import bp as bp_subscribers
from app.controllers.paths_controller import create_path, delete_path, read_all


bp = Blueprint('bp_path', __name__, url_prefix='/paths')

bp.post('')(create_path)
bp.delete('/<int:id>')(delete_path)
bp.get('')(read_all)
bp.register_blueprint(bp_points)
bp.register_blueprint(bp_subscribers)