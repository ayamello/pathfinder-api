from flask import Blueprint
from app.controllers.user_controller import create, login

bp = Blueprint("bp", __name__)

bp.post("/signup")(create)
bp.post("/session")(login)
