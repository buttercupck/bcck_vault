# Cookie Authentication Error Report - HubSpot Testing

**Date:** 2025-10-17
**Issue:** Unable to use curl/httpx for authenticated requests with cookies.txt
**Resolution:** Created Python-based authentication wrapper (test_auth.py)

---

## Problem Statement

Attempted to validate Track B findings using authenticated requests to HubSpot's app.hubspot.com with cookies stored in `cookies.txt`. All shell-based HTTP clients (curl, httpx, wget) failed due to special character handling in cookie values.

---

## Root Cause

The HubSpot cookie string contains special characters that break shell argument parsing:
- Parentheses: `(`, `)`
- Curly braces: `{`, `}`
- Percent encoding: `%7C`, `%2B`
- Embedded JSON: `{"i_l":0}`

**Example problematic cookie:**
```
g_state={"i_l":0}; _hjSession_35118=eyJpZCI6IjU2YjEzZjljLTdmYjgtNWY3Zi1iNzA1...
```

---

## Failed Attempts

### Attempt 1: Direct curl with Cookie header
```bash
curl -H "Cookie: $(cat cookies.txt)" https://app.hubspot.com/contacts
```
**Error:** `curl: option : blank argument where content is expected`

**Analysis:** Shell expansion of `$(...)` with special chars breaks argument parsing

---

### Attempt 2: Cookie file with curl -b flag
```bash
curl -b /tmp/cookies.txt https://app.hubspot.com/contacts
```
**Error:** `curl: option : blank argument where content is expected`

**Analysis:** Curl's `-b` flag expects Netscape cookie format, not raw Cookie header string

---

### Attempt 3: Cleaned cookies with sed/tr
```bash
sed 's/^Cookie: //' cookies.txt | tr -d "'" > /tmp/cookies_clean.txt
curl -H "Cookie: $(cat /tmp/cookies_clean.txt)" https://app.hubspot.com/contacts
```
**Error:** `curl: option : blank argument where content is expected`

**Analysis:** Removing quotes doesn't fix embedded JSON and parentheses

---

### Attempt 4: httpx with header flag
```bash
echo "app.hubspot.com" | httpx -H "Cookie: $(cat /tmp/cookies.txt)"
```
**Error:** Silent failure - no output

**Analysis:** httpx also fails on complex cookie parsing

---

### Attempt 5: wget with header
```bash
wget --header="Cookie: $(cat /tmp/cookies.txt)" https://app.hubspot.com/contacts
```
**Error:** `(eval):1: permission denied`

**Analysis:** Shell evaluation error on special characters

---

## Solution: Python-based HTTP Client

Created `/tmp/test_auth.py` to handle cookies programmatically:

### Initial Version (SSL Error)
```python
import urllib.request

cookies = open('/tmp/hubspot_cookies.txt').read().strip()
req = urllib.request.Request('https://app.hubspot.com/contacts')
req.add_header('Cookie', cookies)
response = urllib.request.urlopen(req)
```

**Error:** `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed`

**Analysis:** Python on macOS requires certificate chain verification

---

### Final Working Version

```python
import urllib.request
import ssl

# Bypass SSL verification for testing
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cookies = open('/tmp/hubspot_cookies.txt').read().strip()

req = urllib.request.Request('https://app.hubspot.com/contacts')
req.add_header('Cookie', cookies)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

response = urllib.request.urlopen(req, context=ctx)
content = response.read().decode('utf-8', errors='ignore')

# Validate authentication
if 'contacts' in content or 'dashboard' in content:
    print("✓ AUTHENTICATED")
else:
    print("✗ NOT AUTHENTICATED")
```

**Result:**
```
✓ Status: 200
✓ URL: https://app.hubspot.com/contacts
✓ Result: AUTHENTICATED (got app content)
✓ Cookies are working!
```

---

## Why Python Succeeded Where curl Failed

