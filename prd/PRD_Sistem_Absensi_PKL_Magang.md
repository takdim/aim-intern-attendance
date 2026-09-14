# Product Requirements Document (PRD)
# Sistem Absensi PKL / Magang

**Nama Produk:** Sistem Absensi PKL/Magang  
**Platform:** Web Responsive  
**Target Perangkat:** Desktop, Laptop, Tablet, Smartphone  
**Zona Waktu:** WITA (UTC+8)  
**Lokasi Utama:** Makassar, Sulawesi Selatan, Indonesia  
**Versi:** 1.0

---

## 1. Product Overview

Sistem Absensi PKL/Magang adalah aplikasi web responsive yang digunakan untuk mengelola kehadiran peserta Praktik Kerja Lapangan (PKL), magang, atau internship secara digital.

Sistem memungkinkan peserta melakukan absensi masuk dan pulang berdasarkan:

- Waktu yang telah ditentukan.
- Lokasi/geofence yang telah ditetapkan.
- Status kehadiran.
- Pengajuan izin sakit.
- Pengajuan izin pulang cepat.

Selain peserta PKL/Magang, sistem memiliki role **Admin** dan **Staff** yang bertanggung jawab terhadap pengelolaan pengguna, monitoring kehadiran, pengajuan izin, dan pembuatan laporan.

---

## 2. Problem Statement

Proses absensi peserta PKL/Magang secara manual memiliki beberapa permasalahan:

1. Absensi menggunakan kertas atau spreadsheet membutuhkan proses administrasi tambahan.
2. Sulit memastikan peserta melakukan absensi dari lokasi PKL yang sebenarnya.
3. Rekap kehadiran harus dilakukan secara manual.
4. Data keterlambatan sulit dimonitor secara real-time.
5. Pengajuan izin sakit atau pulang cepat belum terdokumentasi secara terstruktur.
6. Staff membutuhkan waktu lebih lama untuk membuat laporan kehadiran.
7. Admin membutuhkan sistem terpusat untuk mengelola data peserta PKL/Magang.

Sistem ini dibuat untuk mengotomatisasi proses tersebut.

---

## 3. Goals

### 3.1 Primary Goals

- Menyediakan sistem absensi PKL/Magang berbasis web.
- Memastikan absensi hanya dapat dilakukan pada waktu yang ditentukan.
- Memastikan absensi hanya dapat dilakukan di lokasi yang diizinkan.
- Memudahkan staff memonitor kehadiran peserta.
- Memudahkan pengelolaan izin.
- Menyediakan rekap kehadiran secara otomatis.
- Menyediakan laporan yang dapat digunakan untuk kebutuhan administrasi.

### 3.2 Secondary Goals

- Mengurangi penggunaan dokumen absensi manual.
- Mengurangi kesalahan pencatatan.
- Menyediakan histori absensi setiap peserta.
- Menyediakan informasi keterlambatan dan ketidakhadiran.

---

## 4. User Roles

| Role | Deskripsi |
|---|---|
| Admin | Mengelola sistem dan seluruh data pengguna |
| Staff | Mengelola dan memonitor absensi serta laporan |
| PKL/Magang | Melakukan absensi dan mengajukan izin |

---

## 5. Role & Permission

### 5.1 Admin

Admin memiliki akses penuh terhadap sistem.

#### Fitur Admin

- Login
- Dashboard
- CRUD User
- CRUD Peserta PKL/Magang
- CRUD Staff
- Mengaktifkan/nonaktifkan user
- Reset password user
- Mengatur periode PKL/Magang
- Mengatur lokasi/zona absensi
- Mengatur radius zona
- Mengatur jam absensi
- Melihat seluruh data absensi
- Melihat pengajuan izin
- Melihat laporan
- Export laporan

#### CRUD User

**Create**
- Nama
- Username/email
- Password
- Role
- Nomor identitas
- Nomor telepon
- Instansi/sekolah/universitas
- Program studi
- Divisi
- Periode PKL
- Status

**Read**
- Melihat daftar user
- Melihat detail user
- Melihat histori aktivitas

**Update**
- Mengubah data user
- Mengubah role
- Mengubah status
- Mengubah periode PKL

**Delete**
- Menghapus user

> **Catatan:** Penghapusan user sebaiknya menggunakan **soft delete** agar histori absensi tidak ikut hilang.

---

