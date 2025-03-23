from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import db, User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    user_data = [
        {
            "id": user.id,
            "username": user.username,
            "games_played": user.games_played,
            "best_score": user.best_score
        }
        for user in users
    ]
    return jsonify(user_data), 200
