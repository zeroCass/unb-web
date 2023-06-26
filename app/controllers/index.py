from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint("index", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    print(f"turmas do usuario: {current_user.turmas}")
    print(f"user: {current_user}")
    return render_template("index.jinja2", user=current_user)