## 6. Staff

Staff berfokus pada operasional kehadiran peserta.

### 6.1 Staff dapat

- Login
- Melihat dashboard
- Melihat daftar peserta PKL/Magang
- Melihat absensi hari ini
- Melihat peserta yang belum absen
- Melihat peserta terlambat
- Melihat peserta tidak hadir
- Melihat pengajuan izin
- Approve/reject izin
- Melihat rekap kehadiran
- Filter laporan
- Export laporan

Staff tidak dapat menghapus atau mengubah akun user kecuali permission tersebut diberikan oleh Admin.

---

## 7. PKL / Magang

Peserta merupakan pengguna yang melakukan absensi.

### 7.1 Fitur Peserta

- Login
- Dashboard
- Absensi masuk
- Absensi pulang
- Melihat status absensi hari ini
- Melihat histori absensi
- Mengajukan izin sakit
- Mengajukan izin pulang cepat
- Melihat status pengajuan izin
- Melihat profil

---

## 8. Attendance System

### 8.1 Absensi Masuk

Jam absensi masuk:

> **07.30 WITA**

Peserta dapat melakukan absensi mulai pukul **07.30 WITA**.

### Status Kehadiran

| Waktu Absensi | Status |
|---|---|
| 07.30 | Hadir |
| 07.45 | Hadir |
| 08.00 | Terlambat |
| 08.30 | Terlambat |

Sebaiknya sistem memiliki konfigurasi **grace period/toleransi keterlambatan**.

Contoh:

- Jam masuk: 07.30 WITA
- Toleransi: 15 menit
- Sampai 07.45 → Hadir
- Setelah 07.45 → Terlambat

Nilai toleransi dapat diubah oleh Admin.

---

## 9. Absensi Pulang

Jam absensi pulang:

> **16.00 WITA**

Peserta dapat melakukan absensi pulang mulai pukul **16.00 WITA**.

### Contoh

| Waktu | Status |
|---|---|
| 15.30 | Tidak dapat absen |
| 15.59 | Tidak dapat absen |
| 16.00 | Dapat absen |
| 16.30 | Dapat absen |
| 17.00 | Dapat absen |

Jika peserta perlu pulang sebelum pukul 16.00, peserta harus menggunakan fitur **Izin Pulang Cepat**.

---

## 10. Daily Attendance Flow

### 10.1 Check-in

```text
Peserta Login
      ↓
Buka halaman Absensi
      ↓
Sistem meminta lokasi
      ↓
Validasi lokasi
      ↓
Validasi waktu
      ↓
Validasi apakah sudah absen
      ↓
Ambil data lokasi
      ↓
Simpan absensi
      ↓
Status = HADIR / TERLAMBAT
```

### 10.2 Check-out

```text
Peserta Login
      ↓
Buka halaman Absensi
      ↓
Validasi lokasi
      ↓
Validasi waktu >= 16.00
      ↓
Validasi sudah absen masuk
      ↓
Simpan absensi pulang
```

---

## 11. Location Zone / Geofencing

Geofencing merupakan fitur utama sistem.

Admin dapat menentukan lokasi yang diperbolehkan untuk melakukan absensi.

Contoh:

```text
Nama Zona   : Kantor Utama
Latitude    : -5.xxxxx
Longitude   : 119.xxxxx
Radius      : 100 meter
Status      : Aktif
```

Peserta hanya dapat melakukan absensi apabila berada dalam radius zona yang telah ditentukan.

### 11.1 Konsep

```text
                Zona Absensi
             ┌─────────────────┐
             │                 │
             │      OFFICE     │
             │        ●        │
             │                 │
             └─────────────────┘
                   Radius
                  100 meter

             ● = titik lokasi
```

Jika:

```text
Distance <= Radius
```

maka:

```text
VALID
↓
Peserta dapat melakukan absensi
```

Jika:

```text
Distance > Radius
```

maka:

```text
INVALID
↓
Absensi ditolak
```

---

## 12. Location Configuration

Admin dapat membuat satu atau beberapa zona absensi.

### 12.1 Data Zona

- Nama zona
- Deskripsi
- Latitude
- Longitude
- Radius
- Status aktif/nonaktif

### Contoh

| Zona | Radius | Status |
|---|---:|---|
| Kantor Utama | 100 m | Aktif |
| Gedung Fakultas | 150 m | Aktif |
| Cabang A | 100 m | Nonaktif |

