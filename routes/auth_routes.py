# from flask import Blueprint, request, jsonify
# from models import db, User
# from flask_jwt_extended import create_access_token

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/register', methods=['POST'])

# def register():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     if User.query.filter_by(username=username).first():
#         return jsonify({"error": "User already exists"}), 400

#     user = User(username=username)
#     user.set_password(password)
#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"message": "User registered successfully"}), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     user = User.query.filter_by(username=username).first()

#     if not user or not user.check_password(password):
#         return jsonify({"error": "Invalid credentials"}), 401

#     access_token = create_access_token(identity=str(user.id))  # Convert user.id to string
#     return jsonify({"access_token": access_token}), 200

from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@jwt_required(optional=True)  # ✅ Allows first admin registration without a token
def register():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id) if current_user_id else None

    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False)  # Default to False unless explicitly set

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    # ✅ If no admin exists, the first registered user is automatically an admin
    if User.query.count() == 0:
        is_admin = True  

    # ❌ Prevent normal users from creating admins
    elif is_admin and (not current_user or not current_user.is_admin):
        return jsonify({"error": "Only admins can create another admin"}), 403

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password, is_admin=is_admin)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)  # Keep user.id as an integer
    return jsonify({"access_token": access_token, "is_admin": user.is_admin}), 200

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
