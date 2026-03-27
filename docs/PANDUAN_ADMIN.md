# Panduan Operasional Sistem Layanan Digital
Versi: 1.0 (Maret 2026)

## 1. Persiapan Awal
Sebelum menjalankan sistem, pastikan Anda berada di direktori proyek dan Virtual Environment aktif:
- Perintah: `cd ~/proyek_digital`
- Perintah: `source venv/bin/activate`

## 2. Cara Menjalankan Aplikasi
Jalankan file utama menggunakan Python:
- Perintah: `python src/main.py`

## 3. Alur Kerja (SOP)
### A. Pendaftaran Pesanan Baru
1. Pilih menu [1].
2. Masukkan Nama Pelanggan (Contoh: "Budi Santoso").
3. Masukkan Jenis Layanan (Contoh: "Servis Pompa Air" atau "Cuci AC").
4. Sistem akan otomatis memberikan status "Pending".

### B. Pemantauan & Update Status
1. Gunakan menu [2] untuk melihat daftar antrean.
2. Gunakan menu [3] jika pekerjaan sudah mulai dikerjakan atau selesai.
3. Masukkan ID yang sesuai agar tidak salah update.

### C. Pembersihan Data
1. Menu [4] hanya digunakan jika pesanan dibatalkan atau data salah input.
2. Pastikan konfirmasi dengan mengetik 'y' sebelum menghapus.

## 4. Lokasi Data
Semua data tersimpan secara permanen dalam database SQLite:
- Lokasi: `data/layanan.db`
