---
silo: LEARNING
category: N8N
type: Supabase-Integration
version: 1.0
---

# LRN-N8N-Supabase-Data-Retrieval

This document outlines the n8n workflow to retrieve comprehensive data from Supabase, including all associated relationships. Due to PostgREST limitations on deep nesting in a single `select` query, this workflow uses a multi-step approach.

## Problem Statement:
When trying to GET data with complex relationships, the Supabase node may ask for values and process errors due to nested relationship requirements.

## Solution: Multi-Step HTTP Request Approach

### Step 1: Fetch Primary Data (HTTP Request Node)

This first **HTTP Request node** will fetch all `commitment_blocks` and their directly linked `locations` and `client_requests` (including nested `languages` and `court_programs`).

#### Node Configuration:
- **Method:** `GET`
- **URL:** `YOUR_SUPABASE_URL/rest/v1/commitment_blocks`
  - Replace `YOUR_SUPABASE_URL` with your actual Supabase project URL (e.g., `https://anqfdvyhexpxdpgbkgmd.supabase.co`)

#### Authentication (Headers):
- Enable **"Send Headers"**
- Add Header 1: `Key: apikey`, `Value: YOUR_SUPABASE_ANON_KEY`
- Add Header 2: `Key: Authorization`, `Value: Bearer YOUR_SUPABASE_ANON_KEY`
  - Replace `YOUR_SUPABASE_ANON_KEY` with your actual Supabase `anon` key

#### Query Parameters:
- Enable **"Send Query Parameters"**
- Add Parameter: `Name: select`, `Value: *,locations(*),client_requests(*,languages(*),court_programs(*))`

#### Explanation of `select` Value:
- `*`: Selects all columns from the `commitment_blocks` table
- `locations(*)`: Embeds all columns from the directly linked `locations` table
- `client_requests(*,languages(*),court_programs(*))`: Embeds all columns from the `client_requests` table, and further nests all columns from `languages` and `court_programs` within each `client_request`
- `order=start_time.asc`: (Add as a separate query parameter) Orders the results by `start_time` in ascending order

### Step 2: Fetch Organization Details

After Step 1, your data will contain `locations` objects, but the `organizations` data (like `name`, `abbreviation`, `address`) is linked from the `locations` table via `org_id`. You'll need an additional step to fetch this.

#### Option A: HTTP Request Node with "Split In Batches"
1. **Iterate:** Connect a **Split In Batches** node after Step 1, set to iterate over `{{ $json.locations }}`
2. **HTTP Request Node:**
   - **Method:** `GET`
   - **URL:** `YOUR_SUPABASE_URL/rest/v1/organizations`
   - **Authentication:** Same headers as Step 1
   - **Query Parameters:**
     - `Name: id`, `Value: eq.{{ $json.org_id }}`
     - `Name: select`, `Value: *`
3. **Merge Node:** Use a **Merge node** to re-combine the fetched organization data

#### Option B: Code Node for Batching
For more advanced users, a Code node can fetch all unique `org_id`s and make a single API call for multiple organizations, then map them back.

### Step 3: Fetch Interpreter Details

Similarly, to get the full details for each `interpreter`, you'll need another step. The `interpreter_id` is found on the `commitment_blocks` table.

#### Configuration:
1. **Iterate:** Connect a **Split In Batches** node after Step 1, set to iterate over `{{ $json }}`
2. **HTTP Request Node:**
   - **Method:** `GET`
   - **URL:** `YOUR_SUPABASE_URL/rest/v1/interpreters`
   - **Query Parameters:**
     - `Name: id`, `Value: eq.{{ $json.interpreter_id }}`
     - `Name: select`, `Value: *,interpreter_languages(*,languages(*))`
3. **Merge Node:** Re-combine the fetched interpreter data

## Final Data Structure:
After these steps, your n8n workflow will have processed and merged all the data. Each `commitment_block` record will be enriched with its associated `locations`, `organizations`, `client_requests` (with `languages` and `court_programs`), and `interpreters` details, providing a comprehensive dataset for your app.

## Cross-References:
- [[LRN-Supabase-Complex-Queries]]
- [[LRN-N8N-HTTP-Request-Patterns]]
- [[INC-Interlingo-Data-Architecture]]

---
*Migrated from legacy structure: 2025-09-16*