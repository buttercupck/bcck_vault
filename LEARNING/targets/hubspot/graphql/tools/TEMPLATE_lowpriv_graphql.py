#!/usr/bin/env python3
"""
HubSpot GraphQL Testing - Low-Privileged Account Template
Replace configuration values with your low-privileged account details
"""
import urllib.request
import ssl
import json

# ============================================================================
# CONFIGURATION - REPLACE WITH YOUR LOW-PRIVILEGED ACCOUNT VALUES
# ============================================================================

# Your configuration
HUBLET = "na2"  # Your hublet (na1, na2, eu1, etc.) - check URL after login
PORTAL_ID = "YOUR_PORTAL_ID_HERE"  # Your low-priv portal ID

# Your cookies (copy from browser DevTools → Network → graphql request → Copy as cURL)
COOKIE_HEADER = """
PASTE_YOUR_FULL_COOKIE_HEADER_HERE
""".strip()

# Your CSRF token (from csrf.app or hubspotapi-csrf cookie value)
CSRF_TOKEN = "YOUR_CSRF_TOKEN_HERE"

# ============================================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================================

# SSL context (disable verification for testing)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Build endpoint URL
base_url = f"https://app-{HUBLET}.hubspot.com"
endpoint = "/api/graphql/crm"
params = f"?portalId={PORTAL_ID}&clienttimeout=14000&hs_static_app=crm-index-ui&hs_static_app_version=2.49724"
full_url = f"{base_url}{endpoint}{params}"

def test_graphql(query_name, query):
    """Execute GraphQL query and display results"""
    print(f"\n{'='*70}")
    print(f"TEST: {query_name}")
    print('='*70)

    # Build request
    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', COOKIE_HEADER)
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-HubSpot-CSRF-hubspotapi', CSRF_TOKEN)
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0')
    req.add_header('Origin', base_url)
    req.add_header('Referer', f'{base_url}/contacts/{PORTAL_ID}/objects/0-1/views/all/list')

    # Request body
    body = {"query": query}
    data = json.dumps(body).encode('utf-8')

    try:
        # Execute request
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=15)
        content = response.read().decode('utf-8')

        # Parse response
        json_response = json.loads(content)

        if 'data' in json_response:
            print(f"✓ SUCCESS - GraphQL returned data")
            print(json.dumps(json_response['data'], indent=2)[:500])
            if len(json.dumps(json_response['data'])) > 500:
                print("... (truncated)")
            return True, json_response['data']

        elif 'errors' in json_response:
            print(f"✗ GraphQL Errors:")
            for error in json_response['errors']:
                print(f"  - {error.get('message', error)}")
            return False, json_response['errors']

        else:
            print(f"? Unexpected response format")
            print(json.dumps(json_response, indent=2)[:300])
            return False, None

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")

        if e.code == 401:
            print(f"  → Cookies expired or invalid - recapture from browser")
        elif e.code == 403:
            print(f"  → CSRF token issue or forbidden resource")
        elif e.code == 404:
            print(f"  → Wrong endpoint (check HUBLET and path)")
        elif e.code == 488:
            print(f"  → Wrong hublet - check error message for correct one")

        try:
            error = e.read().decode('utf-8')
            error_json = json.loads(error)
            print(f"  Error details: {json.dumps(error_json, indent=2)}")
        except:
            pass

        return False, None

    except Exception as e:
        print(f"✗ Error: {e}")
        return False, None

# Main execution
if __name__ == "__main__":
    print("="*70)
    print("LOW-PRIVILEGED GRAPHQL TESTING")
    print("="*70)
    print(f"Portal ID: {PORTAL_ID}")
    print(f"Hublet: {HUBLET}")
    print(f"Endpoint: {full_url}")
    print(f"Cookie length: {len(COOKIE_HEADER)} chars")
    print(f"CSRF token: {CSRF_TOKEN[:20]}..." if len(CSRF_TOKEN) > 20 else f"CSRF token: {CSRF_TOKEN}")

    # Test 1: Basic typename query
    test_graphql(
        "Test 1: Basic Typename",
        "{ __typename }"
    )

    # Test 2: Schema metadata
    test_graphql(
        "Test 2: Schema Metadata",
        """
        {
          __schema {
            queryType { name }
            mutationType { name }
          }
        }
        """
    )

    # Test 3: Contact search (your own portal data)
    test_graphql(
        "Test 3: Contact Search (Own Portal)",
        """
        query {
          crmObjectsSearch(
            type: "0-1"
            filterGroups: []
            count: 5
            offset: 0
          ) {
            total
            hasMore
            results {
              id
              properties(names: ["email", "firstname", "lastname"]) {
                name
                value
              }
              userPermissions {
                currentUserCanView
                currentUserCanEdit
              }
            }
          }
        }
        """
    )

    # Test 4: User permissions check
    test_graphql(
        "Test 4: Current User Permissions",
        """
        query {
          crmObjectsSearch(type: "0-1", count: 1) {
            results {
              userPermissions {
                currentUserCanView
                currentUserCanEdit
              }
            }
          }
        }
        """
    )

    print(f"\n{'='*70}")
    print("TESTING COMPLETE")
    print('='*70)
    print("\nNext steps:")
    print("1. Check which queries returned data")
    print("2. Note any permission restrictions (currentUserCanEdit=false)")
    print("3. Try IDOR testing by changing portalId in URL to {PORTAL_ID}+1")
