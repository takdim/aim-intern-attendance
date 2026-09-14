import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/intern_attendance"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
    LOCATION_TOLERANCE_METERS = float(os.getenv("LOCATION_TOLERANCE_METERS", "15"))
