# HubSpot Service Map

**Purpose**: Living document tracking HubSpot's services, technologies, and attack surface discovered during recon.

**Status**: Active | Last Updated: 2025-10-15

---

## 📊 Service Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HubSpot Application                       │
├─────────────────────────────────────────────────────────────┤
│  Frontend Layer (React + Apollo GraphQL)                     │
│  ├─ unified-nav/loader.js (navigation bundle)               │
│  ├─ CRM Common DLB Bundle (static-1.3890)                   │
│  └─ UI Component Libraries                                   │
├─────────────────────────────────────────────────────────────┤
│  API Gateway Layer                                           │
│  ├─ GraphQL (/graphql)                                      │
│  ├─ REST APIs (hub-http, hubspotter-http)                   │
│  └─ Self-Service API                                         │
├─────────────────────────────────────────────────────────────┤
│  Microservices Layer                                         │
│  ├─ CRM Services                                             │
│  ├─ Payment Services                                         │
│  ├─ Analytics/Reporting                                      │
│  ├─ AI/Copilot Services                                      │
│  └─ Customer Data Services                                   │
├─────────────────────────────────────────────────────────────┤
│  Third-Party Integrations                                    │
│  ├─ Ably (Realtime)                                          │
│  ├─ Sentry (Error Tracking)                                  │
│  ├─ Wootric (Feedback)                                       │
│  └─ AWS CloudFront (CDN)                                     │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                  │
│  └─ Snowflake (Data Warehouse)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Internal Services

### Core API Clients
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| Hub HTTP | `hub-http` | Core HTTP client for internal APIs | High |
| Hubspotter HTTP | `hubspotter-http` | Internal employee/user service client | Medium |
| Self-Service API | `self-service-api` | Customer account management (upgrades, billing) | **Critical** |
| Customer Data Objects | `customer-data-objects` | Customer data layer | High |
| CRM Pipelines | `crm-pipelines-api-client-types` | CRM pipeline management | Medium |

**Predicted Endpoints**:
- `https://api.hubspot.com/self-service/v1/*`
- `https://api.hubspot.com/customer-data/*`
- `https://api.hubspot.com/crm-pipelines/*`

**Testing Notes**:
- [ ] Test IDOR on customer-data endpoints
- [ ] Check authorization on self-service account operations
- [ ] Enumerate CRM pipeline permissions

---

### GraphQL Stack
| Component | Module Name | Purpose | Recon Priority |
|-----------|-------------|---------|----------------|
| Apollo Link | `apollo-link-hub-http` | GraphQL HTTP transport layer | **Critical** |
| Apollo DLB | `apollo-dlb` | Data loading bridge | Medium |
| GraphQL Core | `graphql` | Query engine | **Critical** |
| Apollo Stack | `apollo-stack-hubspot` | HubSpot's Apollo implementation | High |

**Known Endpoints**:
- `https://app.hubspot.com/graphql` (to verify)
- `https://api.hubspot.com/graphql` (to verify)

**Testing Notes**:
- [ ] Check if introspection is enabled
- [ ] Test query depth limits
- [ ] Look for field suggestions on errors
- [ ] Test for GraphQL batching attacks
- [ ] Check authorization on mutations

**Recon Commands**:
```bash
# Test GraphQL introspection
curl -X POST https://app.hubspot.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'

# Use graphql-path-enum for discovery
echo "https://app.hubspot.com/graphql" | \
  nuclei -t graphql/graphql-introspection.yaml
```

---

### CRM Services
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| Message Bus | `crm-message-bus` | Event-driven messaging for CRM | Medium |
| Object Map | `crm-object-map` | CRM object relationship mapping | Medium |
| Customer Data UI | `customer-data-reference-ui-components` | Customer data UI layer | Low |

**Testing Notes**:
- [ ] Test message bus for event injection
- [ ] Check object mapping for IDOR
- [ ] Analyze client-side data filtering logic

---

### Payment & Monetization
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| Payments Core | `growth-payments-core` | Payment processing logic | **Critical** |
| Payment Links | `payment-link-components` | Payment link generation | High |
| Monetization Types | `growth-monetization-service-types` | Billing/subscription types | Medium |

**Predicted Endpoints**:
- `/api/growth/payments/*`
- `/api/billing/*`
- `/payment-links/*`

