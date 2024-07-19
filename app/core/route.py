from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from flask_login import login_user, logout_user, login_required, current_user
from app.translations import load_translations
from markupsafe import escape
import hashlib
import os
import requests
import logging

core_bp = Blueprint('core', __name__)

logger = logging.getLogger('core')


# Welcome page / Homepage
@core_bp.route("/welcome")
def welcome_page():
    return render_template('./html/core/welcome.html')
