from flask import Blueprint, render_template, g

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    return render_template("index.html")
