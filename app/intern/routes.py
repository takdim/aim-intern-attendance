from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.models import Attendance, LeaveRequest
from app.utils.attendance_service import check_in, check_out, get_effective_setting
from app.utils.decorators import role_required
from app.utils.time_utils import now_in_tz


intern_bp = Blueprint("intern", __name__, url_prefix="/intern")


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

        leave_request = LeaveRequest(
            user_id=current_user.id,
            request_type=request_type,
            start_date=start_date,
            end_date=end_date,
            planned_checkout=planned_checkout,
            reason=request.form.get("reason", "").strip(),
            status="PENDING",
        )

        db.session.add(leave_request)
        db.session.commit()
        flash("Pengajuan izin berhasil dikirim", "success")
        return redirect(url_for("intern.leave"))

    rows = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.id.desc()).all()
    return render_template("intern/leave.html", leave_requests=rows)


@intern_bp.route("/profile")
@role_required("INTERN")
def profile():
    return render_template("intern/profile.html")
