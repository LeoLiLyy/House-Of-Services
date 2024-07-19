from app import create_app, session
from app.models import User
from flask import redirect

app = create_app()


@app.route("/")
def homepage_redirect():
    return redirect("/core/welcome")


# @app.before_request
# def validate_session_token():
#     global email
#     # check if the user is authenticated
#     if current_user.is_authenticated:
#         db_token = User.query.filter_by(UserID=current_user.get_id()).first().session_token
#         session_token = session.get('user_token')
#         # validating the user session token
#         if not session_token or session_token != db_token:
#             # requiring the user to re-login if user's session token is invalid
#             logout_user()
#             return redirect('/auth/login')


if __name__ == '__main__':
    app.run(debug=True)
