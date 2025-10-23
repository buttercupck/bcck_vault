# Apollo Bundle Analysis - HubSpot GraphQL Infrastructure

**Source**: `apollo.bundle.production.js` + source map
**Date**: 2025-10-15
**Bundle Size**: 2 lines (minified)
**Source Files**: 157 files mapped

---

## 🎯 Executive Summary

HubSpot uses **Apollo Client 3.43** with custom HubSpot packages (`apollo-stack-hubspot` and `apollo-dlb`) for GraphQL communication. This bundle reveals the complete GraphQL infrastructure, transport layer, and caching strategy.

---

## 📦 Key Package Versions

| Package | Version | Purpose |
|---------|---------|---------|
| **apollo-stack-hubspot** | 3.43 | HubSpot's customized Apollo Client |
| **apollo-dlb** | 3.41 | HubSpot's Data Loading Bridge (DLB) |
| **@apollo/client** | 3.x | Official Apollo Client (customized) |
| **bender-build-tools** | static-1.1482 | HubSpot's build system |

---

## 🔍 Critical Findings

### 1. **Custom HubSpot Apollo Packages**

HubSpot maintains **forked/customized versions** of Apollo Client:

```
bpm:///apollo-stack-hubspot@3.43/@apollo/client/
bpm:///apollo-dlb@3.41/js/index.js
```

**Recon Value**: These custom packages may contain HubSpot-specific:
- Authentication logic
- Custom directives
- Error handling
- Query batching mechanisms
- Cache policies

---

### 2. **Build System Path Disclosure**

Found in source map:
```
webpack:///usr/share/hubspot/build/.bpm/packages/bender-build-tools/static-1.1482/
```

