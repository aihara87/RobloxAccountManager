import asyncio
import os
import subprocess
import time
import json
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from database import AccountDatabase

class RobloxBrowserManager:
    def __init__(self):
        self.db = AccountDatabase()
        self.roblox_login_url = "https://www.roblox.com/login"
        self.roblox_home_url = "https://www.roblox.com/"
        
    async def login_and_save_session(self, username: str) -> bool:
        """
        Open browser for user to login and save session data
        """
        try:
            async with async_playwright() as p:
                # Launch browser with GUI for user interaction
                browser = await p.chromium.launch(
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--allow-running-insecure-content'
                    ]
                )
                
                context = await browser.new_context(
                    viewport={'width': 1280, 'height': 720},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                page = await context.new_page()
                
                # Navigate to Roblox login page
                await page.goto(self.roblox_login_url, wait_until='networkidle')
                
                print("🌐 Browser opened! Please login to your Roblox account...")
                print("⏳ Waiting for login completion...")
                
                # Wait for user to login and be redirected to home page
                login_successful = await self._wait_for_login(page)
                
                if login_successful:
                    print("✓ Login detected! Saving session data...")
                    
                    # Get cookies and other session data
                    cookies = await context.cookies()
                    user_agent = await page.evaluate("navigator.userAgent")
                    
                    # Try to get user info from the page
                    display_name = await self._extract_user_info(page)
                    
                    # Save to database
                    success = self.db.add_account(
                        username=username,
                        display_name=display_name,
                        cookies=cookies,
                        user_agent=user_agent,
                        session_data={'logged_in': True, 'login_time': time.time()}
                    )
                    
                    await browser.close()
                    return success
                else:
                    print("❌ Login timeout or failed")
                    await browser.close()
                    return False
                    
        except Exception as e:
            print(f"❌ Error during login process: {str(e)}")
            return False
    
    async def _wait_for_login(self, page: Page, timeout: int = 300) -> bool:
        """
        Wait for user to complete login process
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                current_url = page.url
                
                # Check if we're on the home page (indicates successful login)
                if 'roblox.com' in current_url and 'login' not in current_url:
                    # Additional check: look for elements that indicate logged-in state
                    try:
                        # Look for user navigation elements
                        nav_user = await page.wait_for_selector(
                            '[data-testid="navigation-user"], .navbar-user, #navigation-user', 
                            timeout=3000
                        )
                        if nav_user:
                            await asyncio.sleep(2)  # Give time for page to fully load
                            return True
                    except:
                        pass
                
                # Check for authentication cookies
                cookies = await page.context.cookies()
                auth_cookies = [c for c in cookies if c['name'] in ['.ROBLOSECURITY', 'RBXSessionTracker']]
                if auth_cookies and len(auth_cookies) >= 1:
                    # Verify the cookie has a proper value
                    for cookie in auth_cookies:
                        if cookie['name'] == '.ROBLOSECURITY' and len(cookie['value']) > 50:
                            return True
                
                await asyncio.sleep(2)
                
            except Exception:
                await asyncio.sleep(2)
        
        return False
    
    async def _extract_user_info(self, page: Page) -> Optional[str]:
        """
        Extract user display name from the page
        """
        try:
            # Try different selectors for username/display name
            selectors = [
                '[data-testid="navigation-user"] .text-nav',
                '.navbar-user .text-nav',
                '[data-testid="avatar-card-username"]',
                '.profile-display-name',
                '.header-username'
            ]
            
            for selector in selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=5000)
                    if element:
                        text = await element.text_content()
                        if text and text.strip():
                            return text.strip()
                except:
                    continue
            
            # Try to extract from page content
            title = await page.title()
            if 'Roblox' in title and '-' in title:
                return title.split('-')[0].strip()
                
            return None
            
        except Exception as e:
            print(f"Could not extract user info: {e}")
            return None
    
    async def launch_with_account(self, account: Dict[str, Any]) -> bool:
        """
        Launch Roblox in browser only - no desktop app
        """
        try:
            # Launch browser session only
            return await self._launch_roblox_browser(account, close_after=True)
            
        except Exception as e:
            print(f"❌ Error launching Roblox: {str(e)}")
            return False
    
    async def _launch_roblox_app(self, account: Dict[str, Any]) -> bool:
        """
        Try to launch the Roblox desktop application
        """
        try:
            # Common Roblox installation paths on Windows
            roblox_paths = [
                os.path.expanduser("~/AppData/Local/Roblox/Versions/RobloxPlayerBeta.exe"),
                "C:/Program Files/Roblox/Versions/RobloxPlayerBeta.exe",
                "C:/Program Files (x86)/Roblox/Versions/RobloxPlayerBeta.exe"
            ]
            
            # Find Roblox installation
            roblox_exe = None
            for path in roblox_paths:
                if os.path.exists(path):
                    roblox_exe = path
                    break
            
            # Also check for version folders
            if not roblox_exe:
                versions_dir = os.path.expanduser("~/AppData/Local/Roblox/Versions")
                if os.path.exists(versions_dir):
                    for folder in os.listdir(versions_dir):
                        if folder.startswith("version-"):
                            exe_path = os.path.join(versions_dir, folder, "RobloxPlayerBeta.exe")
                            if os.path.exists(exe_path):
                                roblox_exe = exe_path
                                break
            
            if not roblox_exe:
                print("❌ Roblox desktop app not found")
                return False
            
            # Launch Roblox with a web browser session first
            success = await self._launch_roblox_browser(account, close_after=False)
            if success:
                print("🚀 Launching Roblox desktop application...")
                
                # Launch Roblox app (it will use the browser session)
                subprocess.Popen([roblox_exe], shell=True)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error launching Roblox app: {e}")
            return False
    
    async def _launch_roblox_browser(self, account: Dict[str, Any], close_after: bool = True) -> bool:
        """
        Launch Roblox in browser with saved session and enhanced error handling
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                )
                
                context = await browser.new_context(
                    viewport={'width': 1280, 'height': 720},
                    user_agent=account.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
                    java_script_enabled=True,
                    ignore_https_errors=True
                )
                
                page = await context.new_page()
                
                # First, try to add saved cookies if available
                if account.get('cookies'):
                    try:
                        print(f"🔄 Loading saved cookies for {account['username']}...")
                        # Enhanced cookie processing
                        valid_cookies = []
                        for cookie in account['cookies']:
                            if cookie.get('name') and cookie.get('value'):
                                # Create a clean cookie object
                                clean_cookie = {
                                    'name': cookie['name'],
                                    'value': cookie['value'],
                                    'domain': cookie.get('domain', '.roblox.com'),
                                    'path': cookie.get('path', '/'),
                                }
                                
                                # Add optional fields if they exist and are valid
                                if cookie.get('secure') is not None:
                                    clean_cookie['secure'] = bool(cookie['secure'])
                                if cookie.get('httpOnly') is not None:
                                    clean_cookie['httpOnly'] = bool(cookie['httpOnly'])
                                if cookie.get('sameSite') and cookie['sameSite'] in ['Strict', 'Lax', 'None']:
                                    clean_cookie['sameSite'] = cookie['sameSite']
                                
                                # Handle expires - only add if it's a future timestamp
                                if cookie.get('expires') and cookie['expires'] != -1:
                                    try:
                                        import datetime
                                        expire_time = datetime.datetime.fromtimestamp(cookie['expires'])
                                        if expire_time > datetime.datetime.now():
                                            clean_cookie['expires'] = cookie['expires']
                                    except:
                                        # If expire parsing fails, make it a session cookie
                                        pass
                                
                                # Ensure domain is correct for Roblox
                                if not clean_cookie['domain'].endswith('roblox.com'):
                                    clean_cookie['domain'] = '.roblox.com'
                                
                                # Special handling for .ROBLOSECURITY cookie
                                if cookie['name'] == '.ROBLOSECURITY':
                                    clean_cookie['secure'] = True
                                    clean_cookie['httpOnly'] = True
                                    clean_cookie['sameSite'] = 'None'
                                    clean_cookie['domain'] = '.roblox.com'
                                
                                valid_cookies.append(clean_cookie)
                        
                        if valid_cookies:
                            # Clear any existing cookies first
                            try:
                                await context.clear_cookies()
                            except:
                                pass  # Ignore clear errors
                            
                            # Add cookies one by one with error handling
                            added_count = 0
                            for cookie in valid_cookies:
                                try:
                                    await context.add_cookies([cookie])
                                    added_count += 1
                                    if cookie['name'] == '.ROBLOSECURITY':
                                        print(f"✓ Successfully added .ROBLOSECURITY cookie")
                                except Exception as e:
                                    print(f"⚠️  Failed to add cookie {cookie['name']}: {e}")
                                    # Try with minimal cookie info
                                    try:
                                        minimal_cookie = {
                                            'name': cookie['name'],
                                            'value': cookie['value'],
                                            'domain': '.roblox.com',
                                            'path': '/'
                                        }
                                        await context.add_cookies([minimal_cookie])
                                        added_count += 1
                                        print(f"✓ Added {cookie['name']} with minimal config")
                                    except Exception as e2:
                                        print(f"❌ Completely failed to add {cookie['name']}: {e2}")
                            
                            print(f"✓ Successfully loaded {added_count}/{len(valid_cookies)} cookies")
                            
                            # Verify .ROBLOSECURITY cookie was added
                            test_cookies = await context.cookies()
                            roblosecurity_found = any(c['name'] == '.ROBLOSECURITY' for c in test_cookies)
                            if roblosecurity_found:
                                print("✅ .ROBLOSECURITY cookie verified in context")
                            else:
                                print("❌ .ROBLOSECURITY cookie not found in context after adding")
                                
                        else:
                            print("⚠️  No valid cookies found in account data")
                    except Exception as e:
                        print(f"⚠️  Critical error adding cookies: {e}")
                        # Continue without cookies
                        pass
                else:
                    print("⚠️  No saved cookies available - will need to login")
                
                # Navigate to Roblox home page
                print("🌐 Navigating to Roblox...")
                try:
                    await page.goto(self.roblox_home_url, wait_until='networkidle', timeout=30000)
                except Exception as e:
                    print(f"⚠️  Navigation timeout, trying alternative approach: {e}")
                    await page.goto(self.roblox_home_url, wait_until='domcontentloaded')
                    await asyncio.sleep(3)
                
                # Check if login is still valid
                print("🔍 Verifying login status...")
                is_logged_in = await self._verify_login_status(page)
                
                if is_logged_in:
                    print(f"✅ Successfully logged in as: {account['username']}")
                    
                    # Navigate to games page
                    try:
                        print("🎮 Navigating to games page...")
                        await page.goto("https://www.roblox.com/games", wait_until='networkidle', timeout=15000)
                    except Exception as e:
                        print(f"⚠️  Games page navigation error: {str(e)}, continuing anyway...")
                    
                    if not close_after:
                        print("🌐 Browser session ready! You can browse and play games directly in the browser.")
                        # Keep browser open for a while to maintain session
                        await asyncio.sleep(5)
                    else:
                        print("🎮 Browser ready! You can now play Roblox games directly in the browser.")
                        print("💡 Tip: Browse games and click 'Play' to start playing directly in browser.")
                        print("🌐 Browser will stay open - close manually when done playing.")
                        
                        # Keep browser open indefinitely until user closes it
                        try:
                            # Wait for user to close browser manually
                            while not page.is_closed():
                                await asyncio.sleep(1)
                        except:
                            pass
                    
                    # Don't auto-close browser anymore
                    # if close_after:
                    #     await browser.close()
                    
                    return True
                else:
                    print("❌ Session expired or invalid.")
                    
                    # Offer to refresh session
                    print("🔄 Would you like to refresh the session? This will open a login page.")
                    try:
                        # Give user choice to refresh session
                        refresh_choice = input("Press 'y' to refresh session, or any other key to cancel: ").lower().strip()
                        
                        if refresh_choice == 'y':
                            print("🔄 Refreshing session...")
                            await browser.close()
                            
                            # Try to refresh session
                            refresh_success = await self.refresh_account_session(account['username'])
                            if refresh_success:
                                print("✅ Session refreshed! Please try launching again.")
                                return True
                            else:
                                print("❌ Failed to refresh session")
                                return False
                        else:
                            await browser.close()
                            print("❌ Session refresh cancelled")
                            return False
                            
                    except KeyboardInterrupt:
                        await browser.close()
                        print("\n❌ Operation cancelled by user")
                        return False
                    
        except Exception as e:
            print(f"❌ Error launching browser session: {e}")
            return False
    
    async def _verify_login_status(self, page: Page) -> bool:
        """
        Verify if the user is still logged in with enhanced checks
        """
        try:
            # Wait for page to fully load
            await page.wait_for_load_state('networkidle', timeout=15000)
            await asyncio.sleep(3)  # Additional wait for dynamic content
            
            current_url = page.url
            print(f"🔍 Checking login status on: {current_url}")
            
            # First check: If we're on login page, definitely not logged in
            if any(keyword in current_url.lower() for keyword in ['login', 'authenticate', 'signin']):
                print("❌ Redirected to login page")
                return False
            
            # Second check: Enhanced cookie validation
            cookies = await page.context.cookies()
            print(f"🔍 Found {len(cookies)} total cookies")
            
            # Find all Roblox related cookies
            roblox_cookies = [c for c in cookies if 'roblox' in c.get('domain', '').lower()]
            print(f"🔍 Found {len(roblox_cookies)} Roblox cookies")
            
            auth_cookie = None
            for cookie in cookies:
                if cookie['name'] == '.ROBLOSECURITY':
                    auth_cookie = cookie
                    break
            
            if not auth_cookie:
                # Try alternative cookie names
                alt_names = ['ROBLOSECURITY', '_RobloxSecurity', 'RobloxSecurity']
                for name in alt_names:
                    alt_cookie = next((c for c in cookies if c['name'] == name), None)
                    if alt_cookie:
                        auth_cookie = alt_cookie
                        print(f"✓ Found alternative auth cookie: {name}")
                        break
            
            if not auth_cookie:
                print("❌ No authentication cookie found")
                # Try to see what cookies we do have
                cookie_names = [c['name'] for c in cookies if 'roblox' in c.get('domain', '').lower()]
                if cookie_names:
                    print(f"📋 Available Roblox cookies: {', '.join(cookie_names)}")
                return False
            
            cookie_value = auth_cookie.get('value', '')
            if len(cookie_value) < 30:  # Reduced minimum length
                print(f"❌ Auth cookie too short: {len(cookie_value)} chars")
                return False
            
            print(f"✓ Found valid auth cookie: {cookie_value[:30]}... (length: {len(cookie_value)})")
            
            # Third check: Try to access Roblox API endpoint to verify auth
            try:
                print("🔍 Verifying authentication via API...")
                response = await page.request.get("https://users.roblox.com/v1/users/authenticated", 
                                                fail_on_status_code=False)
                if response.status == 200:
                    user_data = await response.json()
                    if user_data and user_data.get('id'):
                        print(f"✅ API verification successful - User ID: {user_data.get('id')}")
                        return True
                else:
                    print(f"⚠️  API returned status {response.status}")
            except Exception as e:
                print(f"⚠️  API check failed: {e}")
            
            # Fourth check: Look for user navigation elements with multiple selectors
            user_selectors = [
                '[data-testid="navigation-user"]',
                '.navbar-user',
                '#navigation-user',
                '[data-testid="avatar-card-username"]',
                '.menu-user-name',
                '.header-username',
                '.nav-robux-amount',
                '[class*="user"]',
                '[id*="user"]',
                '.navbar .navbar-user',
                '.top-nav-user',
                '.app-header .user'
            ]
            
            for selector in user_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=2000)
                    if element:
                        text = await element.text_content()
                        if text and text.strip() and not text.strip().lower() in ['login', 'sign in']:
                            print(f"✓ Found user element: {text.strip()[:30]}...")
                            return True
                except:
                    continue
            
            # Fifth check: Try to get user data from JavaScript
            try:
                user_data = await page.evaluate("""
                    () => {
                        // Check for Roblox user data in global variables
                        if (window.Roblox) {
                            if (window.Roblox.CurrentUser && window.Roblox.CurrentUser.userId) {
                                return {
                                    source: 'Roblox.CurrentUser',
                                    userId: window.Roblox.CurrentUser.userId,
                                    displayName: window.Roblox.CurrentUser.displayName,
                                    username: window.Roblox.CurrentUser.name
                                };
                            }
                            
                            // Check for other user data locations
                            if (window.Roblox.Users && window.Roblox.Users.authenticatedUserId) {
                                return {
                                    source: 'Roblox.Users',
                                    userId: window.Roblox.Users.authenticatedUserId
                                };
                            }
                        }
                        
                        // Check for meta tags with user info
                        const userMeta = document.querySelector('meta[name="user-data"]');
                        if (userMeta) {
                            try {
                                const content = userMeta.getAttribute('data-userid') || userMeta.getAttribute('content');
                                if (content) {
                                    const userData = JSON.parse(content);
                                    return {
                                        source: 'meta[user-data]',
                                        ...userData
                                    };
                                }
                            } catch(e) {}
                        }
                        
                        // Check for user ID in script tags
                        const scripts = document.querySelectorAll('script');
                        for (const script of scripts) {
                            const content = script.textContent || '';
                            const userIdMatch = content.match(/["']?userId["']?\\s*:\\s*(\\d+)/);
                            if (userIdMatch) {
                                return {
                                    source: 'script-userId',
                                    userId: parseInt(userIdMatch[1])
                                };
                            }
                        }
                        
                        return null;
                    }
                """)
                
                if user_data and user_data.get('userId'):
                    print(f"✅ JavaScript verification successful: {user_data}")
                    return True
                    
            except Exception as e:
                print(f"⚠️  JavaScript check failed: {e}")
            
            # Sixth check: Check page title and content for login indicators
            title = await page.title()
            if any(keyword in title.lower() for keyword in ['home', 'dashboard', 'profile', 'discover']) and 'login' not in title.lower():
                page_content = await page.content()
                if any(indicator in page_content.lower() for indicator in ['logout', 'sign out', 'account settings']):
                    print("✓ Found logout/settings in page content - likely logged in")
                    return True
            
            # Seventh check: Look for specific Roblox logged-in page elements
            logged_in_selectors = [
                '.robux-display',
                '.user-menu',
                '.notification-blue',
                '[data-testid="user-avatar"]',
                '.navbar-robux',
                '.top-nav .user'
            ]
            
            for selector in logged_in_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        print(f"✓ Found logged-in indicator: {selector}")
                        return True
                except:
                    continue
            
            print("❌ No login indicators found despite having auth cookie")
            return False
            
        except Exception as e:
            print(f"❌ Error verifying login status: {e}")
            return False
    
    async def refresh_account_session(self, username: str) -> bool:
        """
        Refresh account session by re-logging in with enhanced flow
        """
        print(f"🔄 Refreshing session for: {username}")
        
        try:
            # First check if account exists
            account = self.db.get_account(username)
            if not account:
                print(f"❌ Account '{username}' not found in database")
                return False
            
            print(f"🔄 Opening browser for session refresh...")
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=False,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--no-sandbox'
                    ]
                )
                
                context = await browser.new_context(
                    viewport={'width': 1280, 'height': 720},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                
                page = await context.new_page()
                
                # Clear any existing cookies and go to login page
                await page.goto(self.roblox_login_url, wait_until='networkidle')
                
                print("🌐 Browser opened for session refresh!")
                print(f"👤 Please login with account: {username}")
                print("⏳ Waiting for login completion...")
                
                # Wait for user to login
                login_successful = await self._wait_for_login(page)
                
                if login_successful:
                    print("✅ Login successful! Updating session data...")
                    
                    # Get new cookies and session data
                    new_cookies = await context.cookies()
                    new_user_agent = await page.evaluate("navigator.userAgent")
                    display_name = await self._extract_user_info(page)
                    
                    # Update account in database
                    update_success = self.db.update_account(
                        username=username,
                        display_name=display_name or account.get('display_name'),
                        cookies=new_cookies,
                        user_agent=new_user_agent,
                        session_data={'logged_in': True, 'refresh_time': time.time()}
                    )
                    
                    await browser.close()
                    
                    if update_success:
                        print(f"✅ Session refreshed successfully for '{username}'!")
                        return True
                    else:
                        print("❌ Failed to update account data in database")
                        return False
                else:
                    print("❌ Login timeout or failed during refresh")
                    await browser.close()
                    return False
                    
        except Exception as e:
            print(f"❌ Error refreshing session: {str(e)}")
            return False
    
    def get_roblox_protocol_handler(self) -> bool:
        """
        Check if Roblox protocol handler is available (roblox://)
        """
        try:
            # Try to find Roblox in registry (Windows specific)
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "roblox")
                winreg.CloseKey(key)
                return True
            except WindowsError:
                return False
        except ImportError:
            # Not on Windows or winreg not available
            return False
    
    async def validate_account_session(self, username: str) -> bool:
        """
        Validate if an account's session is still active without opening browser
        """
        try:
            account = self.db.get_account(username)
            if not account or not account.get('cookies'):
                return False
            
            # Check if we have the essential cookie
            cookies = account['cookies']
            auth_cookie = next((c for c in cookies if c['name'] == '.ROBLOSECURITY'), None)
            if not auth_cookie or len(auth_cookie.get('value', '')) < 30:
                print(f"❌ {username}: No valid auth cookie in database")
                return False
            
            print(f"🔍 Validating session for {username}...")
            
            # Quick validation using headless browser
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=account.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                )
                
                # Add cookies with enhanced processing
                try:
                    valid_cookies = []
                    for cookie in cookies:
                        if cookie.get('name') and cookie.get('value'):
                            # Create clean cookie with proper attributes
                            clean_cookie = {
                                'name': cookie.get('name', ''),
                                'value': cookie.get('value', ''),
                                'domain': cookie.get('domain', '.roblox.com'),
                                'path': cookie.get('path', '/'),
                                'secure': cookie.get('secure', True),
                                'httpOnly': cookie.get('httpOnly', False)
                            }
                            
                            # Fix domain issues
                            if not clean_cookie['domain'].endswith('roblox.com'):
                                clean_cookie['domain'] = '.roblox.com'
                            
                            # Sanitize sameSite attribute
                            same_site = cookie.get('sameSite', 'Lax')
                            if same_site in ['Strict', 'Lax', 'None']:
                                clean_cookie['sameSite'] = same_site
                            else:
                                clean_cookie['sameSite'] = 'Lax'
                            
                            valid_cookies.append(clean_cookie)
                    
                    await context.add_cookies(valid_cookies)
                except Exception as e:
                    print(f"⚠️  Error adding cookies for validation: {e}")
                
                page = await context.new_page()
                
                try:
                    # Try API endpoint first (fastest method)
                    response = await page.request.get("https://users.roblox.com/v1/users/authenticated", 
                                                    fail_on_status_code=False)
                    if response.status == 200:
                        user_data = await response.json()
                        if user_data and user_data.get('id'):
                            print(f"✅ {username}: API validation successful")
                            await browser.close()
                            return True
                except Exception as e:
                    print(f"⚠️  API validation failed for {username}: {e}")
                
                # Fallback: Load home page and check
                try:
                    await page.goto("https://www.roblox.com/home", wait_until='domcontentloaded', timeout=10000)
                    
                    # Check for auth cookie after page load
                    new_cookies = await context.cookies()
                    auth_cookie_after = next((c for c in new_cookies if c['name'] == '.ROBLOSECURITY'), None)
                    
                    await browser.close()
                    
                    is_valid = auth_cookie_after is not None and len(auth_cookie_after.get('value', '')) > 30
                    print(f"{'✅' if is_valid else '❌'} {username}: Page validation {'successful' if is_valid else 'failed'}")
                    return is_valid
                    
                except Exception as e:
                    await browser.close()
                    print(f"❌ {username}: Page validation error: {e}")
                    return False
                
        except Exception as e:
            print(f"❌ {username}: Validation error: {e}")
            return False
    
    async def clean_expired_sessions(self) -> int:
        """
        Check all accounts and mark expired sessions as inactive
        """
        accounts = self.db.get_active_accounts()
        expired_count = 0
        
        print(f"🔍 Checking {len(accounts)} active accounts for expired sessions...")
        
        for account in accounts:
            try:
                is_valid = await self.validate_account_session(account['username'])
                if not is_valid:
                    print(f"❌ Session expired for: {account['username']}")
                    self.db.update_account_status(account['username'], False)
                    expired_count += 1
                else:
                    print(f"✅ Session valid for: {account['username']}")
            except Exception as e:
                print(f"⚠️  Error checking {account['username']}: {e}")
        
        print(f"🧹 Found {expired_count} expired sessions")
        return expired_count