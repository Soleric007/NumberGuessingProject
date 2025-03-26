from flask import Blueprint, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS  # ✅ Fix CORS issues
from models import db, Leaderboard, User  

leaderboard_bp = Blueprint('leaderboard', __name__, template_folder='../templates')

CORS(leaderboard_bp)  # ✅ Allow frontend to fetch API data
@leaderboard_bp.route('/')
def leaderboard_page():
    return render_template('leaderboard.html')

# 🏆 Get Leaderboard Data (API Route)
@leaderboard_bp.route('/data', methods=['GET'])  # ✅ Changed route to avoid conflict
def get_leaderboard():
    top_players = Leaderboard.query.order_by(Leaderboard.score.desc()).limit(10).all()

    leaderboard_data = [
        {"username": player.user.username, "score": player.score} for player in top_players
    ]

    return jsonify(leaderboard_data), 200

# 🔢 Get User's Rank
@leaderboard_bp.route('/rank', methods=['GET'])
@jwt_required()
def get_user_rank():
    user_id = get_jwt_identity()
    all_players = Leaderboard.query.order_by(Leaderboard.score.desc()).all()
    user_rank = next((index + 1 for index, player in enumerate(all_players) if player.user_id == user_id), None)

    if user_rank is None:
        return jsonify({"error": "You are not on the leaderboard"}), 404

    return jsonify({"rank": user_rank}), 200
