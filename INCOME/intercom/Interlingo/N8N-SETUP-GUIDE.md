# n8n Google Calendar → Supabase Setup Guide

**Date:** 2025-10-22
**Purpose:** Complete setup instructions for Interlingo calendar sync automation

---

## 📋 Prerequisites

Before importing the workflow, ensure you have:

- [x] n8n instance running (cloud or self-hosted)
- [x] Google Calendar API access
- [x] Supabase project with PostgreSQL database
- [ ] Interlingo database schema already set up

---

## 🚀 Step 1: Import Workflow into n8n

### Method A: Via n8n UI (Recommended)

1. Open your n8n instance
2. Click **Workflows** in the sidebar
3. Click the **"Import from File"** button (top right)
4. Select the file: `n8n-gcal-to-supabase-workflow.json`
5. The workflow will be imported with all nodes

### Method B: Via Copy-Paste

1. Open `n8n-gcal-to-supabase-workflow.json`
2. Copy the entire JSON content
3. In n8n: **Workflows** → **Import from Clipboard**
4. Paste the JSON
5. Click **Import**

---

## 🔐 Step 2: Configure Google Calendar Credentials

### Create Google Calendar OAuth Credentials

1. In n8n, find the **"Google Calendar - Get Events"** node
2. Click on the node
3. Under **Credentials**, click **"Create New"**
4. Select **"Google Calendar OAuth2 API"**
5. You'll need to create a Google Cloud Project:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project (or use existing)
   - Enable **Google Calendar API**
   - Create OAuth 2.0 credentials
   - Add authorized redirect URI: `https://your-n8n-instance.com/rest/oauth2-credential/callback`
6. Copy **Client ID** and **Client Secret** into n8n
7. Click **Connect my account** and authorize

### Select Your Calendar

1. In the **Google Calendar - Get Events** node
2. Under **Calendar ID**, select your calendar (usually "Primary")
3. Adjust the time range if needed:
   - `timeMin`: How far back to sync (default: 1 day ago)
   - `timeMax`: How far forward to sync (default: 3 months)

---

## 🗄️ Step 3: Configure Supabase PostgreSQL Credentials

### Get Supabase Connection Details

1. Go to your Supabase dashboard: https://supabase.com/dashboard
2. Select your project
3. Navigate to **Settings** → **Database**
4. Copy the following:
   - **Host**: `db.anqfdvyhexpxdpgbkgmd.supabase.co`
   - **Database**: `postgres`
   - **Port**: `5432`
   - **User**: `postgres`
   - **Password**: [your database password]
   - **SSL**: Require

### Add to n8n

1. Find any **Postgres** node in the workflow (e.g., "Lookup Language ID")
2. Under **Credentials**, click **"Create New"**
3. Select **"Postgres"**
4. Fill in the details from above
5. **IMPORTANT:** Enable **SSL** (set to `require`)
6. Test connection (click "Test" button)
7. Save

### Apply to All Postgres Nodes

The workflow has multiple Postgres nodes. You need to:
1. Select each Postgres node
2. Change credential from placeholder to your newly created credential
3. **List of nodes to update:**
   - Lookup Language ID
   - Lookup Organization
   - Create Organization
   - Lookup Location
   - Create Location
   - Create Commitment Block
   - Insert Client Requests

---

## 🔧 Step 4: Review and Customize Parsing Logic

### Summary Field Parsing

The workflow expects this format:
```
LANGUAGE - MODALITY
```

**Examples:**
- `Spanish - ZOOM` → Language: Spanish, Modality: Remote
- `ASL - IN PERSON` → Language: ASL, Modality: In-Person
- `Russian - PHONE` → Language: Russian, Modality: Phone

**If your format is different**, edit the **"Parse Calendar Events"** node:
- Line 22: Adjust the `split(' - ')` logic
- Lines 25-31: Update modality mapping

### Location Field Parsing

The workflow expects organization abbreviations:
```
FIFE
KENT
PUYALLUP
```

**If your format is different**, edit:
- **"Lookup Organization"** node SQL query
- Consider adding fuzzy matching

### Description Field Parsing

Expected format:
```
CLIENT NAME
CASENUM - PROGRAM
1	CHARGE
CASENUM - PROGRAM
2	CHARGE
```

**If your format is different**, edit the **"Parse Calendar Events"** node:
- Lines 38-77: Update the parsing logic

---

## 📊 Step 5: Populate Reference Data

### Required Tables

Before running the workflow, ensure these tables have data:

#### 1. Languages Table

```sql
-- Verify languages exist
SELECT * FROM languages WHERE name IN ('Spanish', 'ASL', 'Russian');

-- Add missing languages if needed
INSERT INTO languages (name) VALUES ('Spanish') ON CONFLICT DO NOTHING;
INSERT INTO languages (name) VALUES ('ASL') ON CONFLICT DO NOTHING;
INSERT INTO languages (name) VALUES ('Russian') ON CONFLICT DO NOTHING;
```

