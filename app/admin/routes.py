import csv
import io
from datetime import datetime

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import Attendance, AttendanceSetting, LeaveRequest, Role, User, Zone
from app.utils.decorators import role_required
from app.utils.time_utils import parse_time


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@role_required("ADMIN")
def dashboard():
    total_users = User.query.filter(User.deleted_at.is_(None)).count()
    total_intern = User.query.join(Role).filter(Role.name == "INTERN", User.deleted_at.is_(None)).count()
    total_staff = User.query.join(Role).filter(Role.name == "STAFF", User.deleted_at.is_(None)).count()
    total_admin = User.query.join(Role).filter(Role.name == "ADMIN", User.deleted_at.is_(None)).count()

    today = datetime.utcnow().date()
    attendance_today = Attendance.query.filter_by(date=today).count()
    late_today = Attendance.query.filter_by(date=today, status="TERLAMBAT").count()
    pending_leave = LeaveRequest.query.filter_by(status="PENDING").count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_intern=total_intern,
        total_staff=total_staff,
        total_admin=total_admin,
        attendance_today=attendance_today,
        late_today=late_today,
        pending_leave=pending_leave,
    )


@admin_bp.route("/users")
@role_required("ADMIN")
def users():
    role_filter = request.args.get("role")
    query = User.query.filter(User.deleted_at.is_(None))

    if role_filter:
        query = query.join(Role).filter(Role.name == role_filter)

    users_data = query.order_by(User.id.desc()).all()
    roles = Role.query.order_by(Role.name.asc()).all()
    return render_template("admin/users.html", users=users_data, roles=roles)


