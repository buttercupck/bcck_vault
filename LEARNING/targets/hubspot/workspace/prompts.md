{ "type": "<API | GraphQL | CDN | Analytics | ErrorTracking | Auth | Realtime | Payments | Storage | Integration | Config>", "indicator": "<exact snippet or short string found (redact secrets)>", "host_or_service": "<hostname or vendor name, if identifiable>", "location": "<filename:line or approximate location in file>", "confidence": "<low|medium|high>", "notes": "<1-2 sentence explanation of what this implies and why it matters for recon>" }

Look for:

explicit full URLs (https://...), hostnames, and domain patterns GraphQL tagged templates or long query strings code initializing SDKs (Sentry/Raven, Segment, Stripe, Ably, etc.) references to /graphql, /api/, /v1/, new URL(...), fetch(, axios(, or Apollo usage CDN or storage references (static.hsappstatic.net, s3, cloudfront, hubspotusercontent) any telemetry/usage trackers or feature-flag/config objects that contain endpoints or region identifiers Rules:

If you find secrets (API keys, DSNs, tokens), do not print the full secret — replace the middle with ... and mark "confidence":"high" with "notes":"SECRET_REDACTED". Be concise. Return only JSON lines (one object per line). No extra commentary. Prioritize findings that are likely externally reachable (hostnames + endpoints) and label which ones to investigate further. Finally, after the JSON lines, output a single short JSON object: { "next_steps": ["<one-line recommended next step 1>", "<one-line recommended next step 2>", ...] }

