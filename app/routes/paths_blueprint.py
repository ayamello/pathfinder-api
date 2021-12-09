from flask import Blueprint
from app.controllers.paths_controller import create_path, delete_path


bp = Blueprint('bp_path', __name__, url_prefix='/paths')

bp.post('')(create_path)
bp.delete('/<int:id>')(delete_path)