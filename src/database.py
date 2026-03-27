import sqlite3
import os

def buat_database():
    # Mengarahkan file database ke folder 'data'
    db_path = os.path.join("data", "layanan.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Membuat tabel layanan/order sederhana
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pelanggan TEXT NOT NULL,
            jenis_layanan TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database berhasil dibuat di: {db_path}")

if __name__ == "__main__":
    buat_database()
