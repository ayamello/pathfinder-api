from flask import Blueprint
from app.controllers.activities_controller import create, read_all, update, delete

bp = Blueprint('bp_activities', __name__, url_prefix='/activities')

bp.post('')(create)
bp.get("")(read_all)
bp.patch("/<int:id>")(update)
bp.delete("/<int:id>")(delete)
