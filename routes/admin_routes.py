from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import db, User, Game

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


@admin_bp.route('/delete-user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@admin_bp.route('/games', methods=['GET'])
@jwt_required()
def get_all_games():
    games = Game.query.all()
    game_data = [
        {
            "id": game.id,
            "user_id": game.user_id,
            "status": game.status,
            "attempts": game.attempts
        }
        for game in games
    ]
    return jsonify(game_data), 200
