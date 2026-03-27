import sqlite3
import os
import urllib.parse
from datetime import datetime

# === KONFIGURASI ===
ADMIN_USER = "admin"
ADMIN_PASS = "rw123" # Ganti sesuai keinginan

def init_db():
    if not os.path.exists('data'): os.makedirs('data')
    conn = sqlite3.connect('data/layanan.db')
    cursor = conn.cursor()
    # Tabel Warga Lengkap
    cursor.execute('''CREATE TABLE IF NOT EXISTS warga 
        (nik TEXT PRIMARY KEY, nama TEXT, kk TEXT, no_hp TEXT, status_iuran TEXT)''')
    cursor.execute('CREATE TABLE IF NOT EXISTS sampah (id INTEGER PRIMARY KEY, warga TEXT, laporan TEXT, tgl TEXT)')
    conn.commit()
    conn.close()

def login():
    os.system('clear')
    print("=== LOGIN ADMIN RW DIGITAL ===")
    u = input("Username: ")
    p = input("Password: ")
    return u == ADMIN_USER and p == ADMIN_PASS

def tambah_warga():
    print("\n--- TAMBAH DATA WARGA ---")
    nik = input("NIK: ")
    nama = input("Nama: ")
    kk = input("No KK: ")
    hp = input("No WhatsApp (awali 62): ")
    conn = sqlite3.connect('data/layanan.db')
    try:
        conn.execute("INSERT INTO warga VALUES (?, ?, ?, ?, ?)", (nik, nama, kk, hp, "BELUM BAYAR"))
        conn.commit()
        print("✅ Data warga berhasil disimpan!")
    except: print("❌ NIK sudah terdaftar!")
    conn.close()
    input("\nKembali...")

def cek_iuran():
    os.system('clear')
    print("--- STATUS IURAN SAMPAH WARGA ---")
    conn = sqlite3.connect('data/layanan.db')
    rows = conn.execute("SELECT * FROM warga").fetchall()
    for r in rows:
        status = "✅ LUNAS" if r[4] == "SUDAH BAYAR" else "❌ TUNGGAKAN"
        print(f"Nama: {r[1]} | Status: {status}")
    
    print("\n1. Tandai Sudah Bayar")
    print("2. Kirim Tagihan via WhatsApp")
    pilih = input("Pilih: ")
    
    if pilih == '1':
        nama = input("Masukkan Nama Warga: ")
        conn.execute("UPDATE warga SET status_iuran='SUDAH BAYAR' WHERE nama=?", (nama,))
        conn.commit()
        print("✅ Status diperbarui!")
    elif pilih == '2':
        nama = input("Kirim tagihan ke: ")
        w = conn.execute("SELECT no_hp FROM warga WHERE nama=?", (nama,)).fetchone()
        if w:
            pesan = f"Halo Bapak/Ibu {nama}, mengingatkan untuk pembayaran iuran sampah RW bulan ini. Terima kasih."
            link = f"https://wa.me/{w[0]}?text={urllib.parse.quote(pesan)}"
            print(f"📲 Buka link ini: {link}")
    conn.close()
    input("\nKembali...")

def main():
    init_db()
    if not login():
        print("❌ Login Gagal!")
        return

    while True:
        os.system('clear')
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("   📱 ADMIN RW DIGITAL v3.0  ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1. Tambah Data Warga (NIK/KK)")
        print("2. Cek Iuran Sampah & WA")
        print("3. Layanan Sampah & Listrik")
        print("4. Menu Bisnis")
        print("5. Keluar")
        
        p = input("\nPilih: ")
        if p == '1': tambah_warga()
        elif p == '2': cek_iuran()
        elif p == '5': break
        # Menu lain (menu_sampah, menu_bisnis) tetap bisa dipanggil di sini

if __name__ == "__main__":
    main()
