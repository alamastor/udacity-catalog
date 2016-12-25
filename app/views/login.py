from flask import session, request, redirect

from app import app


@app.route('/login', methods=['POST'])
def login():
    # TODO: Dummy, replace with OAuth login.
    session['logged_in'] = True
    return redirect(request.referrer)  # TODO: Make this safe.
