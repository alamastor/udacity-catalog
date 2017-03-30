from flask import session

from app import app


@app.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    return '', 204