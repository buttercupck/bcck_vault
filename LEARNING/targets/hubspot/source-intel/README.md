# Source Code Intelligence

**Status:** Analysis Complete
**Bundles Analyzed:** 2 (apollo.bundle, head-dlb.bundle)
**Source Files Extracted:** 185 files
**Total Lines:** 23,696

## Purpose

Static analysis of HubSpot's production JavaScript to discover:
- Internal architecture and service structure
- API endpoints and RPC methods
- Error handling logic
- Multi-tenant isolation mechanisms
- Portal ID extraction patterns

## Structure

- `bundles/` - Original minified production bundles with source maps
- `extracted/` - Deobfuscated/indexed source code
- `analysis/` - Detailed analysis reports by bundle
- `architecture/` - System architecture documentation
- `raw-data/` - Miscellaneous data files (org IDs, loader scripts)

## Key Findings

### 1. CHIRP RPC Framework
- Complete error handling framework exposed
- Service/method enumeration possible
- Internal RPC structure documented

### 2. Portal ID Extraction
- Regex patterns for URL/query param extraction
- Multi-tenant isolation logic revealed
- Edge case test vectors identified

### 3. Error Reporting Infrastructure
- exceptions.hubspot.com endpoint discovered
- Hublet-specific routing exposed
- QA environment endpoints identified

### 4. Configuration Systems
- localStorage-based config discovered
- Hublet routing logic mapped
- Environment detection patterns found

## Files

- `FINDINGS.md` - Complete source analysis report
- `bundles/` - *.bundle.production.js + source maps
- `extracted/` - *-indexed.js, *-sources.js
- `analysis/apollo-bundle-analysis.md` - Apollo GraphQL client analysis
- `analysis/head-dlb-bundle-analysis.md` - Main DLB bundle findings
- `architecture/service-map.md` - Internal service architecture

## Analysis Workflow

1. **Download Bundles** - Capture from browser DevTools
2. **Extract Source Maps** - Unpack to readable JavaScript
3. **Index Code** - Create searchable indexed files
4. **Pattern Analysis** - Search for security-relevant code
5. **Document Findings** - Create analysis reports

## Attack Vectors from Source Analysis

✅ **CHIRP Enumeration** - Trigger errors to map services
✅ **Portal ID IDOR** - Test edge cases: -1, 0, null, 999999
✅ **Hublet Enumeration** - Test na1, na2, eu1, qa environments
✅ **Error Injection** - Test exceptions endpoint for XSS/SSRF

## Next Steps

- Correlate source findings with live testing
- Test all discovered endpoints
- Map complete service architecture
- Identify additional API surfaces from code
