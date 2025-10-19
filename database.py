import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class AccountDatabase:
    def __init__(self, db_path: str = "roblox_accounts.db"):
        """Initialize the database"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        display_name TEXT,
                        cookies TEXT,
                        user_agent TEXT,
                        session_data TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create index for faster searches
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_username ON accounts(username)
                ''')
                
                conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    def account_exists(self, username: str) -> bool:
        """Check if an account with the given username exists"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT 1 FROM accounts WHERE username = ?",
                    (username,)
                )
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking if account exists: {e}")
            return False
    
    def add_account(self, username: str, display_name: Optional[str] = None, 
                   cookies: Optional[List[Dict]] = None, user_agent: Optional[str] = None, 
                   session_data: Optional[Dict] = None) -> bool:
        """Add a new account to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cookies_json = json.dumps(cookies) if cookies else None
                session_json = json.dumps(session_data) if session_data else None
                
                conn.execute('''
                    INSERT INTO accounts 
                    (username, display_name, cookies, user_agent, session_data)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, display_name, cookies_json, user_agent, session_json))
                
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            print(f"Account '{username}' already exists!")
            return False
        except Exception as e:
            print(f"Error adding account: {e}")
            return False
    
    def get_account(self, username: str) -> Optional[Dict]:
        """Get account data by username"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT * FROM accounts WHERE username = ?
                ''', (username,))
                
                row = cursor.fetchone()
                if row:
                    account = dict(row)
                    # Parse JSON fields
                    if account['cookies']:
                        account['cookies'] = json.loads(account['cookies'])
                    if account['session_data']:
                        account['session_data'] = json.loads(account['session_data'])
                    return account
                return None
        except Exception as e:
            print(f"Error getting account: {e}")
            return None
    
    def get_all_accounts(self) -> List[Dict]:
        """Get all accounts from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT id, username, display_name, is_active, created_at, updated_at
                    FROM accounts 
                    ORDER BY created_at DESC
                ''')
                
                accounts = []
                for row in cursor.fetchall():
                    account = dict(row)
                    # Format the date for better display
                    if account['created_at']:
                        try:
                            dt = datetime.fromisoformat(account['created_at'])
                            account['created_at'] = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            pass
                    accounts.append(account)
                
                return accounts
        except Exception as e:
            print(f"Error getting all accounts: {e}")
            return []
    
    def update_account(self, username: str, display_name: Optional[str] = None,
                      cookies: Optional[List[Dict]] = None, user_agent: Optional[str] = None,
                      session_data: Optional[Dict] = None) -> bool:
        """Update account data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                updates = []
                values = []
                
                if display_name is not None:
                    updates.append("display_name = ?")
                    values.append(display_name)
                
                if cookies is not None:
                    updates.append("cookies = ?")
                    values.append(json.dumps(cookies))
                
                if user_agent is not None:
                    updates.append("user_agent = ?")
                    values.append(user_agent)
                
                if session_data is not None:
                    updates.append("session_data = ?")
                    values.append(json.dumps(session_data))
                
                if not updates:
                    return True
                
                updates.append("updated_at = CURRENT_TIMESTAMP")
                values.append(username)
                
                query = f"UPDATE accounts SET {', '.join(updates)} WHERE username = ?"
                conn.execute(query, values)
                conn.commit()
                
                return conn.total_changes > 0
        except Exception as e:
            print(f"Error updating account: {e}")
            return False
    
    def update_account_status(self, username: str, is_active: bool) -> bool:
        """Update account active status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    UPDATE accounts 
                    SET is_active = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE username = ?
                ''', (is_active, username))
                
                conn.commit()
                return conn.total_changes > 0
        except Exception as e:
            print(f"Error updating account status: {e}")
            return False
    
    def remove_account(self, username: str) -> bool:
        """Remove an account from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM accounts WHERE username = ?", (username,))
                conn.commit()
                return conn.total_changes > 0
        except Exception as e:
            print(f"Error removing account: {e}")
            return False
    
    def get_active_accounts(self) -> List[Dict]:
        """Get only active accounts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT * FROM accounts 
                    WHERE is_active = 1 
                    ORDER BY created_at DESC
                ''')
                
                accounts = []
                for row in cursor.fetchall():
                    account = dict(row)
                    # Parse JSON fields
                    if account['cookies']:
                        account['cookies'] = json.loads(account['cookies'])
                    if account['session_data']:
                        account['session_data'] = json.loads(account['session_data'])
                    accounts.append(account)
                
                return accounts
        except Exception as e:
            print(f"Error getting active accounts: {e}")
            return []
    
    def cleanup_inactive_accounts(self) -> int:
        """Remove accounts that are marked as inactive"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("DELETE FROM accounts WHERE is_active = 0")
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error cleaning up inactive accounts: {e}")
            return 0
    
    def get_account_count(self) -> Dict[str, int]:
        """Get count of total and active accounts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) as total FROM accounts")
                total = cursor.fetchone()[0]
                
                cursor = conn.execute("SELECT COUNT(*) as active FROM accounts WHERE is_active = 1")
                active = cursor.fetchone()[0]
                
                return {"total": total, "active": active}
        except Exception as e:
            print(f"Error getting account count: {e}")
            return {"total": 0, "active": 0}
    
    def update_account_cookies(self, username: str, cookies: List[Dict], user_agent: str) -> bool:
        """Update cookies and user agent for an existing account"""
        try:
            cookies_json = json.dumps(cookies) if cookies else None
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """UPDATE accounts 
                       SET cookies = ?, user_agent = ?, updated_at = CURRENT_TIMESTAMP, is_active = 1
                       WHERE username = ?""",
                    (cookies_json, user_agent, username)
                )
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                else:
                    return False
                    
        except Exception as e:
            print(f"Error updating account cookies: {e}")
            return False
    
    def backup_database(self, backup_path: Optional[str] = None) -> bool:
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"roblox_accounts_backup_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            print(f"Database backed up to: {backup_path}")
            return True
        except Exception as e:
            print(f"Error creating database backup: {e}")
            return False