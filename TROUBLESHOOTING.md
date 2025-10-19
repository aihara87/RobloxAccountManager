# Troubleshooting Guide - Roblox Account Manager

## 🔧 Common Issues and Solutions

### 1. "Session expired or invalid" Error

**Problem**: Session cookies sudah expired atau tidak valid.

**Solutions**:
1. **Automatic Refresh** (Recommended):
   - Pilih menu `3. Launch Account`
   - Ketika diminta refresh session, tekan `y`
   - Login ulang di browser yang terbuka
   - Session akan otomatis diperbarui

2. **Manual Refresh**:
   - Pilih menu `7. Refresh Account Session`
   - Pilih akun yang ingin direfresh
   - Login ulang di browser

3. **Validate All Sessions**:
   - Pilih menu `6. Validate Sessions`
   - Sistem akan cek semua akun dan mark yang expired

### 2. Browser Tidak Membuka

**Problem**: Playwright browser tidak terbuka.

**Solutions**:
```bash
# Install ulang browser
playwright install chromium

# Atau install semua browser
playwright install
```

### 3. Import Error Playwright

**Problem**: Module playwright tidak ditemukan.

**Solutions**:
```bash
# Aktifkan venv terlebih dahulu
.\venv\Scripts\Activate.ps1

# Install ulang playwright
pip install --upgrade playwright
```

### 4. Database Error

**Problem**: Database corrupt atau error.

**Solutions**:
1. **Reset Database**:
   ```bash
   # Hapus database lama
   del roblox_accounts.db
   
   # Restart aplikasi untuk buat database baru
   python main.py
   ```

2. **Backup Database**:
   ```python
   # Dalam aplikasi Python
   from database import AccountDatabase
   db = AccountDatabase()
   db.backup_database("backup_filename.db")
   ```

### 5. Roblox Desktop App Tidak Terdeteksi

**Problem**: Aplikasi Roblox desktop tidak ditemukan.

**Solutions**:
1. **Install Roblox**:
   - Download dari https://www.roblox.com/download
   - Install dengan default settings

2. **Check Path Manual**:
   - Path biasanya: `%LOCALAPPDATA%\Roblox\Versions\`
   - Pastikan ada file `RobloxPlayerBeta.exe`

### 6. Cookies Tidak Tersimpan

**Problem**: Session tidak tersimpan dengan benar.

**Solutions**:
1. **Clear Browser Data**:
   - Hapus cookies Roblox di browser utama
   - Login ulang melalui aplikasi

2. **Check Domain Settings**:
   - Pastikan cookies domain `.roblox.com`
   - Disable adblocker/privacy extensions

### 7. Login Timeout

**Problem**: Timeout saat menunggu login.

**Solutions**:
1. **Increase Timeout**:
   ```python
   # Dalam config.py
   LOGIN_TIMEOUT = 600  # 10 menit
   ```

2. **Manual Login**:
   - Login lebih cepat di browser
   - Jangan biarkan browser idle terlalu lama

### 8. "Automation Detected" Error

**Problem**: Roblox mendeteksi browser automation.

**Solutions**:
1. **Use Different User Agent**:
   ```python
   # Browser akan menggunakan user agent yang berbeda
   # Sudah dihandle otomatis dalam kode
   ```

2. **Manual Mode**:
   - Gunakan browser manual jika automation terdeteksi
   - Copy cookies manual ke database

## 🛡️ Prevention Tips

### 1. Session Management
- Refresh session secara berkala (setiap 1-2 minggu)
- Jangan logout dari Roblox di browser lain
- Gunakan menu "Validate Sessions" secara rutin

### 2. Security
- Jangan share file database dengan orang lain
- Backup database secara rutin
- Jangan gunakan pada public computer

### 3. Performance
- Tutup browser setelah selesai
- Jangan buka terlalu banyak akun bersamaan
- Restart aplikasi jika ada memory leak

## 📞 Emergency Recovery

### Jika Semua Akun Hilang:
1. Check file `roblox_accounts.db` masih ada
2. Restore dari backup jika ada
3. Add account ulang jika perlu

### Jika Aplikasi Crash:
1. Restart aplikasi
2. Check error di terminal
3. Reinstall dependencies jika perlu

### Jika Browser Hang:
1. Kill process Chromium/browser
2. Restart aplikasi
3. Try again dengan akun yang berbeda

## 🔍 Debug Mode

Untuk debugging, edit `browser_manager.py`:

```python
# Untuk melihat lebih detail error
import logging
logging.basicConfig(level=logging.DEBUG)

# Untuk keep browser open lebih lama
await page.wait_for_timeout(600000)  # 10 menit
```

## 📧 Support

Jika masalah masih berlanjut:
1. Check README.md untuk informasi terbaru
2. Pastikan semua requirements terpenuhi
3. Coba reinstall dari awal jika diperlukan