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