Hal ini memungkinkan sistem digunakan pada organisasi yang memiliki beberapa lokasi.

---

## 13. Location Validation

Ketika peserta menekan tombol **Absen**, sistem melakukan:

1. Request GPS/browser location.
2. Mendapatkan latitude.
3. Mendapatkan longitude.
4. Menghitung jarak dari lokasi peserta ke lokasi zona.
5. Membandingkan jarak dengan radius.
6. Jika valid, absensi diproses.
7. Jika tidak valid, absensi ditolak.

Contoh:

```text
Lokasi Peserta
Latitude  : -5.123456
Longitude : 119.123456

Zona Kantor
Latitude  : -5.123400
Longitude : 119.123400

Jarak
↓
42 meter

Radius Zona
↓
100 meter

42 <= 100
↓
ABSENSI VALID
```

---

## 14. Browser Location Permission

Karena sistem berbasis web, lokasi menggunakan **Geolocation API pada browser**.

Pada smartphone, browser akan meminta permission:

```text
Allow this website to access your location?
```

Peserta harus memberikan izin lokasi.

Jika peserta menolak permission lokasi:

```text
Absensi tidak dapat dilakukan.
```

---

## 15. Attendance Data

Setiap absensi menyimpan data:

- ID absensi
- User ID
- Tanggal
- Waktu masuk
- Waktu pulang
- Status
- Latitude masuk
- Longitude masuk
- Latitude pulang
- Longitude pulang
- Jarak dari zona saat masuk
- Jarak dari zona saat pulang
- Zona yang digunakan
- Catatan
- Created At
- Updated At

### Contoh

```text
Tanggal       : 14 September 2026
Nama          : Ahmad
Jam Masuk     : 07:42
Jam Pulang    : 16:08
Status        : Hadir
Zona          : Kantor Utama
Jarak         : 43 meter
```

---

## 16. Attendance Status

Status minimal:

- `HADIR`
- `TERLAMBAT`
- `IZIN`
- `SAKIT`
- `PULANG_CEPAT`
- `ALPHA`
- `BELUM_ABSEN`

### Contoh

| Nama | Masuk | Pulang | Status |
|---|---:|---:|---|
| Ahmad | 07:35 | 16:10 | Hadir |
| Budi | 08:02 | 16:05 | Terlambat |
| Citra | - | - | Sakit |
| Deni | 07:40 | 14:30 | Pulang Cepat |
| Eka | - | - | Alpha |

---

## 17. Izin Sakit

Peserta dapat mengajukan izin sakit.

### 17.1 Form Izin Sakit

Field:

- Jenis izin
- Tanggal mulai
- Tanggal selesai
- Alasan
- Lampiran surat/dokumen jika diperlukan
- Catatan tambahan

### 17.2 Status

```text
PENDING
   ↓
Staff Review
   ↓
APPROVED / REJECTED
```

Jika disetujui:

```text
Attendance = SAKIT
```

---

## 18. Izin Pulang Cepat

Peserta dapat mengajukan izin untuk pulang sebelum pukul 16.00 WITA.

### 18.1 Form

- Tanggal
- Jam pulang yang direncanakan
- Alasan
- Keterangan
- Lampiran jika diperlukan

### Contoh

```text
Jenis       : Pulang Cepat
Tanggal     : 14 September 2026
Jam Pulang  : 14.00
Alasan      : Keperluan keluarga
Status      : Pending
```

Staff kemudian melakukan approval.

---

## 19. Approval System

Status pengajuan:

```text
PENDING
   │
   ├── APPROVED
   │
   └── REJECTED
```

Staff dapat memberikan:

- Approve
- Reject
- Catatan approval

Contoh:

```text
Approved by : Staff
Tanggal     : 14 September 2026
Waktu       : 10:32 WITA
```

---

## 20. Dashboard Admin

Dashboard Admin menampilkan informasi sistem secara keseluruhan.

### 20.1 Summary Cards

```text
┌────────────┐ ┌──────────────┐ ┌────────────┐ ┌────────────┐
│ Total User │ │ Peserta PKL  │ │ Staff      │ │ Admin      │
│    120     │ │      95      │ │     23     │ │      2     │
└────────────┘ └──────────────┘ └────────────┘ └────────────┘
```

### 20.2 Informasi

- Total peserta aktif.
- Absensi hari ini.
- Peserta terlambat.
- Peserta izin.
- Peserta sakit.
- Peserta alpha.
- Pengajuan izin pending.

---

## 21. Dashboard Staff

Dashboard Staff berfokus pada operasional kehadiran.

Contoh:

```text
Total Peserta       95

Sudah Absen         83
Belum Absen         12
Terlambat             7
Izin                  3
Sakit                 2
```

### 21.1 Absensi Hari Ini

| Peserta | Masuk | Pulang | Status |
|---|---:|---:|---|
| Ahmad | 07:32 | - | Hadir |
| Budi | 08:02 | - | Terlambat |
| Citra | - | - | Sakit |

---

## 22. Dashboard Peserta

Dashboard peserta dibuat sederhana dan fokus pada absensi.

Contoh:

```text
Selamat pagi, Ahmad

Senin, 14 September 2026

┌─────────────────────────┐
│ Status Hari Ini         │
│                         │
│ Hadir                   │
│ Masuk: 07:35            │
│ Pulang: Belum           │
└─────────────────────────┘

       [ ABSEN PULANG ]
```

### 22.1 Sebelum Jam Masuk

Jika waktu masih sebelum 07.30:

```text
Absensi masuk belum dibuka.
Absensi dibuka pukul 07.30 WITA.
```

### 22.2 Sebelum Jam Pulang

Jika waktu masih sebelum 16.00:

```text
Absensi pulang belum dibuka.
Absensi dibuka pukul 16.00 WITA.
```

---

## 23. Attendance History

Peserta dapat melihat histori absensi miliknya.

### 23.1 Filter

- Bulan
- Tahun
- Status

### Contoh

| Tanggal | Masuk | Pulang | Status |
|---|---:|---:|---|
| 01 Sep | 07:35 | 16:10 | Hadir |
| 02 Sep | 07:55 | 16:02 | Hadir |
| 03 Sep | - | - | Sakit |
| 04 Sep | 08:10 | 16:05 | Terlambat |

---

## 24. Reporting

Admin dan Staff dapat membuat laporan kehadiran.

### 24.1 Filter

- Periode tanggal
- Bulan
- Tahun
- Peserta
- Divisi
- Instansi
- Status kehadiran

### 24.2 Export

Laporan dapat diekspor menjadi:

- Excel
- CSV
- PDF

### Contoh

```text
LAPORAN KEHADIRAN PESERTA PKL

Periode:
01 September 2026 - 30 September 2026

Nama        : Ahmad
Instansi    : Universitas ABC
Divisi      : IT

Hadir       : 20
Terlambat   : 3
Sakit       : 1
Izin        : 1
Alpha       : 0
```

---

## 25. Rekap Kehadiran

Sistem otomatis menghitung:

```text
Total Hari Kerja
Total Hadir
Total Terlambat
Total Sakit
Total Izin
Total Pulang Cepat
Total Alpha
```

### 25.1 Persentase Kehadiran

```text
Persentase Kehadiran =
Hari Hadir / Total Hari Kerja × 100%
```

---

## 26. Notification

Sistem dapat memberikan notifikasi.

### 26.1 Peserta

- Absensi masuk berhasil.
- Absensi pulang berhasil.
- Pengajuan izin diterima.
- Pengajuan izin ditolak.
- Absensi gagal karena lokasi.
- Absensi belum dibuka.

### 26.2 Staff

- Pengajuan izin baru.
- Peserta terlambat.
- Peserta belum melakukan absensi.

---

## 27. Authentication

Sistem menggunakan authentication untuk seluruh user.

### 27.1 Login Flow

```text
Email / Username
       +
Password
       ↓
Authentication
       ↓
Role Checking
       ↓
Dashboard
```

Role menentukan dashboard dan permission.

Contoh route:

```text
/admin/dashboard
/staff/dashboard
/intern/dashboard
```

---

## 28. Responsive Design

Sistem harus dapat digunakan pada:

- Desktop
- Laptop
- Tablet
- Smartphone

### 28.1 Desktop

```text
┌──────────┬───────────────────────────┐
│ Sidebar  │ Dashboard                 │
│          │                           │
│ Dashboard│ Cards                     │
│ Users    │                           │
│ Absensi  │ Attendance Table          │
│ Reports  │                           │
└──────────┴───────────────────────────┘
```

### 28.2 Mobile

Sidebar berubah menjadi:

```text
☰
```

atau menggunakan bottom navigation.

Fungsi utama peserta harus dapat dilakukan melalui smartphone.

---

## 29. Sitemap

### 29.1 Public

```text
/login
```

### 29.2 Admin

```text
/admin/dashboard
/admin/users
/admin/users/create
/admin/users/:id
/admin/attendance
/admin/zones
/admin/reports
/admin/settings
```

### 29.3 Staff

```text
/staff/dashboard
/staff/attendance
/staff/leave-requests
/staff/reports
```

### 29.4 PKL/Magang

```text
/intern/dashboard
/intern/attendance
/intern/history
/intern/leave
/intern/profile
```

---

## 30. Database Design

Minimal tabel yang disarankan:

```text
users
roles
internships
attendance
zones
leave_requests
leave_types
notifications
```

---

## 31. Database Schema

### 31.1 users

```text
id
name
email
password
role_id
phone
institution
department
status
created_at
updated_at
deleted_at
```

### 31.2 roles

```text
id
name
created_at
updated_at
```

Contoh:

```text
ADMIN
STAFF
INTERN
```

### 31.3 internships

```text
id
user_id
start_date
end_date
division
supervisor
status
created_at
updated_at
```

### 31.4 zones

```text
id
name
latitude
longitude
radius
description
status
created_at
updated_at
```

### 31.5 attendance

```text
id
user_id
date
check_in
check_out

check_in_latitude
check_in_longitude
check_in_distance

check_out_latitude
check_out_longitude
check_out_distance

zone_id
status
notes

created_at
updated_at
```

### 31.6 leave_requests

```text
id
user_id
type
start_date
end_date
planned_checkout
reason
attachment

status

reviewed_by
reviewed_at
review_notes

created_at
updated_at
```

### 31.7 notifications

```text
id
user_id
title
message
type
is_read
created_at
```

---

## 32. Business Rules

### Rule 1 — Timezone

Semua proses waktu absensi menggunakan:

```text
Asia/Makassar
UTC+8
```

Timezone harus ditentukan pada sisi server/backend.

Jangan hanya mengandalkan timezone perangkat pengguna.

---

### Rule 2 — Check-in

Check-in dibuka:

```text
07:30 WITA
```

Sebelum 07.30:

```text
DENIED
```

Mulai 07.30:

```text
ALLOWED
```

---

### Rule 3 — Check-out

Check-out dibuka:

```text
16:00 WITA
```

Sebelum 16.00:

```text
DENIED
```

Mulai 16.00:

```text
ALLOWED
```

Kecuali peserta memiliki izin pulang cepat yang telah disetujui.

---

### Rule 4 — Location

Peserta hanya dapat melakukan absensi jika:

```text
distance <= zone.radius
```

---

### Rule 5 — Check-in wajib sebelum Check-out

Peserta tidak dapat melakukan check-out apabila belum memiliki check-in pada hari tersebut.

---

### Rule 6 — Satu Absensi per Hari

Peserta hanya mempunyai satu record attendance untuk satu tanggal.

Constraint database:

```text
UNIQUE(user_id, date)
```

---

### Rule 7 — Sakit

Jika izin sakit disetujui:

```text
Attendance = SAKIT
```

Peserta tidak perlu melakukan check-in/check-out.

---

### Rule 8 — Pulang Cepat

Jika izin pulang cepat disetujui:

```text
planned_checkout < 16:00
```

Peserta dapat melakukan checkout sebelum pukul 16.00 sesuai izin.

---

### Rule 9 — Alpha

Jika hari kerja telah selesai dan:

```text
tidak ada attendance
AND
tidak ada izin approved
```

maka:

```text
status = ALPHA
```

Proses ini dapat dijalankan menggunakan scheduled job/cron.

---

## 33. Security Requirements

Sistem harus memperhatikan keamanan berikut:

- Password harus disimpan menggunakan password hashing.
- Authentication menggunakan session/token yang aman.
- Role-Based Access Control (RBAC).
- Validasi input.
- CSRF protection jika menggunakan session-based authentication.
- Rate limiting pada login.
- Audit log untuk aktivitas penting.
- Validasi file upload.
- Pembatasan ukuran attachment.
- Validasi lokasi pada backend.
- Validasi timestamp menggunakan server time.

### Location Security

Frontend tidak boleh menjadi satu-satunya sumber validasi lokasi.

Backend harus melakukan validasi:

```text
Latitude
Longitude
Timestamp
Zone
Radius
```

sebelum membuat record absensi.

---

## 34. Anti-Fraud / Anti-Abuse

### 34.1 MVP

Untuk versi awal sistem menggunakan:

- GPS browser.
- Geofencing.
- Server timestamp.
- User authentication.
- Backend location validation.

### 34.2 Advanced

Fitur tambahan yang dapat dikembangkan:

- Foto selfie saat absensi.
- Face verification.
- Device fingerprint.
- IP logging.
- GPS accuracy validation.
- Deteksi mock location pada mobile application.
- Audit log.

Untuk MVP, face recognition tidak wajib.

---

## 35. MVP Scope

Versi pertama sistem harus berfokus pada fitur inti.

### Admin

- Login.
- Dashboard.
- CRUD user.
- CRUD peserta.
- CRUD zona.
- Pengaturan jam absensi.
- Pengaturan radius lokasi.

### Staff

- Dashboard.
- Monitoring absensi.
- Approval izin.
- Rekap kehadiran.
- Export laporan.

### Peserta

- Login.
- Check-in.
- Check-out.
- GPS validation.
- Histori absensi.
- Izin sakit.
- Izin pulang cepat.

### System

- Authentication.
- Role management.
- Geofencing.
- Timezone Asia/Makassar.
- Attendance calculation.
- Responsive UI.

---

## 36. Future Development

### Phase 2

- QR Code.
- Selfie attendance.
- Notification.
- Email notification.
- Dashboard analytics.
- PDF report dengan template resmi.

### Phase 3

- Mobile application.
- Push notification.
- Face recognition.
- Device verification.
- Multiple branch/location.
- Supervisor PKL.
- Penilaian peserta PKL.
- Jurnal kegiatan harian.

---

## 37. Success Metrics

Sistem dianggap berhasil jika:

| Metric | Target |
|---|---:|
| Keberhasilan absensi | >= 95% |
| Validasi lokasi | >= 95% |
| Pengurangan pekerjaan rekap manual | >= 80% |
| Waktu membuat laporan | < 1 menit |
| Mobile responsive | 100% fungsi utama |
| Duplikasi absensi | 0 |
| Absensi di luar zona | 0 |

---

## 38. User Flow

```text
                    ABSENSI PKL/MAGANG
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
       ADMIN              STAFF             PESERTA
        │                  │                  │
        │                  │                  │
   User Management    Attendance          Check-in
   Zone Management    Monitoring          Check-out
   System Setting     Leave Approval       Leave Request
   Reports            Reports             History
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                      BACKEND API
                           │
              ┌────────────┴────────────┐
              │                         │
          Database                Location
                                  Validation
              │                         │
              └────────────┬────────────┘
                           │
                    Attendance Data
```

---

## 39. Acceptance Criteria

### 39.1 Check-in Berhasil

**Given:**  
Peserta sudah login.

**When:**  
Waktu sudah 07.30 WITA dan peserta berada di dalam zona.

**Then:**  
Peserta dapat melakukan check-in.

---

### 39.2 Check-in Terlalu Awal

**Given:**  
Waktu masih 07.20 WITA.

**When:**  
Peserta menekan tombol check-in.

**Then:**  
Sistem menolak absensi.

---

### 39.3 Check-in di Luar Zona

**Given:**  
Waktu sudah 07.30 WITA.

**When:**  
Peserta berada 500 meter dari kantor dan radius zona adalah 100 meter.

**Then:**  
Sistem menolak absensi.

---

### 39.4 Check-out Berhasil

**Given:**  
Peserta sudah melakukan check-in.

**When:**  
Waktu sudah 16.00 WITA dan lokasi valid.

**Then:**  
Peserta dapat melakukan check-out.

---

### 39.5 Check-out Sebelum 16.00

**Given:**  
Peserta tidak memiliki izin pulang cepat.

**When:**  
Peserta mencoba check-out pukul 15.00.

**Then:**  
Sistem menolak check-out.

---

### 39.6 Pulang Cepat

**Given:**  
Peserta memiliki izin pulang cepat yang sudah approved.

**When:**  
Peserta melakukan check-out pada waktu yang diizinkan.

**Then:**  
Sistem menerima check-out.

---

### 39.7 Sakit

**Given:**  
Peserta mengajukan izin sakit.

**When:**  
Staff melakukan approval.

**Then:**  
Status attendance menjadi `SAKIT`.

---

### 39.8 Lokasi Tidak Diizinkan

**Given:**  
Peserta berada di luar radius zona.

**When:**  
Peserta mencoba melakukan absensi.

**Then:**  
Sistem menolak absensi dan menampilkan informasi bahwa peserta berada di luar zona absensi.

---

## 40. Technical Recommendation

Arsitektur yang direkomendasikan:

```text
Frontend
   │
   ▼
React / Next.js
   │
   ▼
REST API
   │
   ▼
Backend
   │
   ▼
Flask / FastAPI
   │
   ▼
MySQL / PostgreSQL
```

Alternatif yang lebih sederhana:

```text
React
   │
   ▼
Flask REST API
   │
   ▼
MySQL
```

Stack kedua cocok untuk MVP karena arsitekturnya relatif sederhana dan mudah dikembangkan.

---

## 41. Recommended System Architecture

```text
                 ┌─────────────────────┐
                 │      Web Client     │
                 │                     │
                 │ Desktop / Mobile    │
                 └──────────┬──────────┘
                            │
                            │ HTTPS
                            ▼
                 ┌─────────────────────┐
                 │      Frontend       │
                 │ React / Next.js     │
                 └──────────┬──────────┘
                            │
                            │ REST API
                            ▼
                 ┌─────────────────────┐
                 │       Backend       │
                 │ Flask / FastAPI     │
                 └───────┬─────┬───────┘
                         │     │
               ┌─────────┘     └──────────┐
               ▼                          ▼
      ┌─────────────────┐        ┌─────────────────┐
      │    Database     │        │ Location Service│
      │ MySQL/PostgreSQL│        │   Geofencing    │
      └─────────────────┘        └─────────────────┘
```

---

## 42. Important Configuration

Jam absensi **tidak sebaiknya hard-coded di source code**.

Simpan konfigurasi dalam database.

Contoh:

```text
attendance_settings

id
check_in_time
check_out_time
late_tolerance
timezone
created_at
updated_at
```

Default:

```text
check_in_time  = 07:30
check_out_time = 16:00
timezone       = Asia/Makassar
late_tolerance = 15 minutes
```

Dengan demikian Admin dapat mengubah jam absensi tanpa perlu mengubah source code aplikasi.

---

## 43. Final MVP Definition

MVP dianggap selesai apabila peserta dapat:

```text
LOGIN
  ↓
MELIHAT STATUS ABSENSI
  ↓
MENGAKSES GPS
  ↓
VALIDASI WAKTU
  ↓
VALIDASI ZONA
  ↓
CHECK-IN
  ↓
CHECK-OUT
```

Staff dapat:

```text
LOGIN
  ↓
MELIHAT ABSENSI PESERTA
  ↓
MELIHAT PESERTA TERLAMBAT
  ↓
MENGELOLA IZIN
  ↓
MELIHAT REKAP
  ↓
EXPORT LAPORAN
```

Admin dapat:

```text
LOGIN
  ↓
MANAGE USER
  ↓
MANAGE ZONE
  ↓
MANAGE SETTINGS
  ↓
MONITOR ABSENSI
  ↓
MANAGE REPORT
```

---

## 44. Conclusion

Sistem Absensi PKL/Magang dirancang sebagai aplikasi web responsive yang memusatkan proses absensi, pengelolaan izin, monitoring kehadiran, dan pembuatan laporan.

Fitur utama sistem:

1. **Role-based access** untuk Admin, Staff, dan Peserta.
2. **Check-in mulai 07.30 WITA.**
3. **Check-out mulai 16.00 WITA.**
4. **Geofencing** berdasarkan lokasi yang dikonfigurasi Admin.
5. **Izin sakit.**
6. **Izin pulang cepat.**
7. **Approval Staff.**
8. **Rekap otomatis.**
9. **Export laporan.**
10. **Responsive design.**
11. **Timezone Asia/Makassar.**
12. **Server-side validation untuk waktu dan lokasi.**

Sistem dapat dikembangkan lebih lanjut menjadi platform manajemen PKL/Magang yang mencakup absensi, jurnal kegiatan, monitoring pembimbing, penilaian, hingga pembuatan laporan akhir PKL.
