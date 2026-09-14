from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.models import Attendance, LeaveRequest, Role, User
from app.utils.decorators import role_required


staff_bp = Blueprint("staff", __name__, url_prefix="/staff")


@staff_bp.route("/dashboard")
@role_required("STAFF", "ADMIN")
def dashboard():
    today = datetime.utcnow().date()

    total_intern = User.query.join(Role).filter(Role.name == "INTERN", User.deleted_at.is_(None)).count()
    already_check_in = Attendance.query.filter(Attendance.date == today, Attendance.check_in.isnot(None)).count()
    not_check_in = max(total_intern - already_check_in, 0)
    late = Attendance.query.filter_by(date=today, status="TERLAMBAT").count()
    izin = Attendance.query.filter_by(date=today, status="IZIN").count()
    sakit = Attendance.query.filter_by(date=today, status="SAKIT").count()

    attendance_today = Attendance.query.filter_by(date=today).order_by(Attendance.id.desc()).all()

    return render_template(
        "staff/dashboard.html",
        total_intern=total_intern,
        already_check_in=already_check_in,
        not_check_in=not_check_in,
        late=late,
        izin=izin,
        sakit=sakit,
        attendance_today=attendance_today,
    )


@staff_bp.route("/attendance")
@role_required("STAFF", "ADMIN")
def attendance():
    selected_date = request.args.get("date")
    query = Attendance.query

    if selected_date:
        query = query.filter(Attendance.date == datetime.strptime(selected_date, "%Y-%m-%d").date())

    rows = query.order_by(Attendance.date.desc(), Attendance.id.desc()).all()
    return render_template("staff/attendance.html", attendances=rows)


@staff_bp.route("/leave-requests")
@role_required("STAFF", "ADMIN")
def leave_requests():
    status = request.args.get("status")
    query = LeaveRequest.query

    if status:
        query = query.filter(LeaveRequest.status == status)

    rows = query.order_by(LeaveRequest.id.desc()).all()
    return render_template("staff/leave_requests.html", leave_requests=rows)


@staff_bp.route("/leave-requests/<int:request_id>/review", methods=["POST"])
@role_required("STAFF", "ADMIN")
def review_leave_request(request_id: int):
    row = LeaveRequest.query.get_or_404(request_id)

    decision = request.form.get("decision")
    notes = request.form.get("review_notes", "").strip() or None

    if row.status != "PENDING":
        flash("Pengajuan sudah diproses", "warning")
        return redirect(url_for("staff.leave_requests"))

    row.status = "APPROVED" if decision == "APPROVE" else "REJECTED"
    row.review_notes = notes
    row.reviewed_by = current_user.id
    row.reviewed_at = datetime.utcnow()

    if row.status == "APPROVED" and row.request_type == "SAKIT":
        current_day = row.start_date
        while current_day <= row.end_date:
            attendance = Attendance.query.filter_by(user_id=row.user_id, date=current_day).first()
            if not attendance:
                attendance = Attendance(user_id=row.user_id, date=current_day)
            attendance.status = "SAKIT"
            db.session.add(attendance)
            current_day = current_day.fromordinal(current_day.toordinal() + 1)

    db.session.commit()
    flash("Pengajuan izin diproses", "success")
    return redirect(url_for("staff.leave_requests"))


@staff_bp.route("/reports")
@role_required("STAFF", "ADMIN")
def reports():
    rows = Attendance.query.order_by(Attendance.date.desc(), Attendance.id.desc()).all()
    return render_template("staff/reports.html", attendances=rows)
