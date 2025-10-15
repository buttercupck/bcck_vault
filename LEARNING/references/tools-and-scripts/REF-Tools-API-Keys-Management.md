---
silo: LEARNING
category: Tools-Scripts
type: API-Keys-Template
version: 1.0
warning: "Contains sensitive information - secure appropriately"
---

# REF-Tools-API-Keys-Management

⚠️ **WARNING: This file contains API keys and sensitive credentials. Ensure proper security measures.**

## API Keys Template:

### OpenAI Configuration:
```
OPENAI_API_KEY=[your-openai-api-key-here]
```

### Google Services:
```
GOOGLE_API_KEY=[your-google-api-key-here]
```

### Supabase Configuration:
```
SUPABASE_CONNECTION_STRING="postgresql://postgres.[project-id]:[password]@[host]:5432/postgres"
SUPABASE_SERVICE_KEY=[your-supabase-service-key-here]
```

## Required Dependencies:
```bash
pip install langchain langchain-openai langchain-google-genai psycopg2-binary python-dotenv chromadb sentence-transformers
```

## Security Best Practices:
- Store API keys in environment variables
- Use .env files that are gitignored
- Rotate keys regularly
- Use service-specific keys with minimal permissions
- Monitor API usage for anomalies

## Cross-References:
- [[LRN-APIs-Authentication-Patterns]]
- [[METH-Security-Testing-API-Keys]]
- [[REF-Tools-Environment-Setup]]

---
*Migrated from legacy structure: 2025-09-16*
*NOTE: Original contained actual API keys - template created for security*