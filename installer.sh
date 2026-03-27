#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   🚀 INSTALLER RW DIGITAL v5.0         "
echo "   Oleh: Handika62                      "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Update dan Upgrade System
echo "🔄 Mengupdate sistem..."
pkg update -y && pkg upgrade -y

# 2. Install Package yang dibutuhkan
echo "📦 Menginstall Python dan Git..."
pkg install python git -y

# 3. Buat Folder Database dan Nota
echo "📂 Menyiapkan struktur folder..."
mkdir -p data
mkdir -p data-warga-rt
mkdir -p nota_bisnis
mkdir -p backup_data

# 4. Beri izin akses penyimpanan (HP)
echo "🔓 Meminta izin akses storage (Klik 'Allow' di layar)..."
termux-setup-storage

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " ✅ INSTALASI SELESAI!                  "
echo " 💡 Jalankan aplikasi dengan: python rw.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