**Testing Notes**:
- [ ] Test for price manipulation
- [ ] Check IDOR on payment links
- [ ] Test for race conditions in payment processing
- [ ] Verify refund authorization
- [ ] Check for discount code bypass

---

### AI & Copilot Services
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| Copilot Preview | `ai-addon-copilot-preview` | AI assistant preview feature | High |
| AI Rendering | `ai-rendering-library` | AI content rendering | Medium |
| AI Settings | `ai-settings-ui-library` | AI configuration UI | Medium |
| Copilot Plugins | `copilot-plugins` | Plugin system for AI features | Medium |

**Testing Notes**:
- [ ] Test for prompt injection
- [ ] Check authorization on AI features
- [ ] Look for API key exposure in client code
- [ ] Test plugin loading mechanisms

---

### Reporting & Analytics
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| Reporting Data | `reporting-data` | Reporting data layer | Medium |
| Reporting UI | `reporting-ui-components` | Report visualization components | Low |
| Snowflake Integration | `reporting-snowflake` | Data warehouse connector | **Critical** |

**Testing Notes**:
- [ ] Check for data leakage in reports
- [ ] Test IDOR on saved reports
- [ ] Look for Snowflake connection strings in client code
- [ ] Test for SQL injection in report filters

---

### File & Asset Management
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| File Manager | `file-manager-components`, `FileManagerLib` | File upload/management | High |
| Asset Management | `ui-asset-management-lib` | Digital asset management | Medium |
| CDN | `static.hsappstatic.net` | Static asset delivery | Medium |

**Known Domains**:
- `static.hsappstatic.net` (CloudFront CDN)

**Testing Notes**:
- [ ] Test file upload for malicious files
- [ ] Check IDOR on file access
- [ ] Enumerate CDN for exposed files
- [ ] Test for path traversal in file manager
- [ ] Check for unrestricted file types

**Recon Commands**:
```bash
# Enumerate static assets by version
for v in {3800..3900}; do
  curl -I "https://static.hsappstatic.net/unified-nav/static-1.$v/loader.js"
done | grep "200 OK"
```

---

### Authentication & Session Management
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| Portal ID Parser | `PortalIdParser` | Portal/account ID validation | High |
| Universal Auth | `ui-universal-auth` | Authentication UI/logic | **Critical** |

**Testing Notes**:
- [ ] Test for session fixation
- [ ] Check portal ID enumeration
- [ ] Test for auth bypass via direct API calls
- [ ] Verify JWT validation if used
- [ ] Check for CSRF protection

---

## 🔌 Third-Party Integrations

### Realtime & Messaging
| Service | Purpose | Security Notes | Recon Priority |
|---------|---------|----------------|----------------|
| Ably | WebSocket/realtime messaging | Look for exposed API keys, test channel authorization | **Critical** |

**Testing Notes**:
- [ ] Intercept WebSocket handshakes for tokens
- [ ] Test channel subscription without auth
- [ ] Look for Ably API keys in JS bundles
- [ ] Test for message injection

**Recon Commands**:
```bash
# Search for Ably keys in JS
curl https://static.hsappstatic.net/unified-nav/static-1.3890/loader.js | \
  grep -Eo '[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}'
```

---

### Error Tracking
| Service | Purpose | Security Notes | Recon Priority |
|---------|---------|----------------|----------------|
| Sentry (Raven) | `raven`, `raven-hubspot` | Look for exposed DSNs, check error payloads for sensitive data | High |

**Testing Notes**:
- [ ] Extract Sentry DSN from client code
- [ ] Send test errors to check if accepted
- [ ] Look for PII in error payloads
- [ ] Test for error endpoint abuse

**Recon Commands**:
```bash
# Find Sentry DSN
curl https://static.hsappstatic.net/unified-nav/static-1.3890/loader.js | \
  grep -Eo 'https://[a-f0-9]+@[a-z0-9.]+/[0-9]+'
```

---

### Feedback & Analytics
| Service | Purpose | Security Notes | Recon Priority |
|---------|---------|----------------|----------------|
| Wootric NPS | `wootric-nps` | Feedback/survey integration | Low |

**Testing Notes**:
- [ ] Check if feedback can be injected
- [ ] Test for XSS in survey responses

---

