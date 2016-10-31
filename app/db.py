from flask_sqlalchemy import SQLAlchemy

from app import app


db = SQLAlchemy(app)


@app.cli.command()
def create_tables():
    db.create_all()


@app.cli.command()
def drop_tables():
    db.drop_all()
