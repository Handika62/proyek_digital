import sqlite3
import os
import glob
from datetime import datetime

# 1. Fungsi Sinkronisasi Data dari Folder ke Database
def sinkronisasi_warga():
    folder_path = "data-warga-rt/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    conn = sqlite3.connect('data/layanan.db')
    cursor = conn.cursor()
    
    # Ambil semua file .txt di folder data-warga-rt
    files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    jumlah_baru = 0
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                nama = line.strip()
                if nama:
                    # Masukkan nama ke database jika belum ada
                    cursor.execute('INSERT OR IGNORE INTO daftar_warga (nama) VALUES (?)', (nama,))
                    if cursor.rowcount > 0:
                        jumlah_baru += 1
    
    conn.commit()
    conn.close()
    if jumlah_baru > 0:
        print(f"✨ Berhasil mengimpor {jumlah_baru} warga baru dari folder.")

# 2. Inisialisasi Database Awal
def init_db():
    if not os.path.exists('data'): os.makedirs('data')
    conn = sqlite3.connect('data/layanan.db')
    cursor = conn.cursor()
    # Tabel Master Warga
    cursor.execute('CREATE TABLE IF NOT EXISTS daftar_warga (id INTEGER PRIMARY KEY, nama TEXT UNIQUE)')
    # Tabel Layanan
    cursor.execute('CREATE TABLE IF NOT EXISTS sampah (id INTEGER PRIMARY KEY, warga TEXT, laporan TEXT, tgl TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS listrik (id INTEGER PRIMARY KEY, warga TEXT, layanan TEXT, status TEXT)')
    conn.commit()
    conn.close()
    sinkronisasi_warga()

# 3. Fungsi Cek Validasi Warga
def validasi_warga(nama_input):
    conn = sqlite3.connect('data/layanan.db')
    cur = conn.cursor()
    cur.execute("SELECT nama FROM daftar_warga WHERE nama LIKE ?", (f"%{nama_input}%",))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

# 4. Fitur Layanan
def menu_sampah():
    print("\n--- 🗑️ LAYANAN PENGELOLAAN SAMPAH ---")
    nama_cari = input("Masukkan Nama Warga: ")
    nama_valid = validasi_warga(nama_cari)
    
    if nama_valid:
        print(f"✅ Terverifikasi: {nama_valid}")
        laporan = input("Detail Masalah (misal: Sampah belum diangkut): ")
        tgl = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = sqlite3.connect('data/layanan.db')
        conn.execute("INSERT INTO sampah (warga, laporan, tgl) VALUES (?, ?, ?)", (nama_valid, laporan, tgl))
        conn.commit()
        print("✅ Laporan sampah berhasil disimpan!")
    else:
        print("❌ Nama tidak ditemukan di data-warga-rt!")
    input("\nTekan Enter...")

def menu_listrik():
    print("\n--- ⚡ LAYANAN LISTRIK RW ---")
    nama_cari = input("Masukkan Nama Warga: ")
    nama_valid = validasi_warga(nama_cari)
    
    if nama_valid:
        print(f"✅ Terverifikasi: {nama_valid}")
        print("1. Pasang Baru\n2. Perbaikan Korsleting")
        opsi = input("Pilih layanan: ")
        tipe = "Pasang Baru" if opsi == '1' else "Perbaikan"
        
        conn = sqlite3.connect('data/layanan.db')
        conn.execute("INSERT INTO listrik (warga, layanan, status) VALUES (?, ?, ?)", (nama_valid, tipe, "Menunggu Teknisi"))
        conn.commit()
        print(f"✅ Permintaan {tipe} telah diteruskan ke teknisi!")
    else:
        print("❌ Nama tidak ditemukan!")
    input("\nTekan Enter...")

# 5. Menu Utama
def main():
    def main():
    init_db()
    init_db_bisnis() # Tambahkan ini agar database bisnis siap
    while True:
        os.system('clear')
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("   📱 RW DIGITAL TERIMPOR   ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1. Layanan Sampah")
        print("2. Layanan Listrik")
        print("3. Cek Status Semua")
        print("4. Keluar")
        print("5. Menu Bisnis (Service Pompa/Cleaning)") # Tambahkan baris ini
        
        pilih = input("\nPilih menu: ")
        if pilih == '1': menu_sampah()
        elif pilih == '2': menu_listrik()
        elif pilih == '3':
            # ... kode status ...
            input("\nKembali...")
        elif pilih == '4': break
        elif pilih == '5': menu_bisnis() # Tambahkan baris ini

if __name__ == "__main__":
    main()
import urllib.parse  # Tambahkan ini di bagian paling atas

# 1. Konfigurasi Nomor Pengurus/Teknisi
NOMOR_TEKNISI_LISTRIK = "6281234567890" # Ganti dengan nomor asli (awali 62)
NOMOR_PENGURUS_SAMPAH = "6281234567890"

# 2. Fungsi untuk Generate Link WhatsApp
def kirim_wa(nomor, pesan):
    pesan_encoded = urllib.parse.quote(pesan)
    link = f"https://wa.me/{nomor}?text={pesan_encoded}"
    print("\n" + "="*30)
    print("📲 NOTIFIKASI WHATSAPP SIAP")
    print("="*30)
    print(f"Silakan klik/buka link ini untuk lapor:\n{link}")
    print("="*30)

