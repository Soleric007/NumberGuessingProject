from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS 
from datetime import datetime
from config import Config
from models import db, bcrypt, Feedback
from routes.auth_routes import auth_bp
from routes.game_routes import game_bp
from routes.user_routes import user_bp
from routes.leaderboard import leaderboard_bp
from routes.admin_routes import admin_bp

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

# ✅ Enable CORS
CORS(app, supports_credentials=True)

# ✅ Initialize Extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# ✅ Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(game_bp, url_prefix='/game')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
app.register_blueprint(admin_bp, url_prefix='/admin')

# ✅ Define Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        data = request.json
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        new_feedback = Feedback(name=name, email=email, message=message)
        db.session.add(new_feedback)
        db.session.commit()
        
        return jsonify({"success": "Feedback submitted!"})

    return render_template("feedback.html")

@app.route("/admin/feedbacks", methods=["GET"])
def get_feedbacks():
    try:
        feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
        
        if not feedbacks:
            return jsonify([])  # Return an empty list if no feedback exists
        
        feedback_list = [
            {
                "id": fb.id,
                "name": fb.name,
                "email": fb.email,
                "message": fb.message,
                # ✅ Check if `submitted_at` is None before formatting
                "submitted_at": fb.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if fb.submitted_at else "N/A",
            }
            for fb in feedbacks
        ]
        return jsonify(feedback_list)

    except Exception as e:
        print(f"Error fetching feedbacks: {e}")  # Log the error in the terminal
        return jsonify({"error": "Internal Server Error"}), 500

