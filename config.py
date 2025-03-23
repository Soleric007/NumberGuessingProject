import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "60e4049dafc6b38c2a09b7408532beedcb6e8d6a29f765000e81ca1fa8a9a558")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://numbergame:272005@localhost/database_numbergame")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "90972413d732d9bd45b222b37e822ed6756c0a37a637d06745861aca1cdae94b")