| Aspect | curl/httpx/wget | Python urllib |
|--------|----------------|---------------|
| Cookie parsing | Shell string parsing → breaks on special chars | Direct string reading → no parsing |
| SSL handling | Uses system certificates | Programmatic SSL context control |
| Header encoding | Shell escaping required | Native string handling |
| Debugging | Opaque errors | Exception details |
| Complex cookies | Breaks on `{`, `(`, `%` | Handles all characters |

**Key Insight:** Shell-based tools require escaping for shell evaluation, then HTTP encoding. Python skips shell layer entirely.

---

## Lessons Learned

### 1. Cookie Format Complexity
Modern web apps use JSON in cookies (g_state, _hjSession) which breaks shell argument parsing. Solutions:
- Use programming languages (Python, Node.js) instead of shell scripts
- Convert to Netscape cookie jar format for curl
- Use browser automation (Playwright, Selenium) for complex sessions

### 2. SSL Certificate Handling
macOS Python requires explicit SSL context configuration. For testing:
```python
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
```

**Security Note:** Only use for testing. Production code should verify certificates.

### 3. Authentication Validation
Check response content for keywords:
- **Authenticated:** `contacts`, `dashboard`, `portal`
- **Not authenticated:** `login`, `password`, `signin`

---

## Recommendations for Future Testing

### Option 1: Use test_auth.py wrapper
```python
# Extend test_auth.py for different endpoints
def fetch_authenticated(url):
    req = urllib.request.Request(url)
    req.add_header('Cookie', cookies)
    req.add_header('User-Agent', 'Mozilla/5.0...')
    return urllib.request.urlopen(req, context=ctx).read()
```

### Option 2: Convert to Netscape format
```bash
# Create proper cookie jar
cat > cookies.jar << EOF
# Netscape HTTP Cookie File
.hubspot.com	TRUE	/	FALSE	0	hubspotutk	bc0321ec2df462fdb39f17eb407fac85
...
EOF

curl -b cookies.jar https://app.hubspot.com/contacts
```

### Option 3: Use Playwright MCP
Since we have Chrome DevTools MCP available, use that for authenticated browser automation:
```javascript
mcp__chrome-devtools__navigate_page({ url: 'https://app.hubspot.com/contacts' })
// Cookies automatically handled by browser
```

---

## Impact on Track B Peer Review

**Original Plan:** Use curl/httpx to validate findings against live endpoints

**Actual Method:** Python script for HTTP requests with cookie authentication

**Status:** ✅ Authentication working - can proceed with Track B validation

**Files Created:**
- `/tmp/test_auth.py` - Python authentication wrapper
- `/tmp/hubspot_cookies.txt` - Cleaned cookie string

---

## Next Steps

1. Extend `test_auth.py` to fetch specific endpoints from Track B findings
2. Extract Portal ID from authenticated response
3. Validate localStorage keys via JavaScript injection
4. Test CHIRP error patterns
5. Verify error reporting infrastructure

---

## Code Artifacts

### test_auth.py (Final Version)
```python
import sys
import urllib.request
import ssl

# Create unverified context for testing
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cookies = open('/tmp/hubspot_cookies.txt').read().strip()

req = urllib.request.Request('https://app.hubspot.com/contacts')
req.add_header('Cookie', cookies)
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

try:
    response = urllib.request.urlopen(req, context=ctx)
    print(f"✓ Status: {response.status}")
    print(f"✓ URL: {response.url}")
    content = response.read().decode('utf-8', errors='ignore')

    # Check for authentication indicators
    if 'login' in content.lower() and 'password' in content.lower():
        print("\n✗ Result: NOT AUTHENTICATED (redirected to login)")
    elif 'contacts' in content or 'dashboard' in content or 'portal' in content:
        print("\n✓ Result: AUTHENTICATED (got app content)")
        print("✓ Cookies are working!")
    else:
        print("\n? Result: UNKNOWN (check content)")

except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
except Exception as e:
    print(f"Error: {e}")
```

### Usage
```bash
python3 /tmp/test_auth.py
```

---

**Report Status:** Authentication issue resolved - proceeding with Track B validation
**Time Lost:** ~15 minutes debugging cookie handling
**Time Saved:** Python solution reusable for all future authenticated requests
