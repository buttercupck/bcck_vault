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
print("TRACK A: GRAPHQL SCHEMA INTROSPECTION")
print("="*70)

with open(headers_file, 'r') as f:
    content = f.read()

# Extract components
url_match = re.search(r'POST ([^\s]+) HTTP', content)
path_with_params = url_match.group(1)

host_match = re.search(r'Host: ([^\n]+)', content)
host = host_match.group(1).strip()

csrf_match = re.search(r'X-HubSpot-CSRF-hubspotapi: ([^\n]+)', content)
csrf_token = csrf_match.group(1).strip() if csrf_match else None

cookie_match = re.search(r'Cookie: ([^\n]+)', content)
cookie_header = cookie_match.group(1).strip()

full_url = f"https://{host}{path_with_params}"

print(f"\n[CONFIGURATION]")
print(f"Endpoint: https://{host}/api/graphql/crm")
print(f"Portal ID: 242862774")
print(f"Hublet: app-na2")

def run_graphql_query(query_name, query):
    """Run GraphQL query"""

    print(f"\n{'='*70}")
    print(f"QUERY: {query_name}")
    print('='*70)

    req = urllib.request.Request(full_url, method='POST')
    req.add_header('Cookie', cookie_header)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0')
    req.add_header('Accept', 'application/json')
    req.add_header('Origin', f'https://{host}')

    if csrf_token:
        req.add_header('X-HubSpot-CSRF-hubspotapi', csrf_token)

    body = {"query": query}
    data = json.dumps(body).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, data=data, context=ctx, timeout=30)
        status = response.status
        response_content = response.read().decode('utf-8', errors='ignore')

        print(f"✓ Status: {status}")

        try:
            json_response = json.loads(response_content)

            if 'data' in json_response:
                print(f"✓ GraphQL Success")
                return True, json_response['data']
            elif 'errors' in json_response:
                print(f"✗ GraphQL Errors:")
                for error in json_response['errors']:
                    print(f"    - {error.get('message', error)}")
                return False, json_response['errors']
            else:
                print(f"? Unexpected response")
                return False, json_response

        except json.JSONDecodeError:
            print(f"✗ Not JSON: {response_content[:200]}")
            return False, None

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {e.reason}")
        try:
            error_content = e.read().decode('utf-8', errors='ignore')
            error_json = json.loads(error_content)
            print(f"  {json.dumps(error_json, indent=2)}")
        except:
            pass
        return False, None

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False, None

# Test 1: Basic typename
print(f"\n{'#'*70}")
print(f"# TEST 1: BASIC QUERY")
print(f"{'#'*70}")

success_1, data_1 = run_graphql_query(
    "Basic Typename",
    "{ __typename }"
)

if success_1:
    print(f"  Result: {data_1}")

# Test 2: Schema metadata
print(f"\n{'#'*70}")
print(f"# TEST 2: SCHEMA METADATA")
print(f"{'#'*70}")

success_2, data_2 = run_graphql_query(
    "Schema Metadata",
    """
    {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
      }
    }
    """
)

if success_2:
    print(f"\n  Query Type: {data_2['__schema']['queryType']}")
    print(f"  Mutation Type: {data_2['__schema']['mutationType']}")
    print(f"  Subscription Type: {data_2['__schema']['subscriptionType']}")

# Test 3: Full schema introspection
print(f"\n{'#'*70}")
print(f"# TEST 3: FULL SCHEMA INTROSPECTION")
print(f"{'#'*70}")

introspection_query = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
"""

success_3, data_3 = run_graphql_query(
    "Full Schema Introspection",
    introspection_query
)

if success_3:
    schema = data_3['__schema']
    types = schema['types']
    directives = schema['directives']

    print(f"\n  ✓ Schema retrieved successfully")
    print(f"  Total types: {len(types)}")
    print(f"  Total directives: {len(directives)}")

    # Analyze types
    query_types = [t for t in types if t['kind'] == 'OBJECT' and not t['name'].startswith('__')]
    mutation_types = [t for t in types if t['kind'] == 'OBJECT' and t.get('fields') and any(f.get('type', {}).get('name') == 'Mutation' for f in t.get('fields', []))]
    input_types = [t for t in types if t['kind'] == 'INPUT_OBJECT']
    enum_types = [t for t in types if t['kind'] == 'ENUM']

    print(f"\n  Type breakdown:")
    print(f"    - Object types: {len(query_types)}")
    print(f"    - Input types: {len(input_types)}")
    print(f"    - Enum types: {len(enum_types)}")

    # Show interesting types
    print(f"\n  Interesting Object Types:")
    for t in query_types[:20]:
        name = t['name']
        fields_count = len(t.get('fields', []))
        print(f"    - {name} ({fields_count} fields)")

    # Save full schema to file
    output_file = '/Users/itza/Documents/vault_self/bcck_vault/LEARNING/targets/hubspot/graphql/schema.json'
    with open(output_file, 'w') as f:
        json.dump(data_3, f, indent=2)
    print(f"\n  ✓ Full schema saved to: schema.json")

print(f"\n{'='*70}")
print("TRACK A SUMMARY")
print('='*70)

if success_1 and success_2 and success_3:
    print(f"\n✓✓✓ TRACK A COMPLETE - ALL TESTS PASSED")
    print(f"\nDiscoveries:")
    print(f"  ✓ GraphQL endpoint: /api/graphql/crm")
    print(f"  ✓ Correct hublet: app-na2.hubspot.com")
    print(f"  ✓ CSRF token: Required")
    print(f"  ✓ Body format: Standard {{\"query\": \"...\"}}")
    print(f"  ✓ Schema introspection: ENABLED")
    print(f"  ✓ Total types discovered: {len(types) if success_3 else 'N/A'}")

    print(f"\nNext Steps:")
    print(f"  1. Analyze schema for sensitive queries")
    print(f"  2. Test mutations for IDOR/privilege escalation")
    print(f"  3. Map CRM data access patterns")
    print(f"  4. Test authorization on sensitive fields")

elif success_1:
    print(f"\n✓ GraphQL endpoint working (basic queries)")
    print(f"✗ Schema introspection may be disabled or restricted")

else:
    print(f"\n✗ GraphQL endpoint not working")

print(f"\n{'='*70}")
