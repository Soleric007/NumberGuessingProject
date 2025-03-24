# import random
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import db, Game, Leaderboard, User

# game_bp = Blueprint('game', __name__)  # ✅ Define only ONCE

# @game_bp.route('/start-game', methods=['POST'])
# @jwt_required()
# def start_game():
#     user_id = get_jwt_identity()
#     data = request.json
#     level = data.get('level', 'low')

#     ranges = {"low": 99, "moderate": 999, "expert": 9999}
#     if level not in ranges:
#         return jsonify({"error": "Invalid difficulty level"}), 400

#     target_number = random.randint(0, ranges[level])
#     game = Game(user_id=user_id, target_number=target_number)
#     db.session.add(game)
#     db.session.commit()

#     return jsonify({"message": "Game started", "game_id": game.id, "level": level})

# @game_bp.route('/guess/<int:game_id>', methods=['POST'])
# @jwt_required()
# def make_guess(game_id):
#     data = request.json
#     guess = data.get('guess')

#     game = Game.query.get(game_id)
#     if not game or game.status != "ongoing":
#         return jsonify({"error": "Invalid game"}), 400

#     game.attempts += 1

#     if guess == game.target_number:
#         game.status = "won"

#         user = User.query.get(game.user_id)
#         if user.best_score is None or game.attempts < user.best_score:
#             user.best_score = game.attempts  # Update best score

#         db.session.commit()
#         return jsonify({"message": "Congratulations! You guessed the number!"})

#     if game.attempts >= game.max_attempts:
#         game.status = "lost"
#         db.session.commit()
#         return jsonify({"message": "Game Over! No more attempts left."})

#     hint = "Too low" if guess < game.target_number else "Too high"
#     db.session.commit()
#     return jsonify({"hint": hint, "attempts_left": game.max_attempts - game.attempts})

# # ✅ DO NOT redefine game_bp here!

# @game_bp.route('/game/update-score', methods=['POST'])
# @jwt_required()
# def update_score():
#     user_id = get_jwt_identity()
#     data = request.get_json()

#     leaderboard_entry = Leaderboard.query.filter_by(user_id=user_id).first()
#     if not leaderboard_entry:
#         leaderboard_entry = Leaderboard(user_id=user_id, score=data.get('score', 0))
#         db.session.add(leaderboard_entry)
#     else:
#         leaderboard_entry.score += data.get('score', 0)

#     db.session.commit()
#     return jsonify({"message": "Score updated successfully"}), 200

# @game_bp.route('/leaderboard', methods=['GET'])
# def get_leaderboard():
#     top_players = (
#         db.session.query(Leaderboard, User)
#         .join(User, Leaderboard.user_id == User.id)
#         .order_by(Leaderboard.score.desc())
#         .limit(10)
#         .all()
#     )

#     leaderboard_data = [{"username": player.username, "score": lb.score} for lb, player in top_players]

#     return jsonify(leaderboard_data), 200

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

    ranges = {"low": 99, "moderate": 999, "expert": 9999}
    if level not in ranges:
        return jsonify({"error": "Invalid difficulty level"}), 400

    target_number = random.randint(0, ranges[level])
    game = Game(user_id=user_id, target_number=target_number)
    db.session.add(game)
    db.session.commit()

    return jsonify({"message": "Game started", "game_id": game.id, "level": level, "attempts_left": game.max_attempts})

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

    game.attempts += 1

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
        return jsonify({"message": "Game Over! No more attempts left."})

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

@game_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    top_players = (
        db.session.query(Leaderboard, User)
        .join(User, Leaderboard.user_id == User.id)
        .order_by(Leaderboard.score.desc())
        .limit(10)
        .all()
    )

    leaderboard_data = [{"username": player.username, "score": lb.score} for lb, player in top_players]

    return jsonify(leaderboard_data), 200
