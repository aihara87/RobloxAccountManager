import os

# Database configuration
DATABASE_NAME = "roblox_accounts.db"

# Roblox URLs
ROBLOX_LOGIN_URL = "https://www.roblox.com/login"
ROBLOX_HOME_URL = "https://www.roblox.com/"
ROBLOX_GAMES_URL = "https://www.roblox.com/games"

# Browser configuration
BROWSER_ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--disable-web-security',
    '--allow-running-insecure-content',
    '--no-sandbox'
]

# Timeouts (in seconds)
LOGIN_TIMEOUT = 300  # 5 minutes
PAGE_LOAD_TIMEOUT = 30
BROWSER_LAUNCH_TIMEOUT = 60

# User Agent
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Roblox executable paths (Windows)
ROBLOX_PATHS = [
    os.path.expanduser("~/AppData/Local/Roblox/Versions/RobloxPlayerBeta.exe"),
    "C:/Program Files/Roblox/Versions/RobloxPlayerBeta.exe", 
    "C:/Program Files (x86)/Roblox/Versions/RobloxPlayerBeta.exe"
]

# Colors for CLI (colorama)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'