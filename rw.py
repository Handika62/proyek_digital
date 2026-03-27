import sqlite3
import os
import shutil
import urllib.parse
from datetime import datetime

# === KONFIGURASI ADMIN ===
ADMIN_USER = "admin"
ADMIN_PASS = "rw123"

def init_db():
    if not os.path.exists('data'): os.makedirs('data')
    conn = sqlite3.connect('data/layanan.db')
    cursor = conn.cursor()
    # Tabel Utama
    cursor.execute('''CREATE TABLE IF NOT EXISTS warga 
        (nik TEXT PRIMARY KEY, nama TEXT, kk TEXT, no_hp TEXT, status_iuran TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS kas 
        (id INTEGER PRIMARY KEY, tgl TEXT, keterangan TEXT, masuk REAL, keluar REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pengumuman 
        (id INTEGER PRIMARY KEY, tgl TEXT, judul TEXT, isi TEXT)''')
    conn.commit()
    conn.close()

def login():
    os.system('clear')
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   🔐 LOGIN RW DIGITAL v5.0  ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    u = input("Username: ")
    p = input("Password: ")
    return u == ADMIN_USER and p == ADMIN_PASS

# --- FITUR WARGA & IURAN ---
def tambah_warga():
    print("\n--- 📝 TAMBAH DATA WARGA ---")
    nik, nama, kk = input("NIK: "), input("Nama: "), input("No KK: ")
    hp = input("No WhatsApp (08...): ")
    if hp.startswith('08'): hp = '62' + hp[1:]
    conn = sqlite3.connect('data/layanan.db')
    try:
        conn.execute("INSERT INTO warga VALUES (?, ?, ?, ?, ?)", (nik, nama, kk, hp, "BELUM BAYAR"))
        conn.commit()
        print("✅ Warga Berhasil Ditambahkan!")
    except: print("❌ Gagal! NIK mungkin sudah ada.")
    conn.close()
    input("\nTekan Enter...")

def menu_kas():
    os.system('clear')
    conn = sqlite3.connect('data/layanan.db')
    saldo = conn.execute("SELECT SUM(masuk) - SUM(keluar) FROM kas").fetchone()[0] or 0
    print(f"💰 SALDO KAS RW: Rp{saldo:,.0f}\n" + "-"*30)
    
    print("1. Bayar Iuran | 2. Catat Pengeluaran | 3. Export Laporan (.txt) | 4. Kembali")
    pilih = input("\nPilih: ")
    if pilih == '1':
        nama = input("Nama Warga: ")
        jml = float(input("Jumlah (Rp): "))
        conn.execute("UPDATE warga SET status_iuran='SUDAH BAYAR' WHERE nama=?", (nama,))
        conn.execute("INSERT INTO kas (tgl, keterangan, masuk, keluar) VALUES (?,?,?,?)", 
                     (datetime.now().strftime("%Y-%m-%d"), f"Iuran: {nama}", jml, 0))
        conn.commit()
    elif pilih == '3':
        with open("laporan_kas.txt", "w") as f:
            f.write(f"LAPORAN KAS RW\nSaldo: Rp{saldo:,.0f}\n")
            for r in conn.execute("SELECT nama FROM warga WHERE status_iuran='BELUM BAYAR'"):
                f.write(f"Tunggakan: {r[0]}\n")
        print("✅ Laporan 'laporan_kas.txt' dibuat!")
    conn.close()
    input("\nSelesai...")

# --- FITUR PENGUMUMAN ---
def buat_pengumuman():
    os.system('clear')
    print("--- 📢 PUSAT PENGUMUMAN WARGA ---")
    judul = input("Judul Pengumuman: ")
    isi = input("Isi Pesan: ")
    tgl = datetime.now().strftime("%d/%m/%Y")
    
    conn = sqlite3.connect('data/layanan.db')
    conn.execute("INSERT INTO pengumuman (tgl, judul, isi) VALUES (?, ?, ?)", (tgl, judul, isi))
    conn.commit()
    
    print("\nKirim ke siapa?")
    print("1. Kirim ke Satu Warga")
    print("2. Generate Link Broadcast (Grup)")
    opsi = input("Pilih: ")
    
    pesan_wa = f"*PENGUMUMAN RW* 📢\n\n*Target:* {judul}\n*Info:* {isi}\n\n_Pesan otomatis dari Sistem RW Digital_"
    
    if opsi == '1':
        nama = input("Nama Warga: ")
        w = conn.execute("SELECT no_hp FROM warga WHERE nama=?", (nama,)).fetchone()
        if w:
            link = f"https://wa.me/{w[0]}?text={urllib.parse.quote(pesan_wa)}"
            print(f"\n📲 Klik untuk Kirim: {link}")
    elif opsi == '2':
        print(f"\n📋 Salin Pesan ini ke Grup:\n\n{pesan_wa}")
    
    conn.close()
    input("\nKembali...")

# --- FITUR BACKUP ---
def backup_db():
    folder = "backup_data/"
    if not os.path.exists(folder): os.makedirs(folder)
    path = f"{folder}backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db"
    shutil.copy2('data/layanan.db', path)
    print(f"✅ Backup tersimpan: {path}")
    input("\nEnter...")

# --- MAIN ---
def main():
    init_db()
    if not login(): return
    while True:
        os.system('clear')
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("   📱 ADMIN RW DIGITAL v5.0  ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1. Tambah Data Warga (NIK/KK)")
        print("2. Kas & Iuran Sampah")
        print("3. Buat Pengumuman Warga 📢")
        print("4. Backup Database")
        print("5. Keluar")
        
        p = input("\nPilih menu: ")
        if p == '1': tambah_warga()
        elif p == '2': menu_kas()
        elif p == '3': buat_pengumuman()
        elif p == '4': backup_db()
        elif p == '5': break

if __name__ == "__main__":
    main()
