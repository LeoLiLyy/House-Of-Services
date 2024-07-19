from flask import Flask, request, session, g, redirect, url_for, make_response, jsonify, render_template, flash
import secrets
import logging
from datetime import date
import colorlog
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.translations import load_translations
from descope import DescopeClient
import os
from functools import wraps

login_manager = LoginManager()
db = SQLAlchemy()


def create_app():
    try:
        descope_client = DescopeClient(project_id="P2iRuQ0iD6pJVWtofatuMIdl1Xsj")
    except Exception as error:
        print("failed to initialize. Error:")
        print(error)
    global email
    user = ''
    is_admin = False
    log_name = date.today()
    log_f_name = str(log_name) + '.log'
    users_online = []

    app = Flask(__name__)
    app.secret_key = secrets.token_hex()

    debug = True

    logger = colorlog.getLogger('logger')
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    handler = logging.FileHandler(f'./logs/{log_f_name}')
    handler.setLevel(logging.DEBUG if debug else logging.INFO)

    console = colorlog.StreamHandler()
    console.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'black',
            'ERROR': 'red',
            'CRITICAL': 'purple'
        }
    )

    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.debug(f'[!] Logger starting, log saved at: {log_f_name}')
    logger.addHandler(handler)

    app.config['UPLOAD_FOLDER'] = './uploads'
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'  # Use SQLite for simplicity
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secrets.token_hex()

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth.route import auth_bp
    from app.auth.financial.route import auth_fin_bp
    from app.core.route import core_bp
    from app.service.route import service_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(auth_fin_bp, url_prefix='/auth/fin')
    app.register_blueprint(core_bp, url_prefix='/core')
    app.register_blueprint(service_bp, url_prefix='/service')

    @app.context_processor
    def inject_translations():
        return dict(_=g.translations.get)

    @app.before_request
    def set_language():
        if 'language' not in session:
            session['language'] = request.accept_languages.best_match(['en_US', 'zh_CN'])
        g.translations = load_translations(session['language'])

    @app.route('/set_language', methods=['POST'], endpoint='set_language')
    def set_language_route():
        language = request.form['language']
        session['language'] = language
        return redirect(request.referrer)

    @app.route('/login')
    def login():
        return redirect("/auth/login")

    @app.errorhandler(404)
    def page_not_found():
        return render_template('html/core/error/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error():
        return render_template('html/core/error/500.html'), 500
    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def handle_needs_login():
    return redirect(url_for('auth.login'))
