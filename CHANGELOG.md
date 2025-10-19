# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-19

### Added
- Initial release of Roblox Account Manager
- Multi-account management system with SQLite database
- Browser automation using Playwright for seamless login
- Session persistence with secure cookie storage
- Account validation and automatic session refresh system
- Colorful CLI interface using colorama
- Browser-based gaming without desktop app dependency
- Comprehensive error handling and user feedback
- Account status tracking (Active/Inactive)
- Batch session validation for all accounts
- Individual account session refresh functionality

### Features
- **Add New Account**: Manual login process with automatic cookie extraction
- **List All Accounts**: View all saved accounts with status and dates
- **Launch Account**: Open browser with restored session for immediate gaming
- **Remove Account**: Safe account deletion from database
- **Update Account**: Refresh account information and metadata  
- **Validate Sessions**: Check all accounts for session validity
- **Refresh Account Session**: Re-login specific accounts with expired sessions

### Technical Details
- Python 3.8+ compatibility
- Async/await pattern for browser operations
- SQLite database with proper schema and indexing
- Playwright browser automation with Chromium
- Cross-platform support (Windows optimized)
- Robust error handling and logging
- Secure local storage of sensitive session data

### Security
- Local SQLite storage (no cloud dependencies)
- Session cookies stored securely
- No plaintext password storage
- Automatic session cleanup for expired accounts
- User agent preservation for consistency

### Documentation
- Comprehensive README with installation guide
- Troubleshooting documentation  
- Code comments and type hints
- Git repository with proper .gitignore

## [Unreleased]

### Planned Features
- Account groups/categories
- Bulk operations on multiple accounts
- Export/import functionality
- Configuration file support
- GUI interface option
- Account statistics and usage tracking