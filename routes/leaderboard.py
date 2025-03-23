from flask import Blueprint, jsonify
from models import db, Leaderboard  # Import db directly from models

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard():
    top_players = Leaderboard.query.order_by(Leaderboard.score.desc()).limit(10).all()
    
    leaderboard_data = [
        {"username": player.user.username, "score": player.score} for player in top_players
    ]
    
    return jsonify(leaderboard_data), 200
leaderboard_bp = Blueprint('leaderboard_bp', __name__)

