import sqlite3
import os

def koneksi_db():
    return sqlite3.connect(os.path.join("data", "layanan.db"))

def tambah_pesanan():
    nama = input("\nNama Pelanggan: ")
    layanan = input("Jenis Layanan: ")
    conn = koneksi_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (nama_pelanggan, jenis_layanan) VALUES (?, ?)", (nama, layanan))
    conn.commit()
    conn.close()
    print("[✔] Pesanan berhasil disimpan!")

def lihat_pesanan():
    conn = koneksi_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    print("\n--- DAFTAR PESANAN ---")
    if not rows:
        print("Belum ada data.")
    for row in rows:
        print(f"ID: {row[0]} | Nama: {row[1]} | Layanan: {row[2]} | Status: {row[3]}")
    conn.close()

def update_status():
    lihat_pesanan()
    id_pesanan = input("\nMasukkan ID Pesanan yang diupdate: ")
    print("1. Diproses | 2. Selesai | 3. Dibatalkan")
    pilihan_status = input("Pilih (1/2/3): ")
    status_map = {'1': 'Diproses', '2': 'Selesai', '3': 'Dibatalkan'}
    status_baru = status_map.get(pilihan_status, 'Pending')
    conn = koneksi_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status_baru, id_pesanan))
    conn.commit()
    print(f"[✔] Status ID {id_pesanan} diperbarui.")
    conn.close()

def hapus_pesanan():
    lihat_pesanan()
    id_pesanan = input("\nMasukkan ID Pesanan yang akan DIHAPUS: ")
    konfirmasi = input(f"Yakin menghapus ID {id_pesanan}? (y/n): ")
    if konfirmasi.lower() == 'y':
        conn = koneksi_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (id_pesanan,))
        conn.commit()
        print(f"[✔] Data ID {id_pesanan} berhasil dihapus.")
        conn.close()

def tampilkan_laporan():
    conn = koneksi_db()
    cursor = conn.cursor()
    
    # Menghitung total berdasarkan status
    cursor.execute("SELECT status, COUNT(*) FROM orders GROUP BY status")
    laporan = cursor.fetchall()
    
    print("\n=== LAPORAN RINGKASAN LAYANAN ===")
    total_semua = 0
    if not laporan:
        print("Data masih kosong.")
    else:
        for status, jumlah in laporan:
            print(f"- {status}: {jumlah} pesanan")
            total_semua += jumlah
        print(f"--- Total Semua: {total_semua} ---")
    conn.close()

def menu_utama():
    while True:
        print("\n=== ADMIN LAYANAN DIGITAL ===")
        print("1. Tambah Pesanan")
        print("2. Lihat Semua Pesanan")
        print("3. Update Status")
        print("4. Hapus Pesanan")
        print("5. Laporan Ringkasan")
        print("6. Keluar")
        
        pilihan = input("Pilih menu (1-6): ")
        if pilihan == '1': tambah_pesanan()
        elif pilihan == '2': lihat_pesanan()
        elif pilihan == '3': update_status()
        elif pilihan == '4': hapus_pesanan()
        elif pilihan == '5': tampilkan_laporan()
        elif pilihan == '6': break
        else: print("Pilihan tidak valid!")

if __name__ == "__main__":
    menu_utama()
