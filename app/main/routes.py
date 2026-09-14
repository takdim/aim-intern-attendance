from flask import Blueprint, redirect, url_for
from flask_login import current_user


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    role = current_user.role.name if current_user.role else ""
    if role == "ADMIN":
        return redirect(url_for("admin.dashboard"))
    if role == "STAFF":
        return redirect(url_for("staff.dashboard"))
    return redirect(url_for("intern.dashboard"))
