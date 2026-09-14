from datetime import time
from pathlib import Path

import click
from flask import Flask

from app.config import Config
from app.extensions import csrf, db, login_manager
from app.models import AttendanceSetting, Role, User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.admin.routes import admin_bp
    from app.staff.routes import staff_bp
    from app.intern.routes import intern_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(intern_bp)

    @app.before_request
    def run_auto_checkout() -> None:
        from app.utils.attendance_service import auto_close_checkout_if_due

        auto_close_checkout_if_due()

    @app.cli.command("init-db")
    def init_db() -> None:
        db.create_all()
        seed_defaults()
        print("Database initialized")

    @app.cli.command("mark-alpha")
    def mark_alpha() -> None:
        from app.models import Attendance, LeaveRequest
        from app.utils.time_utils import today_in_tz

        setting = AttendanceSetting.get_active()
        tz_name = setting.timezone if setting else "Asia/Makassar"
        target_day = today_in_tz(tz_name)

        interns = User.query.join(Role).filter(Role.name == "INTERN", User.is_active.is_(True)).all()

        for user in interns:
            has_attendance = Attendance.query.filter_by(user_id=user.id, date=target_day).first()
            has_approved_leave = (
                LeaveRequest.query.filter(
                    LeaveRequest.user_id == user.id,
                    LeaveRequest.status == "APPROVED",
                    LeaveRequest.start_date <= target_day,
                    LeaveRequest.end_date >= target_day,
                ).first()
                is not None
            )

            if not has_attendance and not has_approved_leave:
                db.session.add(Attendance(user_id=user.id, date=target_day, status="ALPHA"))

        db.session.commit()
        print("ALPHA marking finished")

    @app.cli.command("auto-close-checkout")
    def auto_close_checkout() -> None:
        from app.utils.attendance_service import auto_close_checkout_if_due

        total = auto_close_checkout_if_due()
        print(f"Auto checkout processed: {total}")

    @app.cli.command("create-admin")
    @click.option("--name", required=True, help="Nama admin")
    @click.option("--email", required=True, help="Email admin")
    @click.option("--username", required=True, help="Username admin")
    @click.option("--password", required=True, help="Password admin")
    def create_admin(name: str, email: str, username: str, password: str) -> None:
        admin_role = Role.query.filter_by(name="ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN")
            db.session.add(admin_role)
            db.session.flush()

        exists = User.query.filter(
            (User.email == email.lower()) | (User.username == username.lower()),
            User.deleted_at.is_(None),
        ).first()
        if exists:
            print("Admin gagal dibuat: email atau username sudah dipakai")
            return

        admin = User(
            name=name.strip(),
            email=email.strip().lower(),
            username=username.strip().lower(),
            role_id=admin_role.id,
            is_active=True,
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin berhasil dibuat")

    return app


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


def seed_defaults() -> None:
    roles = ["ADMIN", "STAFF", "INTERN"]
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))

    if not AttendanceSetting.query.first():
        db.session.add(
            AttendanceSetting(
                check_in_time=time(7, 30),
                check_out_time=time(16, 0),
                late_tolerance_minutes=15,
                timezone="Asia/Makassar",
            )
        )

    db.session.commit()
