import os
import sys
import time
import json
import shutil
from datetime import datetime
from typing import Optional

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size"""
    size = float(bytes_size)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def backup_file(file_path: str, backup_dir: str = "backups") -> Optional[str]:
    """Create a backup of a file"""
    try:
        if not os.path.exists(file_path):
            return None
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Generate backup filename with timestamp
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{name}_backup_{timestamp}{ext}"
        backup_path = os.path.join(backup_dir, backup_name)
        
        # Copy file
        shutil.copy2(file_path, backup_path)
        return backup_path
        
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def is_windows() -> bool:
    """Check if running on Windows"""
    return os.name == 'nt'

def check_internet_connection() -> bool:
    """Check if internet connection is available"""
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        return True
    except:
        return False

def wait_with_spinner(seconds: int, message: str = "Please wait"):
    """Display a spinner while waiting"""
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    for i in range(seconds * 10):  # 10 iterations per second
        spinner = spinner_chars[i % len(spinner_chars)]
        print(f'\r{spinner} {message}...', end='', flush=True)
        time.sleep(0.1)
    
    print('\r' + ' ' * (len(message) + 10), end='\r')  # Clear the line

def validate_username(username: str) -> bool:
    """Validate Roblox username format"""
    if not username:
        return False
    
    # Roblox username rules (basic)
    if len(username) < 3 or len(username) > 20:
        return False
    
    # Only alphanumeric and underscores allowed
    if not username.replace('_', '').isalnum():
        return False
    
    return True

def safe_input(prompt: str, default: str = "") -> str:
    """Safe input with default value"""
    try:
        user_input = input(prompt).strip()
        return user_input if user_input else default
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return ""
    except EOFError:
        return default

def confirm_action(message: str, default: bool = False) -> bool:
    """Ask for user confirmation"""
    default_char = "Y/n" if default else "y/N"
    response = safe_input(f"{message} ({default_char}): ").lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes', 'true', '1']

def print_error(message: str):
    """Print error message in red"""
    from colorama import Fore, Style
    print(f"{Fore.RED}❌ ERROR: {message}{Style.RESET_ALL}")

def print_success(message: str):
    """Print success message in green"""
    from colorama import Fore, Style
    print(f"{Fore.GREEN}✅ SUCCESS: {message}{Style.RESET_ALL}")

def print_warning(message: str):
    """Print warning message in yellow"""
    from colorama import Fore, Style
    print(f"{Fore.YELLOW}⚠️  WARNING: {message}{Style.RESET_ALL}")

def print_info(message: str):
    """Print info message in blue"""
    from colorama import Fore, Style
    print(f"{Fore.CYAN}ℹ️  INFO: {message}{Style.RESET_ALL}")

def check_system_requirements() -> dict:
    """Check system requirements"""
    requirements = {
        'os': is_windows(),
        'python': sys.version_info >= (3, 7),
        'internet': check_internet_connection()
    }
    
    return requirements

def display_system_info():
    """Display system information"""
    from colorama import Fore, Style
    
    print(f"{Fore.CYAN}{Style.BRIGHT}SYSTEM INFORMATION:")
    print(f"{Fore.WHITE}OS: {os.name} ({sys.platform})")
    print(f"{Fore.WHITE}Python: {sys.version}")
    print(f"{Fore.WHITE}Working Directory: {os.getcwd()}")
    
    req = check_system_requirements()
    print(f"{Fore.WHITE}Requirements Check:")
    print(f"  - Windows: {'✅' if req['os'] else '❌'}")
    print(f"  - Python 3.7+: {'✅' if req['python'] else '❌'}")
    print(f"  - Internet: {'✅' if req['internet'] else '❌'}")

class ProgressBar:
    """Simple progress bar for long operations"""
    
    def __init__(self, total: int, width: int = 50):
        self.total = total
        self.current = 0
        self.width = width
    
    def update(self, increment: int = 1):
        """Update progress"""
        self.current = min(self.current + increment, self.total)
        self.display()
    
    def display(self):
        """Display progress bar"""
        percentage = (self.current / self.total) * 100
        filled = int((self.current / self.total) * self.width)
        bar = '█' * filled + '░' * (self.width - filled)
        
        print(f'\r[{bar}] {percentage:.1f}% ({self.current}/{self.total})', 
              end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete