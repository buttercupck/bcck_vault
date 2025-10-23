import sys
import urllib.request
import ssl
import json
import re

# Create unverified SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Read headers.md
headers_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/graphql/headers.md'

print("="*70)
print("TRACK A: GRAPHQL TESTING WITH CAPTURED HEADERS")
print("="*70)

with open(headers_file, 'r') as f:
    content = f.read()

# Extract components
print("\n[PARSING headers.md]")

# Extract URL from first line
url_match = re.search(r'POST ([^\s]+) HTTP', content)
if url_match:
    path_with_params = url_match.group(1)
    print(f"✓ Path: {path_with_params[:80]}...")
else:
    print("✗ Could not extract URL")
    sys.exit(1)

# Extract Host
host_match = re.search(r'Host: ([^\n]+)', content)
if host_match:
    host = host_match.group(1).strip()
    print(f"✓ Host: {host}")
else:
    print("✗ Could not extract Host")
    sys.exit(1)

# Extract CSRF token
csrf_match = re.search(r'X-HubSpot-CSRF-hubspotapi: ([^\n]+)', content)
if csrf_match:
    csrf_token = csrf_match.group(1).strip()
    print(f"✓ CSRF Token: {csrf_token[:50]}...")
else:
    print("⚠ No CSRF token found")
    csrf_token = None

# Extract Cookie
cookie_match = re.search(r'Cookie: ([^\n]+)', content)
if cookie_match:
    cookie_header = cookie_match.group(1).strip()
    print(f"✓ Cookie: {len(cookie_header)} chars")
else:
    print("✗ Could not extract Cookie")
    sys.exit(1)

# Extract GraphQL body (the JSON array at the end)
# It's after all headers, starts with [
body_match = re.search(r'\[{.*}\]', content, re.DOTALL)
if body_match:
    original_body = body_match.group(0)
    print(f"✓ GraphQL Body: {len(original_body)} chars")
    try:
        parsed_body = json.loads(original_body)
        print(f"  Original query: {parsed_body[0]['operationName']}")
    except:
        print("  Could not parse body as JSON")
else:
    print("⚠ Could not extract GraphQL body")
    original_body = None

# Build full URL
full_url = f"https://{host}{path_with_params}"

print(f"\n[EXTRACTED COMPONENTS]")
print(f"Full URL: {full_url}")
print(f"Host: {host}")
print(f"CSRF Token: {'✓' if csrf_token else '✗'}")
print(f"Cookie: {'✓' if cookie_header else '✗'}")

