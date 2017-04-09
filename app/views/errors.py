"""Error endpoints."""
from flask import render_template

from ..app import app


@app.errorhandler(404)
def not_found(e):
    error_text = '404: Page not found.'
    return render_template('error.html', error_text=error_text), 404


@app.errorhandler(401)
def unauthorized(e):
    error_text = '401: Unauthorized.'
    return render_template('error.html', error_text=error_text), 401


@app.errorhandler(403)
def forbidden(e):
    error_text = '403: Forbidden.'
    return render_template('error.html', error_text=error_text), 403


@app.errorhandler(500)
def error(e):
    error_text = '500: Server error.'
    return render_template('error.html', error_text=error_text), 500