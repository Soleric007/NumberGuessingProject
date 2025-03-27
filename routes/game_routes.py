import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Game, Leaderboard, User

game_bp = Blueprint('game', __name__)  # ✅ Define only ONCE

@game_bp.route('/start-game', methods=['POST'])
@jwt_required()
def start_game():
    user_id = get_jwt_identity()
    data = request.json
    level = data.get('level', 'low')

    difficulty_settings = {
        "low": {"range": 99, "max_attempts": 10},
        "moderate": {"range": 999, "max_attempts": 7},
        "expert": {"range": 9999, "max_attempts": 5}
    }

    if level not in difficulty_settings:
        return jsonify({"error": "Invalid difficulty level"}), 400

    settings = difficulty_settings[level]
    target_number = random.randint(0, settings["range"])

    game = Game(user_id=user_id, target_number=target_number, difficulty=level, max_attempts=settings["max_attempts"])
    db.session.add(game)
    db.session.commit()

    return jsonify({
        "message": "Game started",
        "game_id": game.id,
        "level": level,
        "attempts_left": game.max_attempts
    })

@game_bp.route('/guess/<int:game_id>', methods=['POST'])
@jwt_required()
def make_guess(game_id):
    user_id = get_jwt_identity()
    data = request.json
    guess = data.get('guess')

    if guess is None or not isinstance(guess, int):
        return jsonify({"error": "Invalid guess"}), 400

    game = Game.query.filter_by(id=game_id, user_id=user_id, status="ongoing").first()
    if not game:
        return jsonify({"error": "Invalid game or game already ended"}), 400
    
    if game.max_attempts is None:
        game.max_attempts = 10 
    game.attempts += 1

    print(f"DEBUG: User {user_id} guessed {guess}. Target: {game.target_number}. Attempts: {game.attempts}/{game.max_attempts}")

    if guess == game.target_number:
        game.status = "won"
        user = User.query.get(user_id)
        user.games_played += 1
        if user.best_score is None or game.attempts < user.best_score:
            user.best_score = game.attempts  # Update best score

        # ✅ Update leaderboard
        leaderboard_entry = Leaderboard.query.filter_by(user_id=user_id).first()
        if not leaderboard_entry:
            leaderboard_entry = Leaderboard(user_id=user_id, score=1000 - (game.attempts * 10))
            db.session.add(leaderboard_entry)
        else:
            leaderboard_entry.score += 1000 - (game.attempts * 10)

        db.session.commit()
        return jsonify({"message": "Congratulations! You guessed the number!", "score": 1000 - (game.attempts * 10)})

    if game.attempts >= game.max_attempts:
        game.status = "lost"
        db.session.commit()
        return jsonify({
            "message": "Game Over! No more attempts left.",
            "hint": f"The correct number was {game.target_number}",
            "attempts_left": 0
        })


    hint = "Too low" if guess < game.target_number else "Too high"
    db.session.commit()
    return jsonify({"hint": hint, "attempts_left": game.max_attempts - game.attempts})

@game_bp.route('/update-score', methods=['POST'])
@jwt_required()
def update_score():
    user_id = get_jwt_identity()
    data = request.get_json()
    score = data.get('score', 0)

    leaderboard_entry = Leaderboard.query.filter_by(user_id=user_id).first()
    if not leaderboard_entry:
        leaderboard_entry = Leaderboard(user_id=user_id, score=score)
        db.session.add(leaderboard_entry)
    else:
        leaderboard_entry.score += score

    db.session.commit()
    return jsonify({"message": "Score updated successfully"}), 200

