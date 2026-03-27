import sqlite3
import os
from datetime import datetime

def init_db():
    conn = sqlite3.connect('data/layanan.db') # Menggunakan folder data Anda
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS sampah (id INTEGER PRIMARY KEY, warga TEXT, laporan TEXT, tgl TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS listrik (id INTEGER PRIMARY KEY, warga TEXT, layanan TEXT, status TEXT)')
    conn.commit()
    conn.close()

def menu_utama():
    os.system('clear')
    print("=== 📱 RW DIGITAL v2.0 ===")
    print("1. Layanan Sampah")
    print("2. Layanan Listrik")
    print("3. Keluar")
    pilih = input("\nPilih: ")
    if pilih == '1': menu_sampah()
    elif pilih == '2': menu_listrik()

def menu_sampah():
    print("\n--- 🗑️ LAYANAN SAMPAH ---")
    nama = input("Nama Warga: ")
    ket = input("Laporan: ")
    conn = sqlite3.connect('data/layanan.db')
    conn.execute("INSERT INTO sampah (warga, laporan, tgl) VALUES (?, ?, ?)", (nama, ket, datetime.now()))
    conn.commit()
    print("✅ Laporan sampah tersimpan!")
    input("\nKembali...")

def menu_listrik():
    print("\n--- ⚡ LAYANAN LISTRIK ---")
    nama = input("Nama Warga: ")
    tipe = input("Tipe (Pasang/Perbaikan): ")
    conn = sqlite3.connect('data/layanan.db')
    conn.execute("INSERT INTO listrik (warga, layanan, status) VALUES (?, ?, ?)", (nama, tipe, "Proses"))
    conn.commit()
    print("✅ Permintaan listrik terkirim!")
    input("\nKembali...")

if __name__ == "__main__":
    if not os.path.exists('data'): os.makedirs('data')
    init_db()
    while True: menu_utama()
