from flask import Blueprint
from app.controllers.subscribers_controller import create_subscriber

bp = Blueprint('bp_subscribers', __name__,)

bp.post('/subscribers')(create_subscriber)
