# from flask import Blueprint

# # Create the Blueprint
# user_bp = Blueprint("user", __name__)

# @user_bp.route("/test", methods=["GET"])
# def test():
#     return "User route is working!"

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

# Create the Blueprint
user_bp = Blueprint("user", __name__)

# ✅ Test route (Keep it for now)
@user_bp.route("/test", methods=["GET"])
def test():
    return "User route is working!"

# 🔍 Get User Profile
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "games_played": user.games_played,
        "best_score": user.best_score,
        "is_admin": user.is_admin
    }), 200

# ✏️ Update User Info
@user_bp.route("/update-profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

# ❌ Delete User Account
@user_bp.route("/delete-account", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Account deleted successfully"}), 200

# 🔥 Admin: Get All Users
@user_bp.route("/all-users", methods=["GET"])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        return jsonify({"error": "Admin access required"}), 403

    users = User.query.all()
    users_data = [{"id": user.id, "username": user.username, "email": user.email, "games_played": user.games_played} for user in users]

    return jsonify(users_data), 200

