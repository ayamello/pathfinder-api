from flask import Blueprint
from app.controllers.users_controller import create_user, delete_user, get_all_users, login, get_by_id, update_user

bp = Blueprint('bp', __name__)

bp.post('/signup')(create_user)
bp.post('/login')(login)
bp.get('/users')(get_all_users)
bp.get('/users/<int:id>')(get_by_id)
bp.patch('/users/<int:id>')(update_user)
bp.delete('/users/<int:id>')(delete_user)
