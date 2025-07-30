import os

# project root, two levels up
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# persist to sqlite file in project root
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'feedback.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
