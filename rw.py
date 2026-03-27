import sqlite3
import os
import glob
from datetime import datetime

# Fungsi baru untuk membaca data dari folder data-warga-rt
def import_data_warga():
    folder_path = "data-warga-rt/"
    warga_terdaftar = []
    
    # Mencari semua file .txt di dalam folder data-warga-rt
    files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                nama = line.strip()
                if nama:
                    warga_terdaftar.append(nama)
    return warga_terdaftar

def init_db():
    if not os.path.exists('data'): os.makedirs('data')
    conn = sqlite3.connect('data/layanan.db')
    cursor = conn.cursor()
    # Tabel baru untuk menyimpan daftar warga dari folder
    cursor.execute('CREATE TABLE IF NOT EXISTS daftar_warga (id INTEGER PRIMARY KEY, nama TEXT UNIQUE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS sampah (id INTEGER PRIMARY KEY, warga TEXT, laporan TEXT, tgl TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS listrik (id INTEGER PRIMARY KEY, warga TEXT, layanan TEXT, status TEXT)')
    
    # Sinkronisasi data warga dari folder ke database
    warga_folder = import_data_warga()
    for nama in warga_folder:
        cursor.execute('INSERT OR IGNORE INTO daftar_warga (nama) VALUES (?)', (nama,))
    
    conn.commit()
    conn.close()

def cek_warga(nama):
    conn = sqlite3.connect('data/layanan.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM daftar_warga WHERE nama LIKE ?", (f"%{nama}%",))
    result = cur.fetchone()
    conn.close()
    return result

def menu_sampah():
    print("\n--- 🗑️ LAYANAN SAMPAH ---")
    nama_input = input("Masukkan Nama Warga: ")
    warga = cek_warga(nama_input)
    
    if warga:
        print(f"✅ Warga ditemukan: {warga[1]}")
        ket = input("Laporan: ")
        conn = sqlite3.connect('data/layanan.db')
        conn.execute("INSERT INTO sampah (warga, laporan, tgl) VALUES (?, ?, ?)", (warga[1], ket, datetime.now()))
        conn.commit()
        print("✅ Laporan sampah tersimpan!")
    else:
        print("❌ Nama tidak terdaftar di data-warga-rt!")
    input("\nKembali...")

# ... (lanjutkan dengan menu_listrik dan menu_utama yang sama)

