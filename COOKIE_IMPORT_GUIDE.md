# Cookie Import Guide

This guide explains how to import Roblox account cookies from JSON files.

## Supported JSON Formats

### 1. Array of Cookie Objects (Recommended)
```json
[
    {
        "name": ".ROBLOSECURITY",
        "value": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_YOUR_ACTUAL_COOKIE_VALUE",
        "domain": ".roblox.com",
        "path": "/",
        "secure": true,
        "httpOnly": true,
        "sameSite": "None"
    },
    {
        "name": "RBXEventTrackerV2", 
        "value": "CreateDate=10/19/2025&rbxid=123456789&browserid=987654321",
        "domain": ".roblox.com",
        "path": "/",
        "secure": true,
        "httpOnly": false,
        "sameSite": "Lax"
    }
]
```

### 2. Simple Key-Value Object
```json
{
    ".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_YOUR_ACTUAL_COOKIE_VALUE",
    "RBXEventTrackerV2": "CreateDate=10/19/2025&rbxid=123456789&browserid=987654321",
    "rbx-ip2": "v=1&ip=127.0.0.1",
    "RBXSource": "rbx_acquisition_time=10/19/2025&rbx_acquisition_referrer=https://www.roblox.com/"
}
```

## How to Export Cookies from Browser

### Chrome/Edge
1. Open Developer Tools (F12)
2. Go to Application tab → Cookies → https://www.roblox.com
3. Right-click on cookies → Copy all as JSON (using extensions)
4. Or manually copy each cookie value

### Firefox  
1. Open Developer Tools (F12)
2. Go to Storage tab → Cookies → https://www.roblox.com
3. Right-click → Copy all (using extensions)
4. Or manually copy each cookie value

## Important Cookies

### Essential Cookies:
- **.ROBLOSECURITY** - Main authentication cookie (REQUIRED)
- **RBXEventTrackerV2** - Event tracking
- **rbx-ip2** - IP tracking
- **RBXSessionTracker** - Session management

### Optional Cookies:
- RBXSource - Referrer tracking
- rbxas - Additional session data
- RBXViralAcquisition - Marketing data
- rbx-csrf - CSRF protection

## Usage Steps

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Select option 8** - Import Account from JSON

3. **Enter username** - Type the account username/display name

4. **Provide JSON file path** - Either:
   - Type the full path to your JSON file
   - Drag and drop the JSON file into the terminal

5. **Review import summary** - Check:
   - Total cookies found
   - Roblox-specific cookies
   - .ROBLOSECURITY presence

6. **Test session (optional)** - Verify the imported cookies work

## Troubleshooting

### Common Issues:

1. **"No .ROBLOSECURITY cookie found"**
   - Make sure you copied the main authentication cookie
   - Check that you were logged into Roblox when exporting

2. **"Invalid JSON format"**
   - Validate your JSON using online JSON validators
   - Check for missing quotes or commas

3. **"Session test failed"**
   - Cookies might be expired
   - Try logging into Roblox manually to refresh cookies
   - Export cookies again from an active session

### Tips:
- Always export cookies from an active, logged-in Roblox session
- Don't share your .ROBLOSECURITY cookie with anyone
- Test imported accounts before relying on them
- Keep backup of working cookie files

## Security Notes

⚠️ **IMPORTANT SECURITY WARNINGS:**

1. **Never share your .ROBLOSECURITY cookie** - This gives full access to your account
2. **Store JSON files securely** - They contain sensitive authentication data
3. **Use fresh cookies** - Export cookies from recently active sessions
4. **Enable 2FA** - Add extra security to your Roblox account
5. **Regular updates** - Re-export cookies periodically as they expire

## Example Files

The application includes two example files:
- `example_cookies.json` - Full format with all properties
- `example_cookies_simple.json` - Simple key-value format

**Note:** These contain placeholder values - replace with your actual cookies!