from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False) 
    games_played = db.Column(db.Integer, default=0)
    best_score = db.Column(db.Integer, default=None)

    # Hash password
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Relationship with cascade delete
    games = relationship('Game', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    leaderboard = relationship('Leaderboard', backref='user', cascade="all, delete-orphan", passive_deletes=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    target_number = db.Column(db.Integer, nullable=False)
    attempts = db.Column(db.Integer, default=0)
    max_attempts = db.Column(db.Integer, default=10)
    difficulty = db.Column(db.String(20), nullable=False, default="easy")  # "easy", "medium", "hard"
    status = db.Column(db.String(20), default="ongoing")  # "ongoing", "won", "lost"


class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, default="easy")  # Storing difficulty in leaderboard
