import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Game

game_bp = Blueprint('game', __name__)

@game_bp.route('/start-game', methods=['POST'])
@jwt_required()
def start_game():
    user_id = get_jwt_identity()
    data = request.json
    level = data.get('level', 'low')

    ranges = {"low": 99, "moderate": 999, "expert": 9999}
    if level not in ranges:
        return jsonify({"error": "Invalid difficulty level"}), 400

    target_number = random.randint(0, ranges[level])
    game = Game(user_id=user_id, target_number=target_number)
    db.session.add(game)
    db.session.commit()

    return jsonify({"message": "Game started", "game_id": game.id, "level": level})

@game_bp.route('/guess/<int:game_id>', methods=['POST'])
@jwt_required()
def make_guess(game_id):
    data = request.json
    guess = data.get('guess')

    game = Game.query.get(game_id)
    if not game or game.status != "ongoing":
        return jsonify({"error": "Invalid game"}), 400

    game.attempts += 1

    if guess == game.target_number:
        game.status = "won"
        db.session.commit()
        return jsonify({"message": "Congratulations! You guessed the number!"})

    if game.attempts >= game.max_attempts:
        game.status = "lost"
        db.session.commit()
        return jsonify({"message": "Game Over! No more attempts left."})

    hint = "Too low" if guess < game.target_number else "Too high"
    db.session.commit()
    return jsonify({"hint": hint, "attempts_left": game.max_attempts - game.attempts})