### UX & Onboarding
| Service | Purpose | Security Notes | Recon Priority |
|---------|---------|----------------|----------------|
| Shepherd.js | `ui-shepherd-react` | Onboarding tours | Low |
| Emoji Picker | `ui-addon-emoji-picker` | Emoji selection UI | Low |
| Crosstab | `crosstab` | Cross-tab communication | Medium |

**Testing Notes**:
- [ ] Test crosstab for postMessage vulnerabilities

---

## 📡 Analytics & Telemetry

### Usage Tracking
| Service | Module Name | Purpose | Recon Priority |
|---------|-------------|---------|----------------|
| Metrics JS | `metrics-js` | Client-side metrics | Low |
| Usage Tracker Core | `usage-tracker-core` | Core tracking logic | Medium |
| Usage Tracker | `usage-tracker`, `usage-tracker-container` | Event tracking | Medium |
| Integrations Tracking | `integrations-tracking-lib` | Integration usage tracking | Low |

**Testing Notes**:
- [ ] Check what data is being tracked
- [ ] Look for PII in tracking payloads
- [ ] Test if tracking can be manipulated

---

## 🗺️ Infrastructure & CDN

### Content Delivery
| Domain | Purpose | Technology | Recon Priority |
|--------|---------|------------|----------------|
| `static.hsappstatic.net` | Static assets, JS bundles | AWS CloudFront | Medium |
| `app.hubspot.com` | Main application | Unknown (to verify) | **Critical** |
| `api.hubspot.com` | API gateway | Unknown (to verify) | **Critical** |

**Testing Notes**:
- [ ] Enumerate subdomains
- [ ] Check for AWS S3 bucket exposure
- [ ] Test CloudFront cache poisoning
- [ ] Look for exposed `.git` or backup files

**Recon Commands**:
```bash
# Subdomain enumeration
subfinder -d hubspot.com -silent | httpx -silent -status-code

# Check for common exposures
nuclei -u https://static.hsappstatic.net -t exposures/
```

---

## 🎯 Priority Testing Matrix

### Critical (Test First)
1. GraphQL introspection & authorization
2. Self-Service API (account/billing operations)
3. Payment services (price manipulation, IDOR)
4. Universal Auth (session management)
5. Ably integration (token/key exposure)

### High Priority
1. File Manager (upload vulnerabilities)
2. Snowflake integration (data exposure)
3. Portal ID enumeration
4. AI Copilot (prompt injection)
5. Sentry DSN exposure

### Medium Priority
1. CRM services (IDOR, authorization)
2. Analytics/reporting (data leakage)
3. Message bus (event injection)
4. CDN enumeration

### Low Priority
1. UI components (XSS in edge cases)
2. Feedback systems
3. Onboarding tools

---

## 📝 Recon Workflow Integration

### Phase 1: Discovery (Current)
- [x] Extract services from loader.js
- [ ] Enumerate subdomains
- [ ] Discover API endpoints via httpx
- [ ] Map technology stack

### Phase 2: Endpoint Validation
- [ ] Verify predicted endpoints exist
- [ ] Check authentication requirements
- [ ] Document response formats
- [ ] Identify rate limits

### Phase 3: Nuclei Scanning
- [ ] Run exposures templates
- [ ] Run GraphQL templates
- [ ] Run API-specific templates
- [ ] Run file upload templates

### Phase 4: Manual Testing
- [ ] Test high-priority vulns
- [ ] Chain findings
- [ ] Verify exploitability
- [ ] Document for bounty submission

---

## 🔗 Related Documentation
- [[loader.js Service Analysis copy]] - Source analysis
- [[TARGET-HubSpot-Frontend-Overview]] - Frontend architecture
- [[TARGET-HubSpot-Index]] - Main index
- [[hubspot-js-loader.txt]] - Raw data extraction

---

## 📊 Statistics

**Services Identified**: 40+
**Third-Party Integrations**: 5
**Critical Priority Targets**: 5
**High Priority Targets**: 5
**GraphQL Endpoints**: 2 (to verify)
**CDN Domains**: 1

---

## 🚨 Security Notes

- All testing must be within HubSpot bug bounty scope
- Do not test payment flows with real transactions
- Avoid DOS/load testing without permission
- Document all findings with reproducible steps
- Check for PII before sharing any screenshots

---

**Last Updated**: 2025-10-15
**Next Review**: After Phase 2 completion
**Maintainer**: Itza (Turtle)
