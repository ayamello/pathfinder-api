from flask import Blueprint
from app.controllers.user_controller import create_user, get_all_users, login, get_by_username

bp = Blueprint("bp", __name__)

bp.post("/signup")(create_user)
bp.post("/session")(login)
bp.get("/users")(get_all_users)
bp.get("/user/<int:id>")(get_by_username)