# 3. Update Fungsi Menu Listrik (Contoh)
def menu_listrik():
    print("\n--- ⚡ LAYANAN LISTRIK RW ---")
    nama_cari = input("Masukkan Nama Warga: ")
    nama_valid = validasi_warga(nama_cari)
    
    if nama_valid:
        print("1. Pasang Baru\n2. Perbaikan Korsleting")
        opsi = input("Pilih layanan: ")
        tipe = "Pasang Baru" if opsi == '1' else "Perbaikan"
        
        # Simpan ke Database
        conn = sqlite3.connect('data/layanan.db')
        conn.execute("INSERT INTO listrik (warga, layanan, status) VALUES (?, ?, ?)", (nama_valid, tipe, "Menunggu"))
        conn.commit()
        
        # Kirim Notifikasi WA
        pesan_wa = f"Laporan Listrik RW Digital:\nNama: {nama_valid}\nLayanan: {tipe}\nStatus: Segera diproses."
        kirim_wa(NOMOR_TEKNISI_LISTRIK, pesan_wa)
        
        print(f"✅ Data tersimpan & Link WA dibuat!")
    else:
        print("❌ Nama tidak ditemukan!")
    input("\nTekan Enter...")
# 1. Database Bisnis
def init_db_bisnis():
    conn = sqlite3.connect('data/layanan.db')
    cursor = conn.cursor()
    # Tabel Bisnis (Pompa & Cleaning)
    cursor.execute('''CREATE TABLE IF NOT EXISTS bisnis 
                      (id INTEGER PRIMARY KEY, pelanggan TEXT, jasa TEXT, harga REAL, tgl TEXT)''')
    conn.commit()
    conn.close()

# 2. Fitur Layanan Bisnis
def menu_bisnis():
    while True:
        os.system('clear')
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("   🏢 MANAJEMEN BISNIS SAYA  ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1. Service Pompa Air")
        print("2. Professional Cleaning Service")
        print("3. Cek Laporan Penghasilan")
        print("4. Kembali ke Menu RW")
        
        pilih = input("\nPilih layanan: ")
        
        if pilih in ['1', '2']:
            jasa = "Service Pompa" if pilih == '1' else "Cleaning Service"
            nama = input("Nama Pelanggan: ")
            harga = float(input("Harga Jasa (Rp): "))
            tgl = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            conn = sqlite3.connect('data/layanan.db')
            conn.execute("INSERT INTO bisnis (pelanggan, jasa, harga, tgl) VALUES (?, ?, ?, ?)", 
                         (nama, jasa, harga, tgl))
            conn.commit()
            
            # Kirim Notifikasi WA ke HP Anda sendiri sebagai owner
            pesan = f"Order Masuk!\nLayanan: {jasa}\nPelanggan: {nama}\nTotal: Rp{harga:,.0f}"
            kirim_wa("6281234567890", pesan) # Ganti dengan nomor WA Anda
            
            print(f"✅ Order {jasa} berhasil dicatat!")
            input("\nTekan Enter...")
            
        elif pilih == '3':
            print("\n--- LAPORAN KEUANGAN ---")
            conn = sqlite3.connect('data/layanan.db')
            total = 0
            for r in conn.execute("SELECT pelanggan, jasa, harga FROM bisnis"):
                print(f"- {r[0]} | {r[1]} | Rp{r[2]:,.0f}")
                total += r[2]
            print(f"\n💰 TOTAL PENDAPATAN: Rp{total:,.0f}")
            input("\nTekan Enter...")
        elif pilih == '4':
            break

# 3. Update Menu Utama (Tambahkan Opsi Menu Bisnis)
# Di dalam def main(), tambahkan:
# print("5. Menu Bisnis (Service Pompa/Cleaning)")
# if pilihan == '5': menu_bisnis()
# 1. Fungsi Generate Nota Digital
def buat_nota(pelanggan, jasa, harga):
    nama_file = f"nota_{pelanggan.replace(' ', '_')}_{datetime.now().strftime('%d%m%y_%H%M')}.txt"
    folder_nota = "nota_bisnis/"
    
    if not os.path.exists(folder_nota):
        os.makedirs(folder_nota)
    
    path_nota = os.path.join(folder_nota, nama_file)
    
    garis = "=" * 35
    isi_nota = f"""
{garis}
       BUKTI LAYANAN DIGITAL
{garis}
Tanggal   : {datetime.now().strftime('%Y-%m-%d %H:%M')}
Pelanggan : {pelanggan}
Layanan   : {jasa}
Total     : Rp{harga:,.0f}
{garis}
      TERIMA KASIH TELAH
    MENGGUNAKAN JASA KAMI
{garis}
"""
    with open(path_nota, 'w') as f:
        f.write(isi_nota)
    
    print(f"\n📄 Nota Digital dibuat: {path_nota}")
    print(isi_nota)

# 2. Update Fungsi menu_bisnis()
# Di dalam bagian 'if pilih in ['1', '2']', setelah conn.commit():
# Panggil fungsi buat_nota(nama, jasa, harga)
