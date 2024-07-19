from flask import Blueprint, render_template, request, session, redirect, url_for, make_response, jsonify
import logging
from descope import DescopeClient
from functools import wraps
from flask_login import current_user, login_user, logout_user, login_required, AnonymousUserMixin

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger('auth')
DESCOPE_PROJECT_ID = 'P2iRuQ0iD6pJVWtofatuMIdl1Xsj'
descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)
HCAPTCHA_SECRET_KEY = 'ES_d0da5e64b540401eb477437d59c62639'
users_online = []


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        session_token = None
        if 'Authorization' in request.headers:  # check if token in request
            auth_request = request.headers['Authorization']
            session_token = auth_request.replace('Bearer ', '')
        if not session_token or session_token is None:
            return redirect('/auth/login')

        try:
            # validate token
            jwt_response = descope_client.validate_session(session_token=session_token)
            if not jwt_response or jwt_response is None:
                return redirect('/auth/login')
        except:
            return redirect('/auth/login')

        print(jwt_response)

        return f(jwt_response, *args, **kwargs)

    return decorator


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = 'anonymous'

    def is_anonymous(self):
        return True


@auth_bp.route('/profile')
def profile():
    return render_template("html/auth/profile.html")


@auth_bp.route('/get_secret_message', methods=["GET"])
@token_required
def get_secret_message(jwt_response):
    print(jwt_response)
    return {"secret_msg": "This is the secret message. Congrats!"}


@auth_bp.route('/login', methods=['GET'])
def login():
    if 'Authorization' in request.headers:
        session_token = request.headers['Authorization'].replace('Bearer ', '')
        try:
            descope_client.validate_session(session_token=session_token)
            logger.debug("Valid session token found, redirecting to profile.")
            return redirect(url_for('auth.profile'))
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
    return render_template('html/auth/login.html')


@auth_bp.route('/hop', methods=['GET'])
def hop():
    anonymous_user = Anonymous()
    login_user(anonymous_user)
    return redirect("/auth/profile")


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('html/auth/register.html')


@auth_bp.route('/hopp')
def hopp():
    anonymous_user = Anonymous()
    login_user(anonymous_user)
    return redirect("/login")
