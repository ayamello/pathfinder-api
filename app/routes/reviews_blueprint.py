from flask import Blueprint
from app.controllers.reviews_controller import create_review, delete_review, update_review, reviews_by_activity

bp = Blueprint('bp_reviews', __name__)

bp.post('/reviews')(create_review)
bp.get('/<int:activity_id>/reviews')(reviews_by_activity)
bp.patch('/reviews/<int:id>')(update_review)
bp.delete('/reviews/<int:id>')(delete_review)