@admin_bp.route("/users/create", methods=["GET", "POST"])
@role_required("ADMIN")
def create_user():
    roles = Role.query.order_by(Role.name.asc()).all()
    if request.method == "POST":
        role_id = int(request.form.get("role_id"))

        user = User(
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip().lower(),
            username=request.form.get("username", "").strip().lower(),
            role_id=role_id,
            identity_number=request.form.get("identity_number", "").strip() or None,
            phone=request.form.get("phone", "").strip() or None,
            institution=request.form.get("institution", "").strip() or None,
            department=request.form.get("department", "").strip() or None,
            is_active=request.form.get("is_active") == "on",
        )
        user.set_password(request.form.get("password", "123456"))

        db.session.add(user)
        db.session.commit()

        flash("User berhasil dibuat", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/user_form.html", roles=roles, user=None)


@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@role_required("ADMIN")
def edit_user(user_id: int):
    user = User.query.get_or_404(user_id)
    roles = Role.query.order_by(Role.name.asc()).all()

    if request.method == "POST":
        user.name = request.form.get("name", "").strip()
        user.email = request.form.get("email", "").strip().lower()
        user.username = request.form.get("username", "").strip().lower()
        user.role_id = int(request.form.get("role_id"))
        user.identity_number = request.form.get("identity_number", "").strip() or None
        user.phone = request.form.get("phone", "").strip() or None
        user.institution = request.form.get("institution", "").strip() or None
        user.department = request.form.get("department", "").strip() or None
        user.is_active = request.form.get("is_active") == "on"

        new_password = request.form.get("password", "").strip()
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash("User berhasil diperbarui", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/user_form.html", roles=roles, user=user)


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@role_required("ADMIN")
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    user.deleted_at = datetime.utcnow()
    user.is_active = False
    db.session.commit()
    flash("User dihapus secara soft delete", "warning")
    return redirect(url_for("admin.users"))


@admin_bp.route("/zones")
@role_required("ADMIN")
def zones():
    zone_items = Zone.query.order_by(Zone.id.desc()).all()
    return render_template("admin/zones.html", zones=zone_items)


@admin_bp.route("/zones/create", methods=["POST"])
@role_required("ADMIN")
def create_zone():
    zone = Zone(
        name=request.form.get("name", "").strip(),
        description=request.form.get("description", "").strip() or None,
        latitude=float(request.form.get("latitude", "0")),
        longitude=float(request.form.get("longitude", "0")),
        radius=float(request.form.get("radius", "100")),
        is_active=request.form.get("is_active") == "on",
    )
    db.session.add(zone)
    db.session.commit()
    flash("Zona berhasil ditambahkan", "success")
    return redirect(url_for("admin.zones"))


@admin_bp.route("/zones/<int:zone_id>/edit", methods=["GET", "POST"])
@role_required("ADMIN")
def edit_zone(zone_id: int):
    zone = Zone.query.get_or_404(zone_id)

    if request.method == "POST":
        zone.name = request.form.get("name", "").strip()
        zone.description = request.form.get("description", "").strip() or None
        zone.latitude = float(request.form.get("latitude", "0"))
        zone.longitude = float(request.form.get("longitude", "0"))
        zone.radius = float(request.form.get("radius", "100"))
        zone.is_active = request.form.get("is_active") == "on"

        db.session.commit()
        flash("Zona berhasil diperbarui", "success")
        return redirect(url_for("admin.zones"))

    return render_template("admin/zone_form.html", zone=zone)


@admin_bp.route("/zones/<int:zone_id>/delete", methods=["POST"])
@role_required("ADMIN")
def delete_zone(zone_id: int):
    zone = Zone.query.get_or_404(zone_id)

    used_count = Attendance.query.filter_by(zone_id=zone.id).count()
    if used_count > 0:
        flash("Zona tidak bisa dihapus karena sudah dipakai data absensi", "danger")
        return redirect(url_for("admin.zones"))

    db.session.delete(zone)
    db.session.commit()
    flash("Zona berhasil dihapus", "success")
    return redirect(url_for("admin.zones"))


@admin_bp.route("/zones/<int:zone_id>/toggle", methods=["POST"])
@role_required("ADMIN")
def toggle_zone(zone_id: int):
    zone = Zone.query.get_or_404(zone_id)
    zone.is_active = not zone.is_active
    db.session.commit()
    flash("Status zona diperbarui", "success")
    return redirect(url_for("admin.zones"))


@admin_bp.route("/settings", methods=["GET", "POST"])
@role_required("ADMIN")
def settings():
    setting = AttendanceSetting.get_active()

    if request.method == "POST":
        check_in_time = parse_time(request.form.get("check_in_time"), setting.check_in_time)
        check_out_time = parse_time(request.form.get("check_out_time"), setting.check_out_time)
        tolerance = int(request.form.get("late_tolerance_minutes", setting.late_tolerance_minutes))
        timezone = request.form.get("timezone", "Asia/Makassar").strip() or "Asia/Makassar"

        setting.check_in_time = check_in_time
        setting.check_out_time = check_out_time
        setting.late_tolerance_minutes = tolerance
        setting.timezone = timezone

        db.session.commit()
        flash("Pengaturan absensi diperbarui", "success")
        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html", setting=setting)


@admin_bp.route("/attendance")
@role_required("ADMIN")
def attendance():
    selected_date = request.args.get("date")
    query = Attendance.query.join(User).filter(User.deleted_at.is_(None))
    if selected_date:
        query = query.filter(Attendance.date == datetime.strptime(selected_date, "%Y-%m-%d").date())
    rows = query.order_by(Attendance.date.desc(), Attendance.id.desc()).all()
    return render_template("admin/attendance.html", attendances=rows)


@admin_bp.route("/leave-requests")
@role_required("ADMIN")
def leave_requests():
    rows = LeaveRequest.query.order_by(LeaveRequest.id.desc()).all()
    return render_template("admin/leave_requests.html", leave_requests=rows)


@admin_bp.route("/reports")
@role_required("ADMIN")
def reports():
    status_filter = request.args.get("status")
    query = Attendance.query.join(User).filter(User.deleted_at.is_(None))

    if status_filter:
        query = query.filter(Attendance.status == status_filter)

    rows = query.order_by(Attendance.date.desc(), Attendance.id.desc()).all()
    return render_template("admin/reports.html", attendances=rows)


@admin_bp.route("/reports/export-csv")
@role_required("ADMIN")
def export_reports_csv():
    rows = (
        Attendance.query.join(User)
        .filter(User.deleted_at.is_(None))
        .order_by(Attendance.date.desc(), Attendance.id.desc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Tanggal", "Nama", "Masuk", "Pulang", "Status", "Zona"])

    for row in rows:
        writer.writerow(
            [
                row.date.isoformat(),
                row.user.name,
                row.check_in.strftime("%H:%M") if row.check_in else "-",
                row.check_out.strftime("%H:%M") if row.check_out else "-",
                row.status,
                row.zone.name if row.zone else "-",
            ]
        )

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=laporan_kehadiran.csv"},
    )
