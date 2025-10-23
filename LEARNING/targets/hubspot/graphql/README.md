# GraphQL Attack Surface

**Status:** ✅ COMPLETE - Schema introspection successful
**Endpoint:** `https://app-na2.hubspot.com/api/graphql/crm`
**Schema Size:** 772 types (533 objects, 82 inputs, 115 enums)

## Quick Start

### 1. Validate Cookies
```bash
# Check cookie freshness
ls -la headers.md

# If > 1 hour old, re-capture from browser DevTools
```

### 2. Run Schema Introspection
```bash
cd tools/
python3 graphql_schema_introspection.py
```

### 3. Test for IDOR
```bash
python3 test_graphql_final.py
```

## Files

- `COMPLETE-REPORT.md` - Full research findings with 772 types discovered
- `FINDINGS.md` - Vulnerability summary and exploitation notes
- `schema.json` - Complete GraphQL schema (use for analysis)
- `headers.md` - Captured request headers and cookies
- `tools/` - Testing scripts for schema introspection and IDOR testing

## Key Findings

✅ **Schema Introspection Enabled** - Full type system exposed
✅ **Portal ID in URL** - IDOR testing vector identified
✅ **CSRF Token Required** - `X-HubSpot-CSRF-hubspotapi` header mandatory
⚠️ **Mutations Available** - Test for unauthorized data modification

## Testing Workflow

1. **Cookie Validation** - Ensure session is active
2. **Schema Analysis** - Review types for sensitive data access
3. **IDOR Testing** - Modify portalId parameter
4. **Mutation Testing** - Test create/update/delete operations
5. **Authorization Bypass** - Test with low-privileged account

## Next Steps

- Test all mutations for authorization checks
- Map sensitive CRM data types
- Test cross-portal access
- Document findings in bug bounty report
