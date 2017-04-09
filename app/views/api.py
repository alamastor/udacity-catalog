"""API endpoints."""

from flask import jsonify

from ..app import app
from ..models import Catagory
from ..db import db


@app.route('/api')
def api_base():
    """Endpoint returning whole database as JSON."""
    catagories = db.session.query(Catagory).all()
    return jsonify({'catagories': [catagory.dict for catagory in catagories]})