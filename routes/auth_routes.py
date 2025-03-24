from flask import Blueprint, request, jsonify, make_response
from models import db, User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    unset_jwt_cookies, set_access_cookies, get_jwt
)
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

# 🚀 Register User
@auth_bp.route('/register', methods=['POST'])
@jwt_required(optional=True)  # ✅ Allows first-time registration without authentication
def register():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id) if current_user_id else None

    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False)  # Default: False

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    # ✅ If no admin exists, first user becomes an admin
    if User.query.count() == 0:
        is_admin = True  
    elif is_admin and (not current_user or not current_user.is_admin):
        return jsonify({"error": "Only admins can create another admin"}), 403

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password, is_admin=is_admin)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# 🔑 Login User & Set Token in Cookies
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):  # ✅ Fix: Uses `password_hash`
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(hours=2))

    response = make_response(jsonify({
        "message": "Login successful!",
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin,
        "token": access_token  # ✅ Send token in response for frontend auth
    }))

    # ✅ Store JWT in both cookie & response (so frontend can access it)
    response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="Strict")

    return response

# 🔓 Check Authentication
@auth_bp.route('/check-auth', methods=['GET'])
@jwt_required()
def check_auth():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin
    }), 200

# ❌ Logout User (Clears Token)
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    unset_jwt_cookies(response)
    response.set_cookie("access_token", "", expires=0, httponly=True)
    return response

# 🔥 Admin Route: Get All Users
@auth_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        return jsonify({"error": "Admin access required"}), 403

    users = User.query.all()
    users_data = [{"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin} for user in users]

    return jsonify(users_data), 200
