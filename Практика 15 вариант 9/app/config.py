import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','dev-secret-for-study-only')
    DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///rail_flask.db')
