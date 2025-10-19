#!/usr/bin/env python3
from database import AccountDatabase
import json

db = AccountDatabase()
accounts = db.get_all_accounts()
for account in accounts:
    print(f'Account: {account["username"]}')
    full_account = db.get_account(account['username'])
    if full_account and full_account.get('cookies'):
        cookies = full_account['cookies']
        print(f'  Cookies count: {len(cookies)}')
        for cookie in cookies:
            print(f'    {cookie["name"]}: {cookie["value"][:30]}...')
        auth_cookie = next((c for c in cookies if c['name'] == '.ROBLOSECURITY'), None)
        if auth_cookie:
            print(f'  ✓ Has .ROBLOSECURITY cookie: {len(auth_cookie["value"])} chars')
        else:
            print(f'  ❌ No .ROBLOSECURITY cookie found')
    else:
        print(f'  ❌ No cookies stored')
    print()