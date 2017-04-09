"""Get SQLAlchemy db instance."""
from flask_sqlalchemy import SQLAlchemy

from .app import app


db = SQLAlchemy(app)