from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Attendance, LeaveRequest
from app.utils.attendance_service import check_in, check_out, get_effective_setting
from app.utils.audit import log_action
from app.utils.decorators import role_required
from app.utils.time_utils import now_in_tz


intern_bp = Blueprint("intern", __name__, url_prefix="/intern")


def _allowed_attachment(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config.get("ALLOWED_ATTACHMENT_EXTENSIONS", set())


@intern_bp.route("/dashboard")
@role_required("INTERN")
def dashboard():
    setting = get_effective_setting()
    today = now_in_tz(setting.timezone).date()
    today_attendance = Attendance.query.filter_by(user_id=current_user.id, date=today).first()

    return render_template(
        "intern/dashboard.html",
        today_attendance=today_attendance,
        check_in_time=setting.check_in_time,
        check_out_time=setting.check_out_time,
    )


@intern_bp.route("/attendance")
@role_required("INTERN")
def attendance_page():
    setting = get_effective_setting()
    return render_template("intern/attendance.html", setting=setting)


@intern_bp.route("/attendance/check-in", methods=["POST"])
@role_required("INTERN")
def do_check_in():
    lat = float(request.form.get("latitude", "0"))
    lng = float(request.form.get("longitude", "0"))

    ok, message = check_in(current_user, lat, lng)
    flash(message, "success" if ok else "danger")
    return redirect(url_for("intern.dashboard"))


@intern_bp.route("/attendance/check-out", methods=["POST"])
@role_required("INTERN")
def do_check_out():
    lat = float(request.form.get("latitude", "0"))
    lng = float(request.form.get("longitude", "0"))

    ok, message = check_out(current_user, lat, lng)
    flash(message, "success" if ok else "danger")
    return redirect(url_for("intern.dashboard"))


@intern_bp.route("/history")
@role_required("INTERN")
def history():
    month = request.args.get("month")
    year = request.args.get("year")
    status = request.args.get("status")

    query = Attendance.query.filter_by(user_id=current_user.id)

    if month:
        query = query.filter(db.extract("month", Attendance.date) == int(month))
    if year:
        query = query.filter(db.extract("year", Attendance.date) == int(year))
    if status:
        query = query.filter(Attendance.status == status)

    rows = query.order_by(Attendance.date.desc()).all()
    return render_template("intern/history.html", attendances=rows)


@intern_bp.route("/leave", methods=["GET", "POST"])
@role_required("INTERN")
def leave():
    if request.method == "POST":
        request_type = request.form.get("request_type", "SAKIT")
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date()
        planned_checkout_raw = request.form.get("planned_checkout")
        planned_checkout = (
            datetime.strptime(planned_checkout_raw, "%H:%M").time() if planned_checkout_raw else None
        )

        attachment_path = None
        attachment_file = request.files.get("attachment")
        if attachment_file and attachment_file.filename:
            if not _allowed_attachment(attachment_file.filename):
                flash("Format lampiran tidak diizinkan", "danger")
                return redirect(url_for("intern.leave"))

            safe_name = secure_filename(attachment_file.filename)
            suffix = safe_name.rsplit(".", 1)[1].lower()
            generated_name = f"leave_{current_user.id}_{uuid4().hex}.{suffix}"
            upload_dir = Path(current_app.config["UPLOAD_FOLDER"]) / "leave_attachments"
            upload_dir.mkdir(parents=True, exist_ok=True)
            target = upload_dir / generated_name
            attachment_file.save(target)
            attachment_path = str(target)

        leave_request = LeaveRequest(
            user_id=current_user.id,
            request_type=request_type,
            start_date=start_date,
            end_date=end_date,
            planned_checkout=planned_checkout,
            reason=request.form.get("reason", "").strip(),
            attachment=attachment_path,
            status="PENDING",
        )

        db.session.add(leave_request)
        log_action(
            actor_user_id=current_user.id,
            action="CREATE_LEAVE_REQUEST",
            entity="leave_requests",
            metadata={
                "request_type": request_type,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "has_attachment": bool(attachment_path),
            },
        )
        db.session.commit()
        flash("Pengajuan izin berhasil dikirim", "success")
        return redirect(url_for("intern.leave"))

    rows = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.id.desc()).all()
    return render_template("intern/leave.html", leave_requests=rows)


@intern_bp.route("/profile")
@role_required("INTERN")
def profile():
    return render_template("intern/profile.html")