**Infrastructure Details**:
- Build server path: `/usr/share/hubspot/build/`
- Package manager: `bpm` (likely HubSpot's internal package manager)
- Build tool: `bender-build-tools`
- Static version: `1.1482`

**Attack Surface**: Could indicate:
- Internal package naming conventions
- Build infrastructure details
- Potential for server-side file disclosure

---

### 3. **Apollo Client Components Identified**

From the source map, the bundle includes:

#### Core Client Features
- `ApolloClient.js` - Main client initialization
- `ApolloLink.js` - Request/response middleware chain
- `Observable.js` - Reactive query execution
- `DocumentTransform.js` - Query transformation pipeline

#### GraphQL Utilities
- `directives.js` - Custom directive handling
- `fragments.js` - Fragment management
- `operations.js` - Query/mutation/subscription ops
- `storeUtils.js` - Cache key generation
- `pagination.js` - Pagination policies

#### Caching System
- `InMemoryCache.js` - Client-side cache
- `caches.js` - Cache implementations
- `strong.js` / `weak.js` - Strong/weak cache references
- `getMemoryInternals.js` - Cache internals

#### Network Layer
- `HttpLink.js` - HTTP transport
- `batch.js` - Request batching
- `retry.js` - Retry logic

---

## 🚨 Attack Vectors Discovered

### 1. **GraphQL Endpoint Confirmation**

The presence of `apollo-dlb` (Data Loading Bridge) confirms:
- HubSpot uses GraphQL for frontend data fetching
- Likely endpoint: `/graphql` or `/api/graphql`
- May support batched queries

**Testing Steps**:
```bash
# Test GraphQL introspection
curl -X POST https://app.hubspot.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'

# Test batch endpoint
curl -X POST https://app.hubspot.com/graphql/batch \
  -H "Content-Type: application/json" \
  -d '[{"query":"query { __typename }"}]'
```

---

### 2. **Custom Directive Exploitation**

`directives.js` indicates custom GraphQL directives. Common HubSpot patterns might include:

```graphql
# Potential custom directives
@hubspot
@portal
@permission
@cache
@export
@client
```

**Testing**: Use introspection to discover directives:
```graphql
{
  __schema {
    directives {
      name
      locations
      args {
        name
        type {
          name
        }
      }
    }
  }
}
```

---

### 3. **Cache Poisoning Potential**

Files like `storeUtils.js` and `caches.js` suggest custom cache key generation. Vulnerabilities:

- **Cache Key Collision**: Predict cache keys to poison other users' caches
- **Cache Extraction**: Read cached data via timing attacks
- **Optimistic Update Abuse**: Manipulate client state

**Testing**:
1. Capture cache keys from DevTools
2. Test if cache keys are predictable (e.g., based on portal ID)
3. Try to poison cache with malicious data

---

### 4. **Query Batching Attacks**

`batch.js` presence suggests GraphQL query batching. Potential attacks:

- **Batch Bomb**: Send massive batch causing resource exhaustion
- **Authorization Bypass**: Mix authorized/unauthorized queries in batch
- **Timing Attacks**: Measure batch response times for data inference

**Test Payload**:
```json
[
  {"query": "{ me { id } }"},
  {"query": "{ adminUsers { id } }"},
  {"query": "{ allPortals { id } }"}
]
```

---

### 5. **Fragment Injection**

`fragments.js` suggests fragment support. Test for:

```graphql
fragment MaliciousFragment on User {
  id
  email
  internalData {
    ssn
    salary
  }
}

query GetUser {
  user(id: "123") {
    ...MaliciousFragment
  }
}
```

---

## 📊 Technical Architecture

### Apollo Client Flow

```
User Request
    ↓
ApolloClient.js (initialization)
    ↓
ApolloLink.js (middleware chain)
    ↓
HttpLink.js (network transport)
    ↓
apollo-dlb (HubSpot Data Loading Bridge)
    ↓
/graphql endpoint
    ↓
InMemoryCache.js (response caching)
    ↓
Observable.js (reactive updates)
    ↓
UI Component
```

---

### HubSpot-Specific Layers

```
┌─────────────────────────────────────┐
│  apollo-dlb@3.41                    │  ← HubSpot's Data Loading Bridge
│  (Custom request/response handling) │
├─────────────────────────────────────┤
│  apollo-stack-hubspot@3.43          │  ← Customized Apollo Client
│  (HubSpot-specific features)        │
├─────────────────────────────────────┤
│  @apollo/client@3.x                 │  ← Base Apollo Client
│  (Standard GraphQL client)          │
└─────────────────────────────────────┘
```

---

## 🔗 Internal Package Manager (BPM)

HubSpot uses `bpm` (Bower Package Manager or custom tool) for internal packages:

**Package URL Format**:
```
bpm:///[package-name]@[version]/[path/to/file.js]
```

**Examples**:
- `bpm:///apollo-dlb@3.41/js/index.js`
- `bpm:///apollo-stack-hubspot@3.43/@apollo/client/index.js`

**Recon Value**:
- Internal package names may leak
- Version numbers indicate update frequency
- Could enumerate other internal packages

---

## 🎯 Priority Testing Checklist

### High Priority
- [ ] Test GraphQL introspection on `/graphql`
- [ ] Enumerate custom directives
- [ ] Test query batching limits
- [ ] Check authorization on batched queries
- [ ] Test cache key predictability

### Medium Priority
- [ ] Fragment injection tests
- [ ] Query depth/complexity limits
- [ ] Subscription endpoint discovery
- [ ] Error message information disclosure
- [ ] Cache timing attacks

### Low Priority
- [ ] Apollo DevTools exploitation
- [ ] Source map exposure in production
- [ ] Build path disclosure impact

---

## 🛠️ Recommended Tools

### GraphQL Testing
```bash
# GraphQL Voyager - visualize schema
npx graphql-voyager

# InQL Scanner - Burp extension
# GraphQL Cop - security scanner
```

### Chrome DevTools
```javascript
// Dump Apollo Client state
window.__APOLLO_CLIENT__
window.__APOLLO_CLIENT__.cache.extract()

// Watch queries
window.__APOLLO_CLIENT__.queryManager.queries

// Inspect link chain
window.__APOLLO_CLIENT__.link
```

---

## 📝 Key Files to Investigate Further

### In Source Map
1. `apollo-dlb@3.41/js/index.js` - HubSpot's data loading bridge
2. `apollo-stack-hubspot@3.43/@apollo/client/link/core/ApolloLink.js` - Link middleware
3. `apollo-stack-hubspot@3.43/@apollo/client/core/QueryManager.js` - Query execution
4. `apollo-stack-hubspot@3.43/@apollo/client/utilities/graphql/directives.js` - Custom directives

### To Request from DevTools
1. Full unminified bundle (if available via source map)
2. GraphQL schema file (often cached)
3. Apollo Client cache snapshot
4. Network requests showing GraphQL queries

---

## 🔐 Security Implications

### Information Disclosure
- **Build paths** reveal server infrastructure
- **Package versions** show update cadence
- **Custom packages** indicate internal tools

### Potential Vulnerabilities
1. **GraphQL introspection** - Schema enumeration
2. **Query batching** - Authorization bypass
3. **Cache manipulation** - Data poisoning
4. **Fragment injection** - Data exfiltration
5. **Custom directives** - Logic bypass

---

## 📊 Comparison with loader.js Analysis

| Feature | loader.js Findings | apollo.bundle Findings |
|---------|-------------------|------------------------|
| GraphQL Confirmed | `apollo-link-hub-http`, `graphql` | Full Apollo Client 3.43 implementation |
| Custom Packages | Mentioned `apollo-stack-hubspot` | **Confirmed custom fork at v3.43** |
| Data Loading | `apollo-dlb` mentioned | **apollo-dlb@3.41 fully integrated** |
| Caching | Mentioned InMemoryCache | **Detailed cache implementation exposed** |
| Network | Mentioned apollo-link | **HttpLink, batching, retry logic confirmed** |

**New Discoveries**:
- Build server path: `/usr/share/hubspot/build/`
- Internal package manager: `bpm`
- Apollo Client version: **3.43**
- Total source files: **157**

---

## 🎯 Next Steps

### Immediate Actions
1. **Test GraphQL endpoint** at `/graphql`
2. **Capture live queries** in Chrome DevTools Network tab
3. **Dump Apollo Client** from `window.__APOLLO_CLIENT__`
4. **Extract schema** via introspection or DevTools

### Deep Dive
1. **Deobfuscate bundle** using source map
2. **Analyze apollo-dlb** for custom logic
3. **Map all GraphQL queries** used in app
4. **Test each query** for IDOR/auth bypass

---

## 📁 Related Files

- [[HubSpot-Service-Map]] - Main service inventory
- [[loader.js Service Analysis copy]] - Navigation bundle analysis
- [[TARGET-HubSpot-Frontend-Overview]] - Frontend architecture

---

**Analysis Date**: 2025-10-15
**Analyst**: Itza (Turtle)
**Status**: Active Recon Phase
