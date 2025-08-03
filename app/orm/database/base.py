import os
from flask_sqlalchemy import SQLAlchemy

# Load environment variables

db = SQLAlchemy()

def create_tables(app):
    """
    Creates all tables defined in SQLAlchemy models using the Flask app context.
    """
    try:
        with app.app_context():
            db.create_all()
            print("✅ Tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise e