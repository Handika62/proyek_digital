# 🛠️ Sistem Layanan Digital (Service Management System)

Aplikasi manajemen layanan berbasis CLI (Command Line Interface) yang dirancang untuk mengelola antrean jasa, mulai dari pendaftaran pelanggan hingga pelaporan status pengerjaan.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?style=for-the-badge&logo=sqlite)
![Termux](https://img.shields.io/badge/Platform-Termux-orange?style=for-the-badge&logo=termux)

## 🚀 Fitur Utama
- **Manajemen Order (CRUD):** Tambah, Lihat, Update, dan Hapus data pelanggan.
- **Pelacakan Status:** Pantau progres pekerjaan (Pending, Diproses, Selesai).
- **Laporan Otomatis:** Ringkasan statistik jumlah pesanan berdasarkan status.
- **Database Permanen:** Menggunakan SQLite untuk penyimpanan data yang ringan dan aman.

## 📁 Struktur Proyek
```text
proyek_digital/
├── data/           # Penyimpanan database (layanan.db)
├── docs/           # Dokumentasi & SOP Operasional
├── src/            # Kode sumber (Logic & Database)
└── README.md       # Panduan Utama
