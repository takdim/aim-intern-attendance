from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Role(TimestampMixin, db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    identity_number = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    institution = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(120), nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    role = db.relationship("Role", backref="users")
    internship = db.relationship("Internship", backref="user", uselist=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name: str) -> bool:
        return self.role is not None and self.role.name == role_name


class Internship(TimestampMixin, db.Model):
    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    division = db.Column(db.String(120), nullable=True)
    supervisor = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), nullable=False, default="ACTIVE")


class Zone(TimestampMixin, db.Model):
    __tablename__ = "zones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class AttendanceSetting(TimestampMixin, db.Model):
    __tablename__ = "attendance_settings"

    id = db.Column(db.Integer, primary_key=True)
    check_in_time = db.Column(db.Time, nullable=False)
    check_out_time = db.Column(db.Time, nullable=False)
    late_tolerance_minutes = db.Column(db.Integer, nullable=False, default=15)
    timezone = db.Column(db.String(64), nullable=False, default="Asia/Makassar")

    @staticmethod
    def get_active():
        return AttendanceSetting.query.order_by(AttendanceSetting.id.desc()).first()


class Attendance(TimestampMixin, db.Model):
    __tablename__ = "attendance"
    __table_args__ = (db.UniqueConstraint("user_id", "date", name="uniq_user_date"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey("zones.id"), nullable=True)

    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)

    check_in_latitude = db.Column(db.Float, nullable=True)
    check_in_longitude = db.Column(db.Float, nullable=True)
    check_in_distance = db.Column(db.Float, nullable=True)

    check_out_latitude = db.Column(db.Float, nullable=True)
    check_out_longitude = db.Column(db.Float, nullable=True)
    check_out_distance = db.Column(db.Float, nullable=True)

    status = db.Column(db.String(30), nullable=False, default="BELUM_ABSEN")
    notes = db.Column(db.Text, nullable=True)

    user = db.relationship("User", backref="attendances")
    zone = db.relationship("Zone", backref="attendances")


class LeaveRequest(TimestampMixin, db.Model):
    __tablename__ = "leave_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    request_type = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    planned_checkout = db.Column(db.Time, nullable=True)

    reason = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255), nullable=True)

    status = db.Column(db.String(20), nullable=False, default="PENDING")
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    review_notes = db.Column(db.Text, nullable=True)

    user = db.relationship("User", foreign_keys=[user_id], backref="leave_requests")
    reviewer = db.relationship("User", foreign_keys=[reviewed_by])


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notif_type = db.Column(db.String(30), nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    actor_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(120), nullable=False)
    entity = db.Column(db.String(120), nullable=False)
    entity_id = db.Column(db.Integer, nullable=True)
    metadata_json = db.Column("metadata", db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
