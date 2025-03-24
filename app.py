# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager
# from config import Config
# from models import db, bcrypt
# from routes.auth_routes import auth_bp
# from routes.game_routes import game_bp
# from routes.user_routes import user_bp
# from flask_migrate import Migrate
# from routes.game_routes import game_bp  # Import the game blueprint
# from routes.leaderboard import leaderboard_bp
# from routes.admin_routes import admin_bp

# app = Flask(__name__, static_folder='static', template_folder='templates')
# app.config.from_object(Config)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/game')
# def game():
#     return render_template('game.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')

# # Initialize extensions
# db.init_app(app)
# bcrypt.init_app(app)
# jwt = JWTManager(app)
# migrate = Migrate(app, db)
# # Register Blueprints (Routes)
# app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(game_bp, url_prefix='/game')
# app.register_blueprint(user_bp, url_prefix='/user')
# app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
# app.register_blueprint(admin_bp, url_prefix='/admin')

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS  # ✅ Added CORS for frontend-backend interaction

from config import Config
from models import db, bcrypt
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

if __name__ == "__main__":
    app.run(debug=True)
