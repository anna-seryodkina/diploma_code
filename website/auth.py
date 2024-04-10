from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p> this is login </p>"


@auth.route('/logout')
def logout():
    return "<p> this is logout </p>"


@auth.route('/sign-up')
def sign_up():
    return "<p> this is sign up </p>"
