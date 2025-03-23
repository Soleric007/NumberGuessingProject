from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
from routes.auth_routes import auth_bp
from routes.game_routes import game_bp
from routes.user_routes import user_bp
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
# Register Blueprints (Routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(game_bp, url_prefix='/game')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == "__main__":
    app.run(debug=True)
