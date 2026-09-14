# Sistem Absensi PKL / Magang (Flask + MySQL)

Implementasi MVP berdasarkan PRD di folder [prd](prd), menggunakan:
- Backend: Flask
- Database: MySQL (SQLAlchemy + PyMySQL)
- Auth: Session login + Role-based access (Admin, Staff, Intern)

## Fitur Utama MVP

- Authentication login/logout
- RBAC dashboard per role:
	- Admin: kelola user, zona geofence, pengaturan jam absensi, laporan
	- Staff: monitoring absensi, approval izin
	- Intern: check-in/check-out, histori, pengajuan izin
- Geofencing backend validation (haversine distance)
- Validasi waktu absensi berbasis timezone server (default Asia/Makassar)
- Pengaturan jam masuk, jam pulang, toleransi terlambat dari database
- Status absensi: HADIR, TERLAMBAT, SAKIT, PULANG_CEPAT, ALPHA, BELUM_ABSEN
- Soft delete user
- Export laporan CSV

## Struktur Project

- [app](app)
	- [app/auth/routes.py](app/auth/routes.py)
	- [app/admin/routes.py](app/admin/routes.py)
	- [app/staff/routes.py](app/staff/routes.py)
	- [app/intern/routes.py](app/intern/routes.py)
	- [app/models.py](app/models.py)
	- [app/utils/attendance_service.py](app/utils/attendance_service.py)
- [run.py](run.py)
- [requirements.txt](requirements.txt)

## Setup Lokal

1. Buat virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependency

```bash
pip install -r requirements.txt
```

3. Siapkan environment file

```bash
cp .env.example .env
```

4. Edit koneksi MySQL pada [ .env.example ](.env.example) yang disalin ke .env, contoh:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/intern_attendance
```

5. Buat database MySQL:

```sql
CREATE DATABASE intern_attendance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. Inisialisasi tabel dan seed default

```bash
flask --app run.py init-db
```

7. Jalankan aplikasi

```bash
flask --app run.py run --debug
```

## Buat Admin Manual (Terminal)

Setelah init database, buat akun admin manual lewat terminal:

```bash
flask --app run.py create-admin \
	--name "Super Admin" \
	--email admin@example.com \
	--username admin \
	--password admin123
```

## Scheduler Alpha

Untuk menandai peserta ALPHA (tanpa attendance dan tanpa izin approved), jalankan:

```bash
flask --app run.py mark-alpha
```

Perintah ini bisa dijadwalkan via cron.

## Catatan

- Lampiran izin (upload file), export Excel/PDF, notifikasi real-time, dan audit log detail masih bisa dilanjutkan ke fase berikutnya.
- Frontend saat ini server-rendered Jinja agar MVP cepat dipakai dan mudah dikembangkan.