# Roblox Account Manager

A Python-based CLI application for managing multiple Roblox accounts with browser automation and session persistence using Playwright.

## 🚀 Key Features

- **Multi-Account Management**: Store and manage multiple Roblox accounts
- **Browser Automation**: Automatic login using Playwright
- **Session Persistence**: Save cookies and session data for seamless re-login
- **JSON Cookie Import**: Import accounts from exported browser cookies (JSON format)
- **Browser Gaming**: Play Roblox games directly in browser
- **Session Validation**: Check and refresh expired account sessions
- **CLI Interface**: User-friendly command line interface with colors
- **Windows Support**: Specifically designed for Windows environment

## 📋 Persyaratan Sistem

- Windows 10/11
- Python 3.7+ 
- Virtual Environment (venv)
- Browser Chromium (akan diinstall otomatis oleh Playwright)

## 🛠️ Instalasi

1. **Clone atau download repository ini**
   ```bash
   git clone https://github.com/aihara87/RobloxAccountManager.git
   cd RobloxAccountManager
   ```

2. **Buat virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Aktifkan virtual environment**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install browser Playwright**
   ```bash
   playwright install
   ```

## 🎮 Cara Penggunaan

1. **Jalankan aplikasi**
   ```bash
   python main.py
   ```

2. **Main Menu Options**
   - `1` - Add New Account: Add a new Roblox account via browser login
   - `2` - List All Accounts: View all saved accounts
   - `3` - Launch Account: Launch Roblox with selected account
   - `4` - Remove Account: Delete account from database
   - `5` - Update Account: Update account information
   - `6` - Validate Sessions: Check all account session status
   - `7` - Refresh Account Session: Re-login specific account
   - `8` - Import Account from JSON: Import account using cookie JSON file
   - `0` - Exit: Close the application

## 📂 Struktur File

```
RobloxAccountManager/
├── main.py                      # File utama aplikasi CLI
├── database.py                  # Manajemen database SQLite
├── browser_manager.py           # Browser automation dengan Playwright  
├── config.py                    # Konfigurasi aplikasi
├── utils.py                     # Utility functions
├── requirements.txt             # Dependencies Python
├── README.md                    # Dokumentasi utama
├── CHANGELOG.md                 # Riwayat perubahan
├── COOKIE_IMPORT_GUIDE.md       # Panduan import cookies JSON
├── TROUBLESHOOTING.md           # Panduan troubleshooting
├── example_cookies.json         # Contoh format cookie lengkap
├── example_cookies_simple.json  # Contoh format cookie sederhana
├── roblox_accounts.db           # Database SQLite (dibuat otomatis)
├── setup.bat                    # Script setup Windows
├── run.bat                      # Script run Windows
└── venv/                        # Virtual environment
```

## 🔧 Cara Kerja

### 1. Menambah Akun Baru
- Pilih menu "Add New Account"
- Masukkan username/display name
- Browser akan terbuka ke halaman login Roblox
- Login manual dengan akun Anda
- Session otomatis tersimpan ke database

### 2. Import Akun dari JSON
- Pilih menu "Import Account from JSON" 
- Masukkan username/display name
- Pilih file JSON cookies (drag & drop supported)
- Review analisis cookies yang diimport
- Test session (opsional)
- Akun siap digunakan

### 3. Meluncurkan Akun
- Pilih menu "Launch Account"
- Pilih akun dari daftar
- Aplikasi akan:
  - Membuka browser dengan session tersimpan
  - Otomatis login ke Roblox
  - Redirect ke halaman games untuk bermain

## 💾 Database

Aplikasi menggunakan SQLite untuk menyimpan:
- Username dan display name
- Cookies session
- User agent browser
- Session metadata
- Status aktif/tidak aktif
- Timestamp pembuatan dan update

## ⚠️ Catatan Penting

### 🔒 Security & Privacy
1. **Local Storage Only**: All data stored locally in SQLite database
2. **No Cloud Sync**: Cookies never leave your computer
3. **Secure Cookie Handling**: .ROBLOSECURITY and session data encrypted
4. **File Permissions**: Protect JSON cookie files from unauthorized access

### 🚨 Cookie Safety
1. **Never Share .ROBLOSECURITY**: This cookie gives full account access
2. **Use Fresh Cookies**: Export from recently active browser sessions
3. **Enable 2FA**: Add extra security layer to your Roblox accounts  
4. **Regular Updates**: Re-export cookies when sessions expire

### 📋 General Notes
1. **Session Expiry**: Roblox sessions expire periodically, requires refresh
2. **Windows Optimized**: Designed specifically for Windows environment
3. **Roblox ToS Compliance**: Use responsibly and follow Roblox Terms of Service
4. **Educational Purpose**: Tool designed for legitimate account management

## � Cookie Import Features

### Supported JSON Formats:
1. **Array of Cookie Objects** (Recommended)
   ```json
   [{"name": "cookie_name", "value": "cookie_value", "domain": ".roblox.com", ...}, ...]
   ```

2. **Simple Key-Value Object** 
   ```json
   {"cookie_name": "cookie_value", "another_cookie": "another_value"}
   ```

3. **Browser Export Format** - Compatible with most browser cookie exporters

### Import Process:
1. Export cookies from your browser (while logged into Roblox)
2. Save as JSON file
3. Use menu option 8 to import
4. Provide username and JSON file path
5. Review import analysis and test session

📖 **For detailed instructions, see [COOKIE_IMPORT_GUIDE.md](COOKIE_IMPORT_GUIDE.md)**

## �🐛 Troubleshooting

### Browser tidak membuka
```bash
playwright install chromium
```

### Import error playwright
```bash
pip install --upgrade playwright
```

### JSON import errors
- Validate JSON format using online validators
- Ensure cookies were exported from active Roblox session
- Check that .ROBLOSECURITY cookie is present

### Database error
Hapus file `roblox_accounts.db` dan restart aplikasi untuk membuat database baru.

### Session expired
- Use menu "Refresh Account Session" to re-login
- Or import fresh cookies from active browser session

## � Dependencies

- **playwright**: Browser automation framework
- **colorama**: Terminal colors for enhanced CLI experience  
- **sqlite3**: Built-in database for local storage
- **json**: Built-in JSON handling for cookie import/export
- **asyncio**: Asynchronous operations support

## 🆕 Recent Updates

- ✅ **v1.1.0**: Added JSON cookie import functionality
- ✅ **v1.0.0**: Initial release with core features

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 📚 Documentation

- **[README.md](README.md)** - Main documentation (this file)
- **[COOKIE_IMPORT_GUIDE.md](COOKIE_IMPORT_GUIDE.md)** - Detailed cookie import instructions
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates

## �📄 License

Project ini dibuat untuk keperluan edukasi dan personal use.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

### Development Setup:
```bash
git clone https://github.com/aihara87/RobloxAccountManager.git
cd RobloxAccountManager
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## 📞 Support

Jika ada masalah atau pertanyaan, silakan buat issue di repository ini.

**Repository**: https://github.com/aihara87/RobloxAccountManager

---

**Disclaimer**: Aplikasi ini dibuat untuk tujuan edukasi dan manajemen akun yang legitimate. Pastikan penggunaan sesuai dengan kebijakan dan Terms of Service Roblox. Developer tidak bertanggung jawab atas penyalahgunaan tools ini.
=======
# RobloxAccountManager