#### 2. Organizations Table (Optional - auto-created)

```sql
-- Verify common organizations
SELECT * FROM organizations WHERE abbreviation IN ('FIFE', 'KENT', 'PUYALLUP');

-- Optionally pre-populate
INSERT INTO organizations (name, abbreviation)
VALUES
  ('Fife Municipal Court', 'FIFE'),
  ('Kent Municipal Court', 'KENT'),
  ('Puyallup Municipal Court', 'PUYALLUP')
ON CONFLICT DO NOTHING;
```

#### 3. Court Programs (Optional)

```sql
-- Verify programs like PEI, ARR, etc.
SELECT * FROM court_programs WHERE name IN ('PEI', 'ARR', 'PRETRIAL');

-- Add if needed
INSERT INTO court_programs (name, description)
VALUES
  ('PEI', 'Pre-Examination Interview'),
  ('ARR', 'Arraignment'),
  ('PRETRIAL', 'Pretrial Hearing')
ON CONFLICT DO NOTHING;
```

---

## ▶️ Step 6: Test the Workflow

### Manual Test

1. **Click the "Execute Workflow" button** in n8n
2. The workflow will:
   - Fetch events from Google Calendar
   - Parse each event
   - Create records in Supabase
3. **Check the output** of each node:
   - Green = Success
   - Red = Error
4. **Review errors** if any occur

### Test with Sample Event

Create a test event in Google Calendar:

```
Title: Spanish - ZOOM
Location: KENT
Description:
SMITH, JOHN
TEST123 - ARR
1	DUI
TEST124 - ARR
2	RECKLESS DRIVING

Start: Tomorrow at 9:00 AM
End: Tomorrow at 11:00 AM
```

Run the workflow and verify:
- [ ] Commitment block created in `commitment_blocks`
- [ ] Two client requests created in `client_requests`
- [ ] Language, organization, and location lookups succeeded

---

## 🔄 Step 7: Set Up Automatic Trigger (Optional)

### Option A: Webhook Trigger (Real-time)

1. Replace **"Google Calendar - Get Events"** with **"Webhook"** trigger
2. Configure Google Calendar push notifications:
   - Set up Calendar API watch
   - Point to n8n webhook URL
   - Events trigger immediately

### Option B: Schedule Trigger (Polling)

1. Add **"Schedule Trigger"** node before "Google Calendar - Get Events"
2. Set interval (e.g., every 15 minutes)
3. Workflow runs automatically

**For now, manual execution is fine for testing.**

---

## 🐛 Troubleshooting

### Common Issues

#### **1. "Invalid API key" Error**
- **Solution:** Check Supabase credentials
- Ensure SSL is enabled
- Verify password is correct

#### **2. "Language not found" Error**
- **Solution:** Populate `languages` table
- Run SQL from Step 5

#### **3. "Organization not found" Error**
- **Solution:** The workflow auto-creates organizations
- If it fails, check SQL permissions
- Ensure INSERT permission on `organizations` table

#### **4. Parsing Errors**
- **Solution:** Check your calendar event format
- Compare with examples in Step 4
- Edit parsing logic in "Parse Calendar Events" node

#### **5. Duplicate Jobs Created**
- **Solution:** Add duplicate detection:
  - Check if event ID already exists
  - Add to workflow before insertion

---

## 📈 Next Steps

### After Successful Test:

1. **Enable automatic execution**
   - Set up Schedule Trigger (every 15 min)
   - Or set up Webhook for real-time sync

2. **Monitor the workflow**
   - Check n8n execution history
   - Review Supabase for new jobs
   - Test viewing jobs in Interlingo web app

3. **Enhancements:**
   - Add error notifications (Slack, email)
   - Add duplicate event prevention
   - Add interpreter assignment parsing
   - Add status sync back to Calendar

---

## 🎯 Verification Checklist

Before considering setup complete:

- [ ] Workflow imported successfully
- [ ] Google Calendar credentials configured and tested
- [ ] Supabase credentials configured on all Postgres nodes
- [ ] Reference data populated (languages, organizations)
- [ ] Manual test successful with sample event
- [ ] Commitment block created in database
- [ ] Client requests created and linked correctly
- [ ] Job visible in Interlingo web app dashboard

---

## 📞 Support

**Issues?** Check:
1. n8n execution logs for specific errors
2. Supabase logs for database errors
3. Your calendar event format matches expected structure

**Need help?** Reference:
- `/INCOME/intercom/GCal-to-Supabase-Mapping.md` for parsing rules
- `N8N-SETUP-GUIDE.md` (this file) for setup steps
- n8n community forums for platform-specific issues

---

**Happy Automating! 🚀**
