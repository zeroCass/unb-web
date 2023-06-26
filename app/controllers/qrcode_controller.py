from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user

bp = Blueprint("qrcode", __name__)


@bp.route("/", methods=["GET", "POST"])
def qrcode():
    if request.method == "GET":
        return render_template("qrcode.jinja2")

    decoded_text = request.form.get("decoded_text")
    print(f"qrcode scan: {decoded_text}")
    response = {"status": "sucess"}
    return jsonify(response)
