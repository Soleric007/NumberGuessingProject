# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "60e4049dafc6b38c2a09b7408532beedcb6e8d6a29f765000e81ca1fa8a9a558")
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://numbergame:272005@localhost/database_numbergame")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "90972413d732d9bd45b222b37e822ed6756c0a37a637d06745861aca1cdae94b")

import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

    # ✅ Ensure proper PostgreSQL URI format
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Secure JWT Secret Key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # ✅ Allow JWT cookies for frontend auth
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False  # Set to True in production (for HTTPS)
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_COOKIE_CSRF_PROTECT = False  # Enable this in production for security

