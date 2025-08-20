
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # JWT Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura-aqui-12345")
    
    # Database configuration (optional for JWT-only functionality)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
