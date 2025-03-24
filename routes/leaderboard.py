# from flask import Blueprint, jsonify
# from models import db, Leaderboard  # Import db directly from models

# leaderboard_bp = Blueprint('leaderboard', __name__)

# @leaderboard_bp.route('/', methods=['GET'])
# def get_leaderboard():
#     top_players = Leaderboard.query.order_by(Leaderboard.score.desc()).limit(10).all()
    
#     leaderboard_data = [
#         {"username": player.user.username, "score": player.score} for player in top_players
#     ]
    
#     return jsonify(leaderboard_data), 200
# leaderboard_bp = Blueprint('leaderboard_bp', __name__)

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Leaderboard, User  # Import User for rank checking

leaderboard_bp = Blueprint('leaderboard', __name__)

# 🏆 Get Leaderboard (Top 10 Players)
@leaderboard_bp.route('/', methods=['GET'])
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
    
    # Fetch all players ordered by score
    all_players = Leaderboard.query.order_by(Leaderboard.score.desc()).all()
    user_rank = next((index + 1 for index, player in enumerate(all_players) if player.user_id == user_id), None)

    if user_rank is None:
        return jsonify({"error": "You are not on the leaderboard"}), 404

    return jsonify({"rank": user_rank}), 200
