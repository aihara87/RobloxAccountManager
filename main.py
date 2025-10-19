#!/usr/bin/env python3

import asyncio
import os
import sys
from colorama import init, Fore, Style
from database import AccountDatabase
from browser_manager import RobloxBrowserManager

# Initialize colorama for Windows
init(autoreset=True)

class RobloxAccountManager:
    def __init__(self):
        self.db = AccountDatabase()
        self.browser_manager = RobloxBrowserManager()
    
    def display_header(self):
        """Display the application header"""
        print(f"{Fore.CYAN}{Style.BRIGHT}=" * 60)
        print(f"{Fore.CYAN}{Style.BRIGHT}          ROBLOX ACCOUNT MANAGER")
        print(f"{Fore.CYAN}{Style.BRIGHT}=" * 60)
        print(f"{Fore.GREEN}Manage multiple Roblox accounts with ease!")
        print(f"{Fore.YELLOW}Windows Only - Requires Playwright browsers\n")
    
    def display_menu(self):
        """Display the main menu"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}MAIN MENU:")
        print(f"{Fore.WHITE}1. {Fore.GREEN}Add New Account")
        print(f"{Fore.WHITE}2. {Fore.BLUE}List All Accounts")
        print(f"{Fore.WHITE}3. {Fore.MAGENTA}Launch Account")
        print(f"{Fore.WHITE}4. {Fore.RED}Remove Account")
        print(f"{Fore.WHITE}5. {Fore.YELLOW}Update Account")
        print(f"{Fore.WHITE}6. {Fore.CYAN}Validate Sessions")
        print(f"{Fore.WHITE}7. {Fore.YELLOW}Refresh Account Session")
        print(f"{Fore.WHITE}8. {Fore.GREEN}Import Account from JSON")
        print(f"{Fore.WHITE}0. {Fore.RED}Exit")
        print(f"{Style.DIM}-" * 30)
    
    async def add_account(self):
        """Add a new Roblox account"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}ADD NEW ACCOUNT")
        print(f"{Fore.YELLOW}Note: This will open a browser for you to login")
        
        username = input(f"{Fore.WHITE}Enter account username/display name: ").strip()
        if not username:
            print(f"{Fore.RED}Username cannot be empty!")
            return
        
        # Check if account already exists
        if self.db.account_exists(username):
            print(f"{Fore.RED}Account '{username}' already exists!")
            return
        
        print(f"\n{Fore.YELLOW}Opening browser for login...")
        print(f"{Fore.CYAN}Please login to your Roblox account in the browser window")
        print(f"{Fore.CYAN}The browser will close automatically after successful login")
        
        try:
            success = await self.browser_manager.login_and_save_session(username)
            if success:
                print(f"\n{Fore.GREEN}✓ Account '{username}' added successfully!")
            else:
                print(f"\n{Fore.RED}✗ Failed to add account '{username}'")
        except Exception as e:
            print(f"\n{Fore.RED}✗ Error adding account: {str(e)}")
    
    async def import_account_from_json(self):
        """Import account from JSON cookies file"""
        import json
        import os
        from datetime import datetime
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}IMPORT ACCOUNT FROM JSON")
        print(f"{Fore.YELLOW}This feature allows you to import cookies from a JSON file")
        
        # Step 1: Input username
        username = input(f"{Fore.WHITE}Enter account username/display name: ").strip()
        if not username:
            print(f"{Fore.RED}Username cannot be empty!")
            return
        
        # Check if account already exists
        if self.db.account_exists(username):
            overwrite = input(f"{Fore.YELLOW}Account '{username}' already exists. Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                print(f"{Fore.CYAN}Import cancelled.")
                return
        
        # Step 2: Input JSON file path
        print(f"\n{Fore.CYAN}JSON Cookie Formats Supported:")
        print(f"{Fore.WHITE}1. Array of cookie objects: [{{'name': 'cookie_name', 'value': 'cookie_value', 'domain': '.roblox.com', ...}}, ...]")
        print(f"{Fore.WHITE}2. Simple key-value object: {{'cookie_name': 'cookie_value', ...}}")
        print(f"{Fore.WHITE}3. Browser export format with additional fields")
        
        json_file_path = input(f"\n{Fore.WHITE}Enter JSON file path (or drag & drop file here): ").strip().strip('"')
        
        if not json_file_path:
            print(f"{Fore.RED}File path cannot be empty!")
            return
        
        if not os.path.exists(json_file_path):
            print(f"{Fore.RED}File not found: {json_file_path}")
            return
        
        try:
            # Read and parse JSON file
            with open(json_file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            print(f"{Fore.GREEN}✓ JSON file loaded successfully")
            
            # Convert JSON to cookies format
            cookies = self._convert_json_to_cookies(json_data)
            
            if not cookies:
                print(f"{Fore.RED}✗ No valid cookies found in JSON file")
                return
            
            # Validate that we have essential Roblox cookies
            roblox_cookies = [c for c in cookies if '.roblox.com' in c.get('domain', '')]
            roblosecurity_found = any('.ROBLOSECURITY' in c.get('name', '') for c in roblox_cookies)
            
            print(f"{Fore.CYAN}📊 Cookie Analysis:")
            print(f"{Fore.WHITE}  Total cookies found: {len(cookies)}")
            print(f"{Fore.WHITE}  Roblox cookies: {len(roblox_cookies)}")
            print(f"{Fore.WHITE}  .ROBLOSECURITY found: {'✓' if roblosecurity_found else '✗'}")
            
            if not roblosecurity_found:
                print(f"{Fore.YELLOW}⚠️  Warning: No .ROBLOSECURITY cookie found. Account might not work properly.")
                continue_anyway = input(f"{Fore.WHITE}Continue anyway? (y/n): ").strip().lower()
                if continue_anyway != 'y':
                    print(f"{Fore.CYAN}Import cancelled.")
                    return
            
            # Save to database
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            
            # If account exists, update it, otherwise add new
            if self.db.account_exists(username):
                success = self.db.update_account_cookies(username, cookies, user_agent)
                action = "updated"
            else:
                success = self.db.add_account(username, user_agent, cookies)
                action = "added"
            
            if success:
                print(f"\n{Fore.GREEN}✓ Account '{username}' {action} successfully!")
                print(f"{Fore.GREEN}✓ {len(cookies)} cookies imported")
                
                # Test the imported cookies
                test_session = input(f"\n{Fore.WHITE}Test imported session now? (y/n): ").strip().lower()
                if test_session == 'y':
                    await self._test_imported_session(username)
            else:
                print(f"\n{Fore.RED}✗ Failed to save account '{username}'")
                
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}✗ Invalid JSON format: {str(e)}")
        except Exception as e:
            print(f"\n{Fore.RED}✗ Error importing account: {str(e)}")
    
    def _sanitize_cookie(self, cookie_data):
        """Sanitize a single cookie to ensure proper format"""
        # Normalize sameSite value
        same_site = cookie_data.get('sameSite', 'Lax')
        if same_site not in ['Strict', 'Lax', 'None']:
            same_site = 'Lax'
        
        # Clean and validate cookie
        clean_cookie = {
            'name': cookie_data.get('name', ''),
            'value': cookie_data.get('value', ''),
            'domain': cookie_data.get('domain', '.roblox.com'),
            'path': cookie_data.get('path', '/'),
            'secure': bool(cookie_data.get('secure', True)),
            'httpOnly': bool(cookie_data.get('httpOnly', False)),
            'sameSite': same_site
        }
        
        # Fix domain if needed
        if not clean_cookie['domain'].endswith('roblox.com'):
            clean_cookie['domain'] = '.roblox.com'
            
        return clean_cookie
    
    def _convert_json_to_cookies(self, json_data):
        """Convert various JSON formats to standard cookie format"""
        cookies = []
        
        try:
            if isinstance(json_data, list):
                # Format 1: Array of cookie objects
                for item in json_data:
                    if isinstance(item, dict) and 'name' in item and item.get('value'):
                        cookie = self._sanitize_cookie(item)
                        if cookie['name'] and cookie['value']:
                            cookies.append(cookie)
            
            elif isinstance(json_data, dict):
                # Check if it's a simple key-value format
                if all(isinstance(v, str) for v in json_data.values()):
                    # Format 2: Simple key-value object
                    for name, value in json_data.items():
                        cookie_data = {
                            'name': name,
                            'value': value,
                            'domain': '.roblox.com',
                            'path': '/',
                            'secure': True,
                            'httpOnly': False,
                            'sameSite': 'Lax'
                        }
                        cookie = self._sanitize_cookie(cookie_data)
                        cookies.append(cookie)
                else:
                    # Format 3: Complex object, try to extract cookies
                    # Look for cookies in common locations
                    if 'cookies' in json_data:
                        return self._convert_json_to_cookies(json_data['cookies'])
                    elif 'sessionData' in json_data:
                        return self._convert_json_to_cookies(json_data['sessionData'])
        
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Warning during cookie conversion: {str(e)}")
        
        return cookies
    
    async def _test_imported_session(self, username):
        """Test the imported session by validating login"""
        print(f"\n{Fore.CYAN}🔍 Testing imported session for '{username}'...")
        
        try:
            is_valid = await self.browser_manager.validate_account_session(username)
            if is_valid:
                print(f"{Fore.GREEN}✅ Session test successful! Account is ready to use.")
            else:
                print(f"{Fore.RED}❌ Session test failed. Cookies might be expired or invalid.")
                print(f"{Fore.YELLOW}💡 Try logging in manually to refresh the session.")
        except Exception as e:
            print(f"{Fore.RED}❌ Error testing session: {str(e)}")
    
    def list_accounts(self):
        """List all saved accounts"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}SAVED ACCOUNTS")
        accounts = self.db.get_all_accounts()
        
        if not accounts:
            print(f"{Fore.YELLOW}No accounts found. Add an account first.")
            return
        
        print(f"{Fore.WHITE}{'ID':<5} {'Username':<20} {'Added Date':<20} {'Status'}")
        print(f"{Style.DIM}" + "-" * 70)
        
        for i, account in enumerate(accounts, 1):
            status = f"{Fore.GREEN}Active" if account['is_active'] else f"{Fore.RED}Inactive"
            print(f"{Fore.WHITE}{i:<5} {account['username']:<20} {account['created_at']:<20} {status}")
    
    async def launch_account(self):
        """Launch Roblox with selected account"""
        accounts = self.db.get_all_accounts()
        if not accounts:
            print(f"{Fore.YELLOW}No accounts found. Add an account first.")
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}LAUNCH ACCOUNT")
        self.list_accounts()
        
        try:
            choice = int(input(f"\n{Fore.WHITE}Enter account number to launch: "))
            if 1 <= choice <= len(accounts):
                account_summary = accounts[choice - 1]
                # Get full account data including cookies
                account = self.db.get_account(account_summary['username'])
                if not account:
                    print(f"{Fore.RED}✗ Account data not found!")
                    return
                
                print(f"\n{Fore.YELLOW}Launching Roblox for account: {account['username']}")
                
                success = await self.browser_manager.launch_with_account(account)
                if success:
                    print(f"{Fore.GREEN}✓ Successfully launched Roblox!")
                else:
                    print(f"{Fore.RED}✗ Failed to launch Roblox")
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
        except Exception as e:
            print(f"{Fore.RED}✗ Error launching account: {str(e)}")
    
    def remove_account(self):
        """Remove an account"""
        accounts = self.db.get_all_accounts()
        if not accounts:
            print(f"{Fore.YELLOW}No accounts found.")
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}REMOVE ACCOUNT")
        self.list_accounts()
        
        try:
            choice = int(input(f"\n{Fore.WHITE}Enter account number to remove: "))
            if 1 <= choice <= len(accounts):
                account = accounts[choice - 1]
                confirm = input(f"{Fore.RED}Are you sure you want to remove '{account['username']}'? (y/N): ").lower()
                
                if confirm == 'y':
                    if self.db.remove_account(account['username']):
                        print(f"{Fore.GREEN}✓ Account '{account['username']}' removed successfully!")
                    else:
                        print(f"{Fore.RED}✗ Failed to remove account")
                else:
                    print(f"{Fore.YELLOW}Operation cancelled")
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
    
    def update_account(self):
        """Update account status"""
        accounts = self.db.get_all_accounts()
        if not accounts:
            print(f"{Fore.YELLOW}No accounts found.")
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}UPDATE ACCOUNT STATUS")
        self.list_accounts()
        
        try:
            choice = int(input(f"\n{Fore.WHITE}Enter account number to update: "))
            if 1 <= choice <= len(accounts):
                account = accounts[choice - 1]
                new_status = not account['is_active']
                status_text = "activate" if new_status else "deactivate"
                
                if self.db.update_account_status(account['username'], new_status):
                    print(f"{Fore.GREEN}✓ Account '{account['username']}' {status_text}d successfully!")
                else:
                    print(f"{Fore.RED}✗ Failed to update account")
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
    
    async def run(self):
        """Main application loop"""
        self.display_header()
        
        while True:
            self.display_menu()
            try:
                choice = input(f"{Fore.WHITE}Enter your choice (0-8): ").strip()
                
                if choice == "0":
                    print(f"\n{Fore.GREEN}Thank you for using Roblox Account Manager!")
                    print(f"{Fore.YELLOW}Goodbye! 👋")
                    break
                elif choice == "1":
                    await self.add_account()
                elif choice == "2":
                    self.list_accounts()
                elif choice == "3":
                    await self.launch_account()
                elif choice == "4":
                    self.remove_account()
                elif choice == "5":
                    self.update_account()
                elif choice == "6":
                    await self.validate_sessions()
                elif choice == "7":
                    await self.refresh_single_session()
                elif choice == "8":
                    await self.import_account_from_json()
                else:
                    print(f"{Fore.RED}Invalid choice! Please try again.")
                
                # Wait for user input before showing menu again
                if choice != "0":
                    input(f"\n{Fore.CYAN}Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Interrupted by user. Goodbye! 👋")
                break
            except Exception as e:
                print(f"\n{Fore.RED}An error occurred: {str(e)}")
                print(f"{Fore.CYAN}Press Enter to continue...")

    async def validate_sessions(self):
        """Validate all account sessions"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}VALIDATE SESSIONS")
        print(f"{Fore.YELLOW}This will check all accounts for expired sessions...")
        
        try:
            expired_count = await self.browser_manager.clean_expired_sessions()
            if expired_count > 0:
                print(f"\n{Fore.YELLOW}Found {expired_count} expired sessions.")
                print(f"{Fore.CYAN}You can refresh them using menu option 7.")
            else:
                print(f"\n{Fore.GREEN}All sessions are valid!")
        except Exception as e:
            print(f"{Fore.RED}Error validating sessions: {str(e)}")
    
    async def refresh_single_session(self):
        """Refresh a single account session"""
        accounts = self.db.get_all_accounts()
        if not accounts:
            print(f"{Fore.YELLOW}No accounts found.")
            return
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}REFRESH ACCOUNT SESSION")
        self.list_accounts()
        
        try:
            choice = int(input(f"\n{Fore.WHITE}Enter account number to refresh: "))
            if 1 <= choice <= len(accounts):
                account = accounts[choice - 1]
                print(f"\n{Fore.YELLOW}Refreshing session for: {account['username']}")
                
                success = await self.browser_manager.refresh_account_session(account['username'])
                if success:
                    print(f"{Fore.GREEN}✓ Session refreshed successfully!")
                    # Reactivate the account
                    self.db.update_account_status(account['username'], True)
                else:
                    print(f"{Fore.RED}✗ Failed to refresh session")
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
        except Exception as e:
            print(f"{Fore.RED}Error refreshing session: {str(e)}")

def main():
    """Main entry point"""
    try:
        app = RobloxAccountManager()
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program interrupted. Goodbye!")
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()