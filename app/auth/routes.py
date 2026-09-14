from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        identity = request.form.get("identity", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.email == identity) | (User.username == identity),
            User.deleted_at.is_(None),
            User.is_active.is_(True),
        ).first()

        if not user or not user.check_password(password):
            flash("Email/username atau password salah", "danger")
            return render_template("auth/login.html")

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
