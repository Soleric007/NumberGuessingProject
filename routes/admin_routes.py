from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Game

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

# 🛑 Admin Access Check
def admin_required():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        return jsonify({"error": "Admin access required"}), 403  

    return current_user  

# 🏠 Admin Dashboard
@admin_bp.route('/')
@jwt_required()
def admin_dashboard():
    admin_check = admin_required()
    if isinstance(admin_check, tuple):
        return admin_check  

    return render_template('admin/admin.html')

# 👥 Get All Users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    admin_check = admin_required()
    if isinstance(admin_check, tuple):
        return admin_check  

    users = User.query.all()
    user_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "games_played": user.games_played,
            "best_score": user.best_score,
            "is_admin": user.is_admin
        }
        for user in users
    ]
    return jsonify(user_data), 200

# 🎮 Get All Games (Admins Only)
@admin_bp.route('/games', methods=['GET'])
@jwt_required()
def get_all_games():
    admin_check = admin_required()
    if isinstance(admin_check, tuple):
        return admin_check  

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

# ⭐ Promote User to Admin
@admin_bp.route('/promote/<int:user_id>', methods=['PATCH'])
@jwt_required()
def promote_user(user_id):
    admin_check = admin_required()
    if isinstance(admin_check, tuple):
        return admin_check  

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.is_admin:
        return jsonify({"message": f"User {user.username} is already an admin"}), 400

    user.is_admin = True
    db.session.commit()
    return jsonify({"message": f"User {user.username} is now an admin"}), 200

# ❌ Delete User (Admins Only)
@admin_bp.route('/delete-user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    admin_check = admin_required()
    if isinstance(admin_check, tuple):
        return admin_check  

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.id == get_jwt_identity():  
        return jsonify({"error": "Admins cannot delete themselves"}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user.username} deleted successfully"}), 200

# 🗑️ Delete Game (Admins Only)
@admin_bp.route('/delete-game/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    admin_check = admin_required()
    if isinstance(admin_check, tuple):
        return admin_check  

    game = Game.query.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    db.session.delete(game)
    db.session.commit()
    return jsonify({"message": f"Game {game_id} deleted successfully"}), 200
