[CHAVVO: MENTOR MODE]

**Intent:**
You want a complete execution plan for validating GraphQL infrastructure (Option A) and extracting source maps for secret hunting (Option B), with clear divisions of what I'll automate versus what you need to do manually, prioritizing existing tools over custom builds.

**Explanation:**

I'll structure this as two parallel tracks you can run simultaneously. Track A targets live GraphQL endpoints and requires your authenticated session. Track B is fully automated source map extraction and analysis that I can run immediately without cookies.

**The Tools Stack:**

For GraphQL (Track A), we'll use httpx for endpoint discovery, nuclei with graphql templates for introspection testing, and GraphQL Voyager or Altair for schema visualization. ProjectDiscovery's suite handles everything except schema visualization, which requires a browser-based tool.

For source map extraction (Track B), I'll use curl + jq for downloading and parsing, then ripgrep for pattern matching across the extracted sources. This finds API keys, tokens, DSNs, and hardcoded endpoints without any custom tooling.

**Track A: GraphQL Infrastructure Validation**

**What I Handle (No Authentication Required):**
1. Endpoint discovery - I'll use httpx to test common GraphQL paths across hubspot.com subdomains
2. Generate nuclei command for you to run with cookies
3. Build GraphQL introspection queries for you to execute

**What You Do (Requires Cookies):**
1. Get authenticated session cookies from browser
2. Run nuclei GraphQL scans with your cookies
3. Execute introspection queries via curl or Altair
4. Import schema into GraphQL Voyager for visualization

**Step-by-Step for Track A:**

**Step 1 (Me):** Enumerate potential GraphQL endpoints
```bash
echo -e "app.hubspot.com\napi.hubspot.com\napp-na1.hubspot.com\napi-na1.hubspot.com" | \
  httpx -silent -path /graphql -path /api/graphql -path /graphql/batch -mc 200,401,403,405
```

**Step 2 (You):** Once I find responsive endpoints, export your cookies:
```bash
# In Chrome DevTools Console on app.hubspot.com:
document.cookie.split(';').map(c => c.trim()).join('; ')

# Save to file: cookies.txt in format:
# Cookie: [paste output here]
```

**Step 3 (Me):** Generate nuclei command with GraphQL templates:
```bash
nuclei -u https://app.hubspot.com/graphql \
  -H "Cookie: [YOUR_COOKIES]" \
  -t ~/nuclei-templates/http/graphql/ \
  -o graphql-nuclei-results.txt
```

**Step 4 (You):** Run the nuclei command I generate, then test introspection manually:
```bash
curl -X POST https://app.hubspot.com/graphql \
  -H "Content-Type: application/json" \
  -H "Cookie: [YOUR_COOKIES]" \
  -d '{"query":"{ __schema { queryType { name } mutationType { name } subscriptionType { name } } }"}' \
  | jq .
```

If introspection works, dump full schema:
```bash
curl -X POST https://app.hubspot.com/graphql \
  -H "Content-Type: application/json" \
  -H "Cookie: [YOUR_COOKIES]" \
  -d '{"query":"{ __schema { types { name kind fields { name type { name kind ofType { name kind } } args { name type { name kind } } } } } }"}' \
  > hubspot-graphql-schema.json
```

**Step 5 (You):** Visualize schema using GraphQL Voyager:
```bash
# Install voyager
npm install -g graphql-voyager

# Or use online version at:
# https://graphql-kit.com/graphql-voyager/
# Upload hubspot-graphql-schema.json
```

**Track B: Source Map Extraction & Secret Analysis**

**What I Handle (Fully Automated):**
1. Download all three source maps
2. Parse and extract all source files
3. Run comprehensive regex searches for secrets
4. Generate findings report with file locations

**Step-by-Step for Track B:**

**Step 1 (Me):** Download source maps:
```bash
curl -o apollo.bundle.map https://static.hsappstatic.net/[path]/apollo.bundle.production.js.map
curl -o head-dlb.bundle.map https://static.hsappstatic.net/[path]/head-dlb.bundle.production.js.map
curl -o loader.bundle.map https://static.hsappstatic.net/[path]/unified-nav/static-1.3890/loader.js.map
```

**Step 2 (Me):** Extract source files from maps:
```bash
# Extract sources from each map
jq -r '.sourcesContent[]' apollo.bundle.map > apollo-sources.js
jq -r '.sourcesContent[]' head-dlb.bundle.map > head-dlb-sources.js
jq -r '.sourcesContent[]' loader.bundle.map > loader-sources.js

# Create indexed files for grep
jq -r '.sources[] as $name | .sourcesContent[] | "\($name)\n\(.)"' apollo.bundle.map > apollo-indexed.txt
```

**Step 3 (Me):** Hunt for secrets with ripgrep patterns:
```bash
# API Keys (32-64 char alphanumeric)
rg -i "api[_-]?key[\"']?\s*[:=]\s*[\"'][a-zA-Z0-9_-]{32,}[\"']" *-sources.js

# Tokens
rg -i "token[\"']?\s*[:=]\s*[\"'][a-zA-Z0-9_-]{32,}[\"']" *-sources.js

# Sentry DSN
rg "https://[a-f0-9]+@[a-z0-9.]+sentry\.[a-z]+/[0-9]+" *-sources.js

# Ably Keys
rg "[a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}" *-sources.js

# AWS Keys
rg "AKIA[0-9A-Z]{16}" *-sources.js

# Private Keys
rg "-----BEGIN (RSA |)PRIVATE KEY-----" *-sources.js

# GraphQL Endpoints
rg -i "(https?://[^\"']+/graphql)" *-sources.js

# API Endpoints
rg "https://[a-z0-9-]+\.hubspot[a-z]*\.com/[a-z0-9/_-]+" *-sources.js
```

**Step 4 (Me):** Generate prioritized findings report:
```json
{
  "high_severity": [
    {"type": "API_KEY", "file": "apollo-dlb@3.41/config.js", "line": 42, "redacted": "abc...xyz"},
    {"type": "SENTRY_DSN", "file": "raven-hubspot@1.5344/client.js", "line": 12, "value": "https://..."}
  ],
  "medium_severity": [
    {"type": "GRAPHQL_ENDPOINT", "file": "apollo-link/http.js", "line": 88, "url": "https://app.hubspot.com/graphql"}
  ],
  "informational": [
    {"type": "CDN_PATH", "file": "loader.js", "pattern": "static.hsappstatic.net/static-1.{version}"}
  ]
}
```

**What You Do (Manual Review):**
1. Review my findings report
2. Verify any potential secrets aren't false positives
3. Test discovered endpoints with your cookies
4. Decide which findings warrant deeper investigation or bounty submission

**Changes Implemented:**
Creating execution plan and tool selection framework for dual-track reconnaissance operation.

**Next Steps:**

- **Option A: I'll Start Track B Immediately** — Give me the green light and I'll download the source maps and start extraction. This requires no input from you and runs in parallel while you get cookies ready.

- **Option B: You Provide Source Map URLs First** — If the URLs in your documents are outdated (static-1.3890 might be old), give me the current version numbers from your browser's Network tab so I download the right files.

- **Option C: We Start with Track A Endpoint Discovery** — I'll run httpx endpoint enumeration right now to see what responds on hubspot.com domains, then you can focus your cookie gathering on the live endpoints only.