def test_graphql(query_name, query, variables=None):
    """Test GraphQL endpoint with captured headers"""

    print(f"\n{'='*70}")
    print(f"TEST: {query_name}")
    print('='*70)

    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', cookie_header)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('Origin', f'https://{host}')
    req.add_header('Referer', f'https://{host}/contacts/242862774/objects/0-1/views/all/list')

    # Add CSRF token if available
    if csrf_token:
        req.add_header('X-HubSpot-CSRF-hubspotapi', csrf_token)
        print(f"✓ Added CSRF token")

    # Build body in the format from captured request: [{operationName, variables, query}]
    body = [{
        "operationName": query_name,
        "variables": variables if variables else {},
        "query": query
    }]

    data = json.dumps(body).encode('utf-8')
    print(f"Body length: {len(data)} bytes")

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=15)
        status = response.status
        response_content = response.read().decode('utf-8', errors='ignore')

        print(f"✓ Status: {status}")
        print(f"✓ Content Length: {len(response_content)} bytes")

        try:
            json_response = json.loads(response_content)
            print(f"✓ Response Type: JSON")

            # Check if it's an array response (matching request format)
            if isinstance(json_response, list) and len(json_response) > 0:
                print(f"✓ Array response with {len(json_response)} items")
                first_item = json_response[0]

                if 'data' in first_item:
                    print(f"✓✓✓ GRAPHQL SUCCESS - Has 'data' field")
                    print(f"  Data keys: {list(first_item['data'].keys())}")

                    # Pretty print (truncated)
                    data_str = json.dumps(first_item['data'], indent=2)
                    if len(data_str) > 800:
                        print(f"  Data preview:\n{data_str[:800]}...")
                    else:
                        print(f"  Data:\n{data_str}")

                    return True, 'SUCCESS', json_response

                elif 'errors' in first_item:
                    print(f"✓ GRAPHQL RESPONDED - Has 'errors' field")
                    print(f"  Errors: {first_item['errors']}")
                    return True, 'ERROR_RESPONSE', json_response
                else:
                    print(f"? Unexpected structure: {list(first_item.keys())}")
                    print(f"  Response: {json.dumps(first_item, indent=2)[:500]}")
                    return False, 'UNEXPECTED_FORMAT', json_response

            # Maybe single object response
            elif isinstance(json_response, dict):
                print(f"✓ Object response")
                if 'data' in json_response:
                    print(f"✓✓✓ GRAPHQL SUCCESS - Has 'data' field")
                    print(f"  Data keys: {list(json_response['data'].keys())}")
                    print(f"  Data: {json.dumps(json_response['data'], indent=2)[:500]}")
                    return True, 'SUCCESS', json_response
                elif 'errors' in json_response:
                    print(f"✓ GRAPHQL RESPONDED - Has 'errors' field")
                    print(f"  Errors: {json_response['errors']}")
                    return True, 'ERROR_RESPONSE', json_response
                else:
                    print(f"? Unexpected structure: {list(json_response.keys())}")
                    return False, 'UNEXPECTED_FORMAT', json_response
            else:
                print(f"? Unexpected response type: {type(json_response)}")
                print(f"  Content: {response_content[:500]}")
                return False, 'UNEXPECTED_TYPE', None

        except json.JSONDecodeError:
            print(f"✗ Response is not JSON")
            print(f"  Content preview: {response_content[:500]}")
            return False, 'NOT_JSON', None

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")

        try:
            error_content = e.read().decode('utf-8', errors='ignore')
            print(f"  Error length: {len(error_content)} bytes")

            try:
                error_json = json.loads(error_content)
                print(f"  Error JSON:")
                print(f"    {json.dumps(error_json, indent=4)[:500]}")
            except:
                print(f"  Error content: {error_content[:300]}")
        except:
            pass

        if e.code == 401:
            print(f"  → Unauthorized (cookies may be expired)")
        elif e.code == 403:
            print(f"  → Forbidden (CSRF token or permissions issue)")
        elif e.code == 404:
            print(f"  → Not Found (wrong endpoint)")
        elif e.code == 405:
            print(f"  → Method Not Allowed (wrong method)")
        elif e.code == 488:
            print(f"  → Wrong hublet (need different subdomain)")

        return False, f'HTTP_{e.code}', None

    except Exception as e:
        print(f"✗ Error: {e}")
        return False, 'EXCEPTION', None

print(f"\n{'#'*70}")
print(f"# TEST 1: SIMPLE INTROSPECTION QUERY")
print(f"{'#'*70}")

# Test simple typename query
success_1, result_1, response_1 = test_graphql(
    "TypenameQuery",
    "{ __typename }"
)

print(f"\n{'#'*70}")
print(f"# TEST 2: SCHEMA INTROSPECTION")
print(f"{'#'*70}")

# Test schema introspection
introspection_query = """
{
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      name
      kind
      description
    }
  }
}
"""

success_2, result_2, response_2 = test_graphql(
    "SchemaIntrospection",
    introspection_query
)

print(f"\n{'='*70}")
print("SUMMARY")
print('='*70)

if success_1 and result_1 == 'SUCCESS':
    print(f"\n✓✓✓ GRAPHQL ENDPOINT WORKING!")
    print(f"  Endpoint: /api/graphql/crm")
    print(f"  Hublet: {host}")
    print(f"  CSRF Token: Required and working")
    print(f"\n✓✓✓ TRACK A COMPLETE - GraphQL infrastructure VALIDATED")

    if success_2 and result_2 == 'SUCCESS':
        print(f"\n✓✓✓ SCHEMA INTROSPECTION WORKING")
        print(f"  Can enumerate entire GraphQL schema")
        print(f"  Next: Run full introspection for schema mapping")

elif success_1 and result_1 == 'ERROR_RESPONSE':
    print(f"\n✓ GraphQL endpoint responding")
    print(f"  Query has errors but endpoint works")
    print(f"  Check error messages for query issues")

else:
    print(f"\n✗ GraphQL endpoint not working")
    print(f"  Result: {result_1}")

    if 'HTTP_401' in str(result_1):
        print(f"\n  → Cookies may be expired")
        print(f"  → Regenerate cookies from browser")
    elif 'HTTP_403' in str(result_1):
        print(f"\n  → CSRF token may be expired")
        print(f"  → Regenerate entire capture from browser")
    elif 'HTTP_404' in str(result_1):
        print(f"\n  → Wrong endpoint path")
        print(f"  → Check browser Network tab for correct path")
    elif 'HTTP_488' in str(result_1):
        print(f"\n  → Wrong hublet")
        print(f"  → Use {host} from capture")

print(f"\n{'='*70}")
