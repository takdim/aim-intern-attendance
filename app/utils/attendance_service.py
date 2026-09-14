from datetime import date, datetime, time, timedelta
from typing import Optional, Tuple

from flask import current_app

from app.extensions import db
from app.models import Attendance, AttendanceSetting, LeaveRequest, Zone
from app.utils.geo import haversine_meters
from app.utils.time_utils import now_in_tz, parse_time


def get_effective_setting() -> AttendanceSetting:
    setting = AttendanceSetting.get_active()
    if setting:
        return setting
    fallback = AttendanceSetting(
        check_in_time=datetime.strptime("07:30", "%H:%M").time(),
        check_out_time=datetime.strptime("16:00", "%H:%M").time(),
        late_tolerance_minutes=15,
        timezone="Asia/Makassar",
    )
    db.session.add(fallback)
    db.session.commit()
    return fallback


def resolve_zone_and_distance(
    lat: float, lng: float, tolerance_meters: float = 0.0
) -> Tuple[Optional[Zone], Optional[float]]:
    zones = Zone.query.filter_by(is_active=True).all()
    nearest_zone = None
    nearest_distance = None
    matched_zone = None
    matched_distance = None

    for zone in zones:
        distance = haversine_meters(lat, lng, zone.latitude, zone.longitude)
        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_zone = zone

        if distance <= (zone.radius + tolerance_meters):
            if matched_distance is None or distance < matched_distance:
                matched_zone = zone
                matched_distance = distance

    if matched_zone is not None and matched_distance is not None:
        return matched_zone, matched_distance

    if nearest_zone is None or nearest_distance is None:
        return None, None

    return None, nearest_distance


def can_checkout_early(user_id: int, target_date: date, current_time) -> bool:
    leave = (
        LeaveRequest.query.filter(
            LeaveRequest.user_id == user_id,
            LeaveRequest.request_type == "PULANG_CEPAT",
            LeaveRequest.status == "APPROVED",
            LeaveRequest.start_date <= target_date,
            LeaveRequest.end_date >= target_date,
        )
        .order_by(LeaveRequest.id.desc())
        .first()
    )

    if not leave or not leave.planned_checkout:
        return False

    return current_time >= leave.planned_checkout


def auto_close_checkout_if_due() -> int:
    setting = get_effective_setting()
    now = now_in_tz(setting.timezone)
    target_date = now.date()
    auto_close_time = parse_time(
        current_app.config.get("AUTO_CLOSE_CHECKOUT_TIME", "18:00"), time(18, 0)
    )

    if now.time() < auto_close_time:
        return 0

    auto_checkout_dt = datetime.combine(target_date, auto_close_time)

    rows = (
        Attendance.query.filter(
            Attendance.date == target_date,
            Attendance.check_in.isnot(None),
            Attendance.check_out.is_(None),
        )
        .order_by(Attendance.id.asc())
        .all()
    )

    for row in rows:
        row.check_out = auto_checkout_dt
        row.notes = (
            f"{row.notes}\nAuto checkout pada {auto_close_time.strftime('%H:%M')}"
            if row.notes
            else f"Auto checkout pada {auto_close_time.strftime('%H:%M')}"
        )

    if rows:
        db.session.commit()

    return len(rows)


def check_in(user, lat: float, lng: float):
    setting = get_effective_setting()
    now = now_in_tz(setting.timezone)
    today = now.date()

    if now.time() < setting.check_in_time:
        return False, "Absensi masuk belum dibuka"

    existing = Attendance.query.filter_by(user_id=user.id, date=today).first()
    if existing and existing.check_in:
        return False, "Anda sudah melakukan check-in hari ini"

    tolerance = float(current_app.config.get("LOCATION_TOLERANCE_METERS", 0))
    zone, distance = resolve_zone_and_distance(lat, lng, tolerance)
    if not zone:
        if distance is not None:
            return False, f"Lokasi di luar zona absensi. Jarak terdekat: {distance:.1f} m"
        return False, "Lokasi di luar zona absensi"

    late_limit = datetime.combine(today, setting.check_in_time) + timedelta(
        minutes=setting.late_tolerance_minutes
    )
    status = "HADIR" if now.replace(tzinfo=None) <= late_limit else "TERLAMBAT"

    attendance = existing or Attendance(user_id=user.id, date=today)
    attendance.zone_id = zone.id
    attendance.check_in = now.replace(tzinfo=None)
    attendance.check_in_latitude = lat
    attendance.check_in_longitude = lng
    attendance.check_in_distance = distance
    attendance.status = status

    db.session.add(attendance)
    db.session.commit()
    return True, f"Check-in berhasil dengan status {status}"


def check_out(user, lat: float, lng: float):
    setting = get_effective_setting()
    now = now_in_tz(setting.timezone)
    today = now.date()

    attendance = Attendance.query.filter_by(user_id=user.id, date=today).first()
    if not attendance or not attendance.check_in:
        return False, "Anda belum check-in hari ini"

    if attendance.check_out:
        return False, "Anda sudah check-out hari ini"

    can_early = can_checkout_early(user.id, today, now.time())
    if now.time() < setting.check_out_time and not can_early:
        return False, "Absensi pulang belum dibuka"

    tolerance = float(current_app.config.get("LOCATION_TOLERANCE_METERS", 0))
    zone, distance = resolve_zone_and_distance(lat, lng, tolerance)

    attendance.check_out = now.replace(tzinfo=None)
    attendance.check_out_latitude = lat
    attendance.check_out_longitude = lng
    attendance.check_out_distance = distance
    if zone and not attendance.zone_id:
        attendance.zone_id = zone.id
    if can_early:
        attendance.status = "PULANG_CEPAT"

    db.session.add(attendance)
    db.session.commit()
    return True, "Check-out berhasil"
