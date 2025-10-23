# Low-Privileged Testing

**Purpose:** Horizontal privilege escalation testing with restricted accounts
**Focus:** Same-portal IDOR, unauthorized data access, permission bypass

## Overview

Low-privileged testing validates authorization controls by attempting to access higher-privileged resources using a restricted user account. This identifies horizontal privilege escalation vulnerabilities.

## Testing Methodology

1. **Create Test Account** - Low-privilege user in test portal
2. **Capture Credentials** - Session cookies, portal ID, user ID
3. **Replicate Tests** - Run Track A & B tests with low-priv creds
4. **Compare Access** - Identify unauthorized data accessible

## Quick Start

### 1. Set Up Low-Priv Account
- Create user with minimal permissions
- No admin access
- Limited CRM data visibility

### 2. Capture Session Data
```bash
# Document in portal-credentials.md:
- Portal ID
- User ID
- Hublet
- Session cookies
- CSRF token
```

### 3. Run Template Tests
```bash
# GraphQL IDOR test
cd ../graphql/tools/
python3 TEMPLATE_lowpriv_graphql.py

# Presence API IDOR test
cd ../rest-api/presence/tools/
python3 TEMPLATE_lowpriv_presence_idor.py

# CHIRP RPC test
cd ../rest-api/chirp/tools/
python3 TEMPLATE_lowpriv_chirp.py
```

## Files

- `README.md` - This file
- `quick-start.md` - Step-by-step testing instructions
- `portal-credentials.md` - Low-priv account details (gitignored)

## Expected vs Actual Behavior

### ✅ Expected (Secure)
- Access denied to other users' data
- Mutations rejected for unauthorized resources
- Cross-portal requests blocked
- Proper 403 Forbidden responses

### ⚠️ Vulnerabilities (If Found)
- 200 OK when accessing unauthorized resources
- Data returned for other portal IDs
- Mutations succeed on restricted objects
- Permission bypass through parameter manipulation

## Test Scenarios

1. **User IDOR** - Access other user IDs in same portal
2. **Portal IDOR** - Access different portal IDs
3. **Object IDOR** - Access restricted CRM objects
4. **Mutation Testing** - Attempt unauthorized data modification
5. **Query Bypass** - Access filtered data through alternate queries

## HubSpot Scope Alignment

Per HubSpot bug bounty scope:
- ✅ Cross-portal IDORs - **High Priority, Rewardable**
- ⚠️ Same-portal IDORs - **Case-by-case, depends on data sensitivity**
- ✅ PHI/PII access - **High Priority, Rewardable**
- ✅ Privilege escalation to Super Admin - **High Priority, Rewardable**

## Next Steps

- Execute all TEMPLATE scripts with low-priv creds
- Document access levels (what CAN vs CANNOT access)
- Test boundary conditions
- Prepare bug bounty reports for confirmed IDORs
