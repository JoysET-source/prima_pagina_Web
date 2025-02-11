from flask_login import LoginManager, login_required
from flask import render_template
from main import app

from models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

