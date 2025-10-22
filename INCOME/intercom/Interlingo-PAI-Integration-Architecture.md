# Interlingo + PAI Integration Architecture

**Version:** 1.0.0
**Date:** 2025-10-22
**Author:** Itza (with Chavvo)
**Status:** Design Phase

---

## Executive Summary

This document outlines the technical architecture for integrating **Interlingo** (interpreter scheduling web application) with **PAI** (Personal AI Infrastructure) to create an intelligent, voice-enabled, AI-powered scheduling assistant that reduces manual work by 80%+ while improving accuracy and response times.

### Key Objectives
1. **Speed:** Reduce job creation from 10+ minutes to <2 minutes
2. **Intelligence:** AI-powered interpreter matching with 95%+ accuracy
3. **Accessibility:** Voice-first interface for mobile/hands-free operation
4. **Automation:** 70%+ of routine tasks automated with human oversight
5. **Scalability:** Handle 3-5x current volume without additional staff

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Components](#architecture-components)
3. [Data Flow](#data-flow)
4. [API Design](#api-design)
5. [Database Architecture](#database-architecture)
6. [Integration Points](#integration-points)
7. [Voice Interface](#voice-interface)
8. [AI/ML Components](#aiml-components)
9. [Security & Privacy](#security--privacy)
10. [Deployment Architecture](#deployment-architecture)
11. [Implementation Phases](#implementation-phases)
12. [Technical Stack](#technical-stack)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  Web App (Desktop)  │  Mobile PWA  │  Voice Interface  │  Email Client  │
└──────────┬──────────┴──────┬───────┴────────┬──────────┴────────┬───────┘
           │                 │                │                   │
           └─────────────────┴────────────────┴───────────────────┘
                                      │
                              ┌───────▼────────┐
                              │   API GATEWAY   │
                              │  (Rate Limit,   │
                              │   Auth, Route)  │
                              └───────┬────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
    ┌──────▼─────┐          ┌────────▼────────┐       ┌────────▼────────┐
    │ INTERLINGO │          │   PAI SERVICE   │       │  VOICE SERVICE  │
    │  WEB APP   │◄────────►│   (AI Brain)    │◄─────►│  (ElevenLabs)   │
    │            │          │                 │       │                 │
    │ Next.js    │          │ Express/Bun API │       │ HTTP Server     │
    │ React      │          │ Agent Orchestr. │       │ TTS/STT         │
    └──────┬─────┘          └────────┬────────┘       └─────────────────┘
           │                         │
           │                         │
    ┌──────▼─────────────────────────▼────────┐
    │         SUPABASE (PostgreSQL)            │
    │  ┌────────┐  ┌────────┐  ┌────────┐    │
    │  │ Jobs   │  │Interp. │  │ AI     │    │
    │  │ Data   │  │ Data   │  │Context │    │
    │  └────────┘  └────────┘  └────────┘    │
    └──────────────────┬──────────────────────┘
                       │
    ┌──────────────────┴──────────────────────┐
    │        EXTERNAL INTEGRATIONS             │
    ├──────────────┬──────────────┬────────────┤
    │  FastMail    │  Google Cal  │  Webhooks  │
    │  IMAP/SMTP   │  CalDAV API  │  (Zapier)  │
    └──────────────┴──────────────┴────────────┘
```

### System Boundaries

**Interlingo Web App:**
- User interface for job management
- Client-facing features (job board, interpreter profiles, email preview)
- Traditional CRUD operations
- Real-time updates via WebSocket

**PAI Service:**
- AI-powered decision making
- Natural language processing
- Interpreter matching engine
- Email generation and parsing
- Workflow automation
- Voice command processing

**Voice Service:**
- Text-to-speech (ElevenLabs)
- Speech-to-text (future)
- Voice notification delivery
- Multi-voice management

---

## Architecture Components

### 1. Interlingo Web Application

**Technology:** Next.js 14+ (App Router), React, TypeScript, Tailwind CSS, shadcn/ui

**Responsibilities:**
- User authentication and authorization
- Job CRUD operations
- Interpreter management
- Email template preview and editing
- Real-time dashboard
- Mobile-responsive PWA

**Key Pages:**
```
/dashboard           - Overview with widgets
/jobs                - Jobs board with filters
/jobs/[id]           - Job detail page
/jobs/new            - Job creation flow
/interpreters        - Interpreter database
/interpreters/[id]   - Interpreter profile
/settings            - User/org settings
/reports             - Analytics and reports
```

**State Management:**
- React Query (server state)
- Zustand (client state)
- Supabase Realtime (live updates)

---

### 2. PAI Service (AI Brain)

**Technology:** Bun + Express (or Hono for speed), TypeScript

**Port:** `8889` (distinct from voice server on 8888)

**Responsibilities:**
- Natural language understanding
- AI agent orchestration
- Interpreter matching algorithms
- Email generation/parsing
- Workflow automation
- Context management
- Learning from user behavior

**Core Modules:**

```typescript
// Module structure
pai-service/
├── src/
│   ├── agents/
│   │   ├── matching-agent.ts      // Interpreter matching logic
│   │   ├── email-agent.ts         // Email generation/parsing
│   │   ├── voice-agent.ts         // Voice command processing
│   │   └── analytics-agent.ts     // Pattern recognition
│   ├── api/
│   │   ├── routes/
│   │   │   ├── jobs.ts            // Job-related AI endpoints
│   │   │   ├── interpreters.ts    // Interpreter matching
│   │   │   ├── emails.ts          // Email generation
│   │   │   └── voice.ts           // Voice commands
│   │   └── middleware/
│   │       ├── auth.ts            // JWT validation
│   │       ├── rate-limit.ts      // Rate limiting
│   │       └── logging.ts         // Request logging
│   ├── services/
│   │   ├── supabase.ts            // Database client
│   │   ├── claude.ts              // Anthropic API client
│   │   ├── voice.ts               // Voice server client
│   │   └── email.ts               // FastMail client
│   ├── utils/
│   │   ├── context-loader.ts      // Load org-specific rules
│   │   ├── template-engine.ts     // Email template processor
│   │   └── conflict-detector.ts   // Calendar conflict logic
│   └── index.ts                   // Server entry point
├── tests/
├── package.json
└── tsconfig.json
```

**API Endpoints Overview:**
```
POST   /api/match-interpreter       - AI-powered interpreter suggestions
POST   /api/generate-email          - Generate REQ/CONF/REM emails
POST   /api/parse-email-response    - Parse interpreter email replies
POST   /api/voice-command           - Process voice commands
POST   /api/create-job-nl           - Natural language job creation
GET    /api/insights                - Analytics and patterns
POST   /api/conflict-check          - Detect scheduling conflicts
POST   /api/auto-assign             - Automated assignment (with approval)
```

---

### 3. Voice Service (Already Implemented)

**Technology:** Bun + ElevenLabs TTS API

**Port:** `8888`

**Responsibilities:**
- Text-to-speech conversion
- Voice notification delivery
- Multi-voice support (different agents)
- Priority-based queuing

**Current Endpoints:**
```
GET    /health                      - Server health check
POST   /notify                      - Send voice notification
POST   /pai                         - PAI-specific notifications
```

**Enhancements Needed:**
```typescript
// Add speech-to-text for voice commands
POST   /transcribe                  - Convert speech to text

// Add voice command shortcuts
POST   /command/brief               - Morning briefing
POST   /command/status              - Current status
POST   /command/unassigned          - List unassigned jobs
```

---

## Data Flow

### Scenario 1: Manual Job Creation (Traditional)

```
User opens Interlingo → Fills form → Clicks "Create Job"
                                              │
                                              ▼
                                    Next.js Server Action
                                              │
                                              ▼
                                    Supabase Insert (commitment_blocks)
                                              │
                                              ▼
                                    Realtime broadcast to connected clients
                                              │
                                              ▼
                        ┌───────────────────┴───────────────────┐
                        ▼                                       ▼
            Dashboard updates (new job)              Webhook to PAI Service
                                                              │
                                                              ▼
                                            PAI suggests interpreters
                                                              │
                                                              ▼
                                            Voice notification to user
```

### Scenario 2: AI-Assisted Job Creation

```
User: "Chavvo, create job tomorrow 9am Kent Court Spanish certified"
                        │
                        ▼
            Voice Service transcribes speech
                        │
                        ▼
            POST /api/voice-command to PAI Service
                        │
                        ▼
            PAI parses natural language:
            - Date: 2025-10-24
            - Time: 09:00
            - Organization: Kent Municipal Court
            - Language: Spanish
            - Certification: Required
                        │
                        ▼
            PAI calls Interlingo API: POST /api/jobs
                        │
                        ▼
            Job created in Supabase
                        │
                        ▼
            PAI immediately runs matching agent
                        │
                        ▼
            Returns top suggestions to user via voice
                        │
                        ▼
            User: "Assign Elena"
                        │
                        ▼
            PAI updates job, generates REQ email, sends via FastMail
                        │
                        ▼
            Voice confirms: "Elena assigned, REQ email sent"
```

### Scenario 3: Email Response Processing (Automated)

```
Interpreter replies to REQ email
            │
            ▼
FastMail IMAP (email received)
            │
            ▼
Webhook to PAI Service: POST /webhooks/email-received
            │
            ▼
PAI Email Agent parses:
- Thread ID → Matches to job_id
- Sentiment analysis: "Yes" or "No"
- Extract availability details
            │
            ▼
If "Yes": Update job status to Confirmed
If "No": Mark interpreter unavailable, suggest alternatives
            │
            ▼
Voice notification to user:
"Elena accepted Kent job at 9am"
            │
            ▼
PAI asks: "Should I send CONF email?"
            │
            ▼
User: "Yes" (via voice or web UI)
            │
            ▼
PAI generates CONF email, sends, updates status
```

---

## API Design

### PAI Service REST API

#### 1. Interpreter Matching

**Endpoint:** `POST /api/match-interpreter`

**Request:**
```typescript
interface MatchRequest {
  job_id: string;
  language: string;
  certification_required: boolean;
  modality: 'In-Person' | 'Remote' | 'Phone';
  organization_id: string;
  start_time: string; // ISO 8601
  end_time: string;
  location_id?: string;
  priority?: 'normal' | 'urgent';
}
```

**Response:**
```typescript
interface MatchResponse {
  suggestions: Array<{
    interpreter_id: string;
    interpreter_name: string;
    match_score: number; // 0-100
    confidence: 'very_high' | 'high' | 'medium' | 'low';
    reasoning: string[];
    availability: {
      confirmed: boolean;
      conflicts: Array<{
        job_id: string;
        start_time: string;
        end_time: string;
        overlap_minutes: number;
      }>;
    };
    statistics: {
      acceptance_rate: number;
      response_time_avg_minutes: number;
      completion_rate: number;
      organization_preference: boolean;
    };
    estimated_response_time: string; // "< 2 hours"
  }>;
  auto_action?: {
    action: 'assign' | 'send_request' | 'none';
    target_interpreter_id?: string;
    reason: string;
  };
  alternatives_count: number;
}
```

**Algorithm Logic:**
```typescript
// Matching score calculation
const matchScore = (
  languageMatch * 30 +          // Must match (30 points)
  certificationMatch * 25 +     // Cert > Reg > None (25 points)
  availabilityScore * 20 +      // No conflicts (20 points)
  organizationPreference * 15 + // Org prefers this interpreter (15 points)
  historicalReliability * 10    // Past performance (10 points)
);

// Confidence thresholds
if (matchScore >= 90) confidence = 'very_high';
else if (matchScore >= 75) confidence = 'high';
else if (matchScore >= 60) confidence = 'medium';
else confidence = 'low';
```

#### 2. Email Generation

**Endpoint:** `POST /api/generate-email`

**Request:**
```typescript
interface EmailGenerateRequest {
  template_type: 'REQ' | 'CONF' | 'REM';
  job_id: string;
  interpreter_id?: string;
  custom_instructions?: string;
  organization_id: string;
}
```

**Response:**
```typescript
interface EmailGenerateResponse {
  subject: string;
  body: string;
  to: string;
  cc?: string[];
  variables_used: Record<string, any>;
  organization_instructions_applied: boolean;
  estimated_reading_time_seconds: number;
  tone_analysis: {
    formality: 'formal' | 'neutral' | 'friendly';
    urgency: 'urgent' | 'normal' | 'low';
  };
}
```

**Template Processing:**
```typescript
// Load base template
const template = await loadTemplate(template_type);

// Load org-specific instructions
const orgInstructions = await loadOrgInstructions(organization_id);

// Load job data
const job = await supabase.from('commitment_blocks').select('*').eq('id', job_id).single();
const clientRequests = await supabase.from('client_requests').select('*').eq('commitment_block_id', job_id);

// Variable substitution
const variables = {
  'CommitmentBlock.date': formatDate(job.start_time),
  'CommitmentBlock.time': formatTime(job.start_time),
  'CommitmentBlock.modality': job.modality,
  'CommitmentBlock.organization': await getOrgName(job.organization_id),
  'ClientRequest[]': clientRequests.map(cr => ({
    clientName: cr.client_name,
    caseNumber: cr.case_number,
    hearingType: cr.meeting_type,
    charges: cr.charges
  }))
};

// Inject org-specific instructions
const bodyWithInstructions = injectOrgInstructions(template.body, orgInstructions);

// Final rendering
const renderedBody = renderTemplate(bodyWithInstructions, variables);
```

#### 3. Voice Command Processing

**Endpoint:** `POST /api/voice-command`

**Request:**
```typescript
interface VoiceCommandRequest {
  command: string; // Transcribed text
  context?: {
    current_page?: string;
    selected_job_id?: string;
    user_location?: { lat: number; lng: number };
  };
  session_id?: string; // For multi-turn conversations
}
```

**Response:**
```typescript
interface VoiceCommandResponse {
  understood: boolean;
  intent: {
    action: string; // 'create_job', 'assign_interpreter', 'get_status', etc.
    entities: Record<string, any>;
    confidence: number;
  };
  action_taken?: {
    type: string;
    result: any;
    message: string; // Human-readable description
  };
  voice_response: string; // What to speak back to user
  follow_up_question?: string; // If more info needed
  conversation_state?: any; // For multi-turn dialogs
}
```

**Intent Recognition:**
```typescript
// Example intent patterns
const intentPatterns = [
  {
    pattern: /create job (tomorrow|today|\d{4}-\d{2}-\d{2}) at (\d{1,2}:\d{2}|\d{1,2}\s?(am|pm))/i,
    intent: 'create_job',
    extract: ['date', 'time']
  },
  {
    pattern: /assign (\w+\s?\w*) to (.*)/i,
    intent: 'assign_interpreter',
    extract: ['interpreter_name', 'job_identifier']
  },
  {
    pattern: /what('?s| is) (my|today('?s)?|tomorrow('?s)?) (schedule|jobs)/i,
    intent: 'get_schedule',
    extract: ['time_frame']
  },
  {
    pattern: /send (req|conf|rem) (email )?to (\w+)/i,
    intent: 'send_email',
    extract: ['email_type', 'interpreter_name']
  }
];

// Use Claude API for complex queries
if (!simplePatternMatch(command)) {
  const claudeResponse = await anthropic.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    messages: [{
      role: 'user',
      content: `Parse this scheduling command and extract structured data: "${command}"`
    }]
  });
  // Parse Claude's response for entities
}
```

#### 4. Natural Language Job Creation

**Endpoint:** `POST /api/create-job-nl`

**Request:**
```typescript
interface NLJobCreateRequest {
  description: string; // Natural language description
  user_id: string;
}
```

**Response:**
```typescript
interface NLJobCreateResponse {
  parsed_data: {
    date: string;
    time: string;
    organization: string;
    language: string;
    certification_required: boolean;
    modality: string;
    client_name?: string;
    case_number?: string;
    hearing_type?: string;
    charges?: string;
  };
  confidence: number;
  missing_fields: string[];
  clarifications_needed: Array<{
    field: string;
    question: string;
    options?: string[];
  }>;
  job_id?: string; // If created
  next_steps: string[];
}
```

**Implementation:**
```typescript
async function createJobFromNaturalLanguage(description: string) {
  // Step 1: Use Claude to extract structured data
  const claudePrompt = `
You are parsing interpreter scheduling requests. Extract:
- Date and time
- Organization name (must match known orgs)
- Language needed
- Certification required (yes/no)
- Modality (In-Person, Remote, Phone)
- Client details if mentioned

Description: "${description}"

Respond with JSON only.
  `;

  const parsed = await callClaudeAPI(claudePrompt);

  // Step 2: Validate against database
  const orgMatch = await fuzzyMatchOrganization(parsed.organization);
  const languageMatch = await matchLanguage(parsed.language);

  // Step 3: Check for missing required fields
  const required = ['date', 'time', 'organization', 'language', 'modality'];
  const missing = required.filter(f => !parsed[f]);

  if (missing.length > 0) {
    return {
      confidence: 0.6,
      missing_fields: missing,
      clarifications_needed: generateClarificationQuestions(missing)
    };
  }

  // Step 4: Create job
  const job = await createJob(parsed);

  // Step 5: Immediately run matching
  const suggestions = await matchInterpreter(job.id);

  return {
    parsed_data: parsed,
    confidence: 0.95,
    job_id: job.id,
    next_steps: [
      `Job created for ${parsed.date} at ${parsed.time}`,
      `Top suggestion: ${suggestions[0].interpreter_name} (${suggestions[0].match_score}% match)`,
      'Say "Assign [name]" to proceed'
    ]
  };
}
```

---

## Database Architecture

### Supabase Schema Extensions

**New Tables for PAI Integration:**

#### 1. `ai_interpreter_insights`
```sql
CREATE TABLE ai_interpreter_insights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  interpreter_id UUID NOT NULL REFERENCES interpreters(id),

  -- Performance metrics
  acceptance_rate DECIMAL(5,2), -- % of requests accepted
  response_time_avg_minutes INTEGER, -- Avg response time
  completion_rate DECIMAL(5,2), -- % of jobs completed
  cancellation_rate DECIMAL(5,2), -- % of jobs cancelled

  -- Preferences learned by AI
  preferred_organizations UUID[], -- Array of org IDs
  preferred_modalities TEXT[], -- ['Remote', 'In-Person']
  preferred_time_slots JSONB, -- { "monday": ["09:00-12:00"], ... }
  decline_patterns JSONB, -- Reasons for declining

  -- Reliability score (AI-calculated)
  reliability_score INTEGER, -- 0-100
  last_calculated_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_ai_insights_interpreter ON ai_interpreter_insights(interpreter_id);
CREATE INDEX idx_ai_insights_reliability ON ai_interpreter_insights(reliability_score DESC);
```

#### 2. `ai_matching_history`
```sql
CREATE TABLE ai_matching_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID NOT NULL REFERENCES commitment_blocks(id),

  -- What AI suggested
  suggested_interpreters JSONB, -- Array of suggestions with scores
  top_suggestion_id UUID REFERENCES interpreters(id),
  top_suggestion_score INTEGER,

  -- What user chose
  user_selected_id UUID REFERENCES interpreters(id),
  user_accepted_suggestion BOOLEAN, -- Did they pick top suggestion?

  -- Outcome
  interpreter_accepted BOOLEAN,
  interpreter_response_time_minutes INTEGER,
  job_completed BOOLEAN,

  -- Learning
  feedback_score INTEGER, -- User can rate the suggestion
  notes TEXT,

  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_matching_history_job ON ai_matching_history(job_id);
CREATE INDEX idx_matching_history_accepted ON ai_matching_history(user_accepted_suggestion);
```

#### 3. `ai_email_templates`
```sql
CREATE TABLE ai_email_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  template_type TEXT NOT NULL, -- 'REQ', 'CONF', 'REM'
  organization_id UUID REFERENCES organizations(id), -- Org-specific or NULL for default

  subject_template TEXT NOT NULL,
  body_template TEXT NOT NULL,

  -- AI learns from edits
  times_used INTEGER DEFAULT 0,
  times_edited INTEGER DEFAULT 0,
  avg_edit_distance INTEGER, -- How much users modify it

  -- Performance
  avg_response_time_minutes INTEGER, -- How fast interpreters respond
  acceptance_rate DECIMAL(5,2), -- % of REQs that get accepted

  version INTEGER DEFAULT 1,
  is_active BOOLEAN DEFAULT true,

  created_by UUID, -- user_id
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_ai_templates_type_org ON ai_email_templates(template_type, organization_id);
CREATE INDEX idx_ai_templates_active ON ai_email_templates(is_active) WHERE is_active = true;
```

#### 4. `ai_voice_commands_log`
```sql
CREATE TABLE ai_voice_commands_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,

  -- Input
  command_text TEXT NOT NULL,
  audio_duration_seconds INTEGER,

  -- Processing
  intent_detected TEXT,
  confidence_score DECIMAL(5,2),
  entities_extracted JSONB,

  -- Action
  action_taken TEXT,
  action_successful BOOLEAN,
  error_message TEXT,

  -- Response
  voice_response TEXT,
  response_duration_seconds INTEGER,

  -- Metadata
  session_id UUID,
  device_type TEXT, -- 'mobile', 'desktop', 'watch'
  location POINT, -- If available

  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_voice_log_user ON ai_voice_commands_log(user_id);
CREATE INDEX idx_voice_log_intent ON ai_voice_commands_log(intent_detected);
CREATE INDEX idx_voice_log_success ON ai_voice_commands_log(action_successful);
```

#### 5. `ai_conflict_resolutions`
```sql
CREATE TABLE ai_conflict_resolutions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Conflict details
  interpreter_id UUID NOT NULL REFERENCES interpreters(id),
  job_1_id UUID NOT NULL REFERENCES commitment_blocks(id),
  job_2_id UUID NOT NULL REFERENCES commitment_blocks(id),
  conflict_type TEXT NOT NULL, -- 'time_overlap', 'location_distance', 'capacity'

  -- AI suggestion
  suggested_resolution TEXT, -- 'reschedule_job_2', 'assign_alternative', etc.
  alternative_interpreters UUID[], -- If reassignment suggested

  -- User decision
  user_resolution TEXT,
  resolved_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_conflict_interpreter ON ai_conflict_resolutions(interpreter_id);
CREATE INDEX idx_conflict_unresolved ON ai_conflict_resolutions(resolved_at) WHERE resolved_at IS NULL;
```

### Row Level Security (RLS) Policies

```sql
-- Only authenticated users can access AI tables
ALTER TABLE ai_interpreter_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_matching_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_email_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_voice_commands_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_conflict_resolutions ENABLE ROW LEVEL SECURITY;

-- Super Admin (Itza) has full access
CREATE POLICY "Super Admin Full Access" ON ai_interpreter_insights
  FOR ALL USING (auth.uid() IN (
    SELECT id FROM team_members WHERE role = 'super_admin'
  ));

-- Coordinators can read but not delete
CREATE POLICY "Coordinators Read Access" ON ai_matching_history
  FOR SELECT USING (auth.uid() IN (
    SELECT id FROM team_members WHERE role IN ('super_admin', 'coordinator')
  ));

-- Voice commands: users can only see their own
CREATE POLICY "Users Own Voice Logs" ON ai_voice_commands_log
  FOR ALL USING (auth.uid() = user_id);
```

---

## Integration Points

### 1. FastMail Integration (Email)

**IMAP (Incoming Email Monitoring):**
```typescript
// pai-service/src/services/fastmail-imap.ts
import Imap from 'imap';

class FastMailIMAPService {
  private imap: Imap;

  constructor() {
    this.imap = new Imap({
      user: process.env.FASTMAIL_USER,
      password: process.env.FASTMAIL_APP_PASSWORD,
      host: 'imap.fastmail.com',
      port: 993,
      tls: true
    });
  }

  async watchInbox(callback: (email: ParsedEmail) => void) {
    this.imap.once('ready', () => {
      this.imap.openBox('INBOX', false, () => {
        // Listen for new emails
        this.imap.on('mail', async (numNewMsgs) => {
          const emails = await this.fetchLatest(numNewMsgs);
          emails.forEach(callback);
        });
      });
    });

    this.imap.connect();
  }

  async fetchLatest(count: number): Promise<ParsedEmail[]> {
    // Fetch and parse emails
    // Extract: from, subject, body, thread_id, in_reply_to
  }
}

// Usage in PAI service
const imapService = new FastMailIMAPService();
imapService.watchInbox(async (email) => {
  // Check if it's a reply to one of our REQ emails
  const job = await findJobByThreadId(email.thread_id);
  if (!job) return;

  // Parse response (Yes/No)
  const response = await parseInterpreterResponse(email.body);

  if (response.accepted) {
    await updateJobStatus(job.id, 'Confirmed');
    await sendVoiceNotification(`${email.from_name} accepted ${job.organization} job`);
  } else {
    await markInterpreterUnavailable(job.id, email.from_email, response.reason);
    const alternatives = await matchInterpreter(job.id);
    await sendVoiceNotification(`${email.from_name} declined. Suggested alternatives: ${alternatives[0].name}`);
  }
});
```

**SMTP (Outgoing Email):**
```typescript
// pai-service/src/services/fastmail-smtp.ts
import nodemailer from 'nodemailer';

class FastMailSMTPService {
  private transporter: nodemailer.Transporter;

  constructor() {
    this.transporter = nodemailer.createTransport({
      host: 'smtp.fastmail.com',
      port: 465,
      secure: true,
      auth: {
        user: process.env.FASTMAIL_USER,
        pass: process.env.FASTMAIL_APP_PASSWORD
      }
    });
  }

  async sendEmail(email: EmailData): Promise<EmailResult> {
    const result = await this.transporter.sendMail({
      from: process.env.FASTMAIL_USER,
      to: email.to,
      cc: email.cc,
      subject: email.subject,
      text: email.body,
      // Store thread ID for tracking
      headers: {
        'X-Job-ID': email.job_id,
        'X-Template-Type': email.template_type
      }
    });

    // Log sent email
    await supabase.from('communication_log').insert({
      job_id: email.job_id,
      direction: 'outbound',
      type: email.template_type,
      to: email.to,
      subject: email.subject,
      message_id: result.messageId,
      sent_at: new Date().toISOString()
    });

    return result;
  }
}
```

### 2. Google Calendar Integration

**CalDAV API for Read/Write:**
```typescript
// pai-service/src/services/google-calendar.ts
import { google } from 'googleapis';

class GoogleCalendarService {
  private calendar;

  constructor() {
    const auth = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI
    );

    auth.setCredentials({
      refresh_token: process.env.GOOGLE_REFRESH_TOKEN
    });

    this.calendar = google.calendar({ version: 'v3', auth });
  }

  async createEvent(job: Job): Promise<string> {
    const event = {
      summary: `${job.language} - ${job.interpreter_name} - ${job.modality}`,
      description: this.formatJobDescription(job),
      start: {
        dateTime: job.start_time,
        timeZone: 'America/Los_Angeles'
      },
      end: {
        dateTime: job.end_time,
        timeZone: 'America/Los_Angeles'
      },
      attendees: [
        { email: job.interpreter_email }
      ],
      reminders: {
        useDefault: false,
        overrides: [
          { method: 'popup', minutes: 60 },
          { method: 'popup', minutes: 1440 } // 24 hours
        ]
      }
    };

    const result = await this.calendar.events.insert({
      calendarId: 'primary',
      requestBody: event
    });

    return result.data.id;
  }

  async findCaseHistory(caseNumber: string): Promise<PreviousHearings[]> {
    // Search calendar for past events matching case number
    const events = await this.calendar.events.list({
      calendarId: 'primary',
      q: caseNumber,
      timeMax: new Date().toISOString(), // Past events only
      singleEvents: true,
      orderBy: 'startTime'
    });

    return events.data.items.map(e => ({
      date: e.start.dateTime,
      interpreter: extractInterpreterFromSummary(e.summary),
      hearing_type: extractHearingType(e.description),
      charges: extractCharges(e.description)
    }));
  }
}
```

### 3. Webhook System

**Webhook Dispatcher (Interlingo → PAI):**
```typescript
// interlingo-web/src/lib/webhooks.ts
export async function sendWebhook(event: WebhookEvent) {
  const webhookUrl = process.env.PAI_WEBHOOK_URL || 'http://localhost:8889/webhooks';

  try {
    await fetch(`${webhookUrl}/${event.type}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Webhook-Secret': process.env.WEBHOOK_SECRET
      },
      body: JSON.stringify({
        event: event.type,
        data: event.data,
        timestamp: new Date().toISOString()
      })
    });
  } catch (error) {
    console.error('Webhook delivery failed:', error);
    // Queue for retry
    await queueWebhook(event);
  }
}

// Trigger webhooks on key events
export const webhookEvents = {
  JOB_CREATED: 'job.created',
  JOB_UPDATED: 'job.updated',
  JOB_ASSIGNED: 'job.assigned',
  JOB_CONFIRMED: 'job.confirmed',
  EMAIL_SENT: 'email.sent',
  INTERPRETER_UNAVAILABLE: 'interpreter.unavailable'
};
```

**Webhook Receiver (PAI Service):**
```typescript
// pai-service/src/api/routes/webhooks.ts
import { Router } from 'express';

const router = Router();

// Middleware: Verify webhook signature
router.use((req, res, next) => {
  const signature = req.headers['x-webhook-secret'];
  if (signature !== process.env.WEBHOOK_SECRET) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  next();
});

router.post('/job.created', async (req, res) => {
  const { data } = req.body;

  // Immediately run interpreter matching
  const suggestions = await matchInterpreter(data.job_id);

  // Send voice notification with suggestions
  await sendVoiceNotification(
    `New job created for ${data.organization}. Top suggestion: ${suggestions[0].interpreter_name}`
  );

  res.json({ success: true });
});

router.post('/job.assigned', async (req, res) => {
  const { data } = req.body;

  // Generate REQ email
  const email = await generateEmail({
    template_type: 'REQ',
    job_id: data.job_id,
    interpreter_id: data.interpreter_id
  });

  // Optionally auto-send if confidence is high
  if (data.auto_send) {
    await sendEmail(email);
    await sendVoiceNotification(`REQ email sent to ${data.interpreter_name}`);
  }

  res.json({ email });
});

router.post('/email.received', async (req, res) => {
  // Handled by IMAP watcher, but can also accept webhooks
  res.json({ success: true });
});

export default router;
```

---

## Voice Interface

### Voice Command Grammar

**Command Categories:**

**1. Status Queries:**
```
- "What's my schedule today?"
- "Do I have any unassigned jobs?"
- "Who's working tomorrow?"
- "Show me pending responses"
- "What jobs need reminders?"
```

**2. Job Management:**
```
- "Create job tomorrow at 9am Kent Court Spanish certified"
- "Assign Elena to the Kent job"
- "Mark Kent job as confirmed"
- "Cancel the Yakima job"
- "Move the Puyallup job to 2pm"
```

**3. Email Actions:**
```
- "Send REQ email to Elena"
- "Send confirmation to Carlos"
- "Send reminders for tomorrow"
- "Draft CONF email for Kent job"
```

**4. Interpreter Queries:**
```
- "Who can take a Spanish job tomorrow at 9?"
- "Is Elena available tomorrow?"
- "Show me Carlos's schedule"
- "Find certified interpreters"
```

### Multi-Turn Conversations

**Example Dialog:**

```
User: "Create a job for tomorrow"
Chavvo: "What time should the job start?"

User: "9am"
Chavvo: "Which organization is this for?"

User: "Kent Court"
Chavvo: "What language is needed?"

User: "Spanish, certified required"
Chavvo: "Got it. Creating job for Oct 24 at 9am, Kent Municipal Court,
         certified Spanish interpreter. Should this be in-person or remote?"

User: "Remote"
Chavvo: "Job created. I've identified Elena Rodriguez as the top match with
         a 95% score. Should I send her the REQ email?"

User: "Yes"
Chavvo: "REQ email sent to Elena. I'll notify you when she responds."
```

**Implementation:**
```typescript
// pai-service/src/agents/voice-agent.ts
class VoiceConversationManager {
  private sessions: Map<string, ConversationState> = new Map();

  async processCommand(sessionId: string, command: string): Promise<VoiceResponse> {
    let state = this.sessions.get(sessionId) || this.createNewSession();

    // If in middle of multi-turn conversation
    if (state.expecting_response) {
      state = await this.handleFollowUp(state, command);
    } else {
      state = await this.handleNewCommand(state, command);
    }

    this.sessions.set(sessionId, state);

    return {
      voice_response: state.current_response,
      follow_up_question: state.next_question,
      action_taken: state.last_action,
      conversation_complete: !state.expecting_response
    };
  }

  private async handleFollowUp(state: ConversationState, input: string): Promise<ConversationState> {
    // Extract the missing field from user's response
    const field = state.waiting_for_field;
    state.partial_data[field] = input;

    // Check if we have all required fields
    const missingFields = this.getMissingFields(state.partial_data);

    if (missingFields.length === 0) {
      // Complete! Execute the action
      const result = await this.executeAction(state.intent, state.partial_data);
      state.current_response = result.message;
      state.expecting_response = false;
    } else {
      // Ask for next field
      const nextField = missingFields[0];
      state.waiting_for_field = nextField;
      state.next_question = this.generateQuestionFor(nextField);
      state.current_response = state.next_question;
    }

    return state;
  }
}
```

---

## AI/ML Components

### 1. Interpreter Matching Model

**Approach:** Hybrid Rules + ML

**Rules-Based Layer (Filters):**
```typescript
// Hard constraints that must be met
const filters = {
  languageMatch: (interpreter, job) =>
    interpreter.languages.includes(job.language),

  certificationMatch: (interpreter, job) =>
    !job.certification_required ||
    interpreter.certification === 'Certified' ||
    interpreter.certification === 'Registered',

  modalityMatch: (interpreter, job) =>
    interpreter.modality_preferences.includes(job.modality),

  availabilityCheck: async (interpreter, job) =>
    !(await hasConflict(interpreter.id, job.start_time, job.end_time))
};
```

**ML Scoring Layer (Rankings):**
```typescript
// Feature engineering for ML model
const features = {
  // Historical performance
  acceptance_rate: interpreter.acceptance_rate,
  response_time_norm: normalize(interpreter.avg_response_time_minutes, 0, 1440),
  completion_rate: interpreter.completion_rate,

  // Preferences
  org_preference_score: interpreter.preferred_organizations.includes(job.org_id) ? 1 : 0,
  time_preference_match: checkTimePreference(interpreter, job.start_time),

  // Recent patterns
  recent_workload: getRecentJobCount(interpreter.id, days=7),
  days_since_last_job: getDaysSinceLastJob(interpreter.id),

  // Contextual
  is_local: interpreter.is_local && job.modality === 'In-Person',
  has_worked_this_org: hasWorkedOrg(interpreter.id, job.org_id),

  // Decline patterns
  recent_decline_rate: getDeclineRate(interpreter.id, days=30),
  declined_similar_jobs: checkSimilarJobDeclines(interpreter.id, job)
};

// Simple weighted scoring (can be replaced with trained model)
const score = (
  features.acceptance_rate * 25 +
  (1 - features.response_time_norm) * 15 +
  features.completion_rate * 20 +
  features.org_preference_score * 15 +
  features.time_preference_match * 10 +
  (features.is_local ? 10 : 0) +
  (features.has_worked_this_org ? 5 : 0) -
  (features.recent_decline_rate * 10)
);
```

**Future: Train ML Model:**
```python
# Offline training script (Python + scikit-learn)
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load historical matching data
df = pd.read_sql('SELECT * FROM ai_matching_history', conn)

# Features
X = df[['acceptance_rate', 'response_time_norm', 'completion_rate', ...]]

# Target: Was the suggestion accepted AND did interpreter accept?
y = df['user_accepted_suggestion'] & df['interpreter_accepted']

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Export for use in TypeScript
# Use ONNX or similar for cross-language ML model deployment
```

### 2. Email Response Parser

**Sentiment Analysis:**
```typescript
async function parseInterpreterResponse(emailBody: string): Promise<ResponseParsed> {
  // Use Claude API for intelligent parsing
  const prompt = `
Parse this interpreter's email response. Determine:
1. Did they accept or decline the job?
2. If declined, what's the reason?
3. Do they have any questions?
4. Extract any alternative availability mentioned.

Email:
"""
${emailBody}
"""

Respond with JSON only:
{
  "accepted": boolean,
  "declined": boolean,
  "reason": string | null,
  "questions": string[],
  "alternative_availability": string | null,
  "confidence": number
}
  `;

  const response = await anthropic.messages.create({
    model: 'claude-3-5-sonnet-20241022',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }]
  });

  return JSON.parse(response.content[0].text);
}
```

### 3. Pattern Recognition (Analytics)

**Background Job:**
```typescript
// Run nightly to analyze patterns
async function analyzePatterns() {
  // 1. Identify high-demand periods
  const demandPatterns = await analyzeDemandByTimeOfDay();

  // 2. Detect interpreter preferences
  const interpreterPreferences = await learnInterpreterPreferences();

  // 3. Optimize assignment strategies
  const optimizations = await suggestOptimizations();

  // 4. Update AI insights table
  await updateAIInsights({
    demand_patterns: demandPatterns,
    interpreter_insights: interpreterPreferences,
    optimizations: optimizations
  });

  // 5. Generate voice alert if important
  if (optimizations.critical_alerts.length > 0) {
    await sendVoiceNotification(
      `Weekly insight: ${optimizations.critical_alerts[0]}`
    );
  }
}

// Schedule to run nightly at 2am
cron.schedule('0 2 * * *', analyzePatterns);
```

---

## Security & Privacy

### 1. Authentication & Authorization

**User Authentication (Supabase Auth):**
```typescript
// Interlingo uses Supabase Auth
// JWT tokens issued on login, validated on every request

// API Gateway middleware
async function authenticateRequest(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const { data: user, error } = await supabase.auth.getUser(token);

    if (error || !user) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    req.user = user;
    next();
  } catch (error) {
    res.status(500).json({ error: 'Auth verification failed' });
  }
}
```

**Role-Based Access Control:**
```typescript
enum Role {
  SUPER_ADMIN = 'super_admin',
  COORDINATOR = 'coordinator',
  VIEWER = 'viewer'
}

const permissions = {
  [Role.SUPER_ADMIN]: ['*'], // All permissions
  [Role.COORDINATOR]: [
    'jobs.read', 'jobs.create', 'jobs.update',
    'interpreters.read', 'interpreters.update',
    'emails.send'
  ],
  [Role.VIEWER]: ['jobs.read', 'interpreters.read']
};

function requirePermission(permission: string) {
  return async (req, res, next) => {
    const userRole = await getUserRole(req.user.id);
    const userPerms = permissions[userRole];

    if (userPerms.includes('*') || userPerms.includes(permission)) {
      next();
    } else {
      res.status(403).json({ error: 'Insufficient permissions' });
    }
  };
}

// Usage
router.post('/api/jobs',
  authenticateRequest,
  requirePermission('jobs.create'),
  createJob
);
```

### 2. API Security

**Rate Limiting:**
```typescript
import rateLimit from 'express-rate-limit';

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests, please try again later'
});

// Voice command rate limit (more restrictive)
const voiceLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 10, // 10 voice commands per minute
  message: 'Too many voice commands, please slow down'
});

app.use('/api', apiLimiter);
app.use('/api/voice-command', voiceLimiter);
```

**Request Validation:**
```typescript
import { z } from 'zod';

// Validate all incoming data
const JobCreateSchema = z.object({
  start_time: z.string().datetime(),
  end_time: z.string().datetime(),
  organization_id: z.string().uuid(),
  language: z.string().min(1).max(100),
  modality: z.enum(['In-Person', 'Remote', 'Phone']),
  certification_required: z.boolean()
});

router.post('/api/jobs', async (req, res) => {
  try {
    const validated = JobCreateSchema.parse(req.body);
    // Safe to use validated data
  } catch (error) {
    res.status(400).json({ error: 'Invalid input', details: error.errors });
  }
});
```

### 3. Data Privacy

**PII Handling:**
```typescript
// Sensitive fields that should never be logged
const PII_FIELDS = [
  'email', 'phone', 'ssn', 'license_number',
  'client_name', 'case_number', 'charges'
];

function sanitizeForLogging(data: any): any {
  const sanitized = { ...data };

  PII_FIELDS.forEach(field => {
    if (sanitized[field]) {
      sanitized[field] = '[REDACTED]';
    }
  });

  return sanitized;
}

// Usage in logging
logger.info('Job created', sanitizeForLogging(jobData));
```

**Encryption at Rest:**
```sql
-- Supabase has encryption at rest by default
-- For extra-sensitive fields, use pgcrypto

-- Encrypt interpreter notes
CREATE EXTENSION IF NOT EXISTS pgcrypto;

ALTER TABLE interpreters ADD COLUMN internal_notes_encrypted BYTEA;

-- Encrypt on insert
INSERT INTO interpreters (internal_notes_encrypted)
VALUES (pgp_sym_encrypt('sensitive notes', 'encryption-key'));

-- Decrypt on read
SELECT
  pgp_sym_decrypt(internal_notes_encrypted::bytea, 'encryption-key') AS internal_notes
FROM interpreters;
```

---

## Deployment Architecture

### Production Infrastructure

```
┌─────────────────────────────────────────────────────────┐
│                    CLOUDFLARE CDN                        │
│  (DDoS Protection, WAF, SSL, Caching)                   │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐    ┌────────▼────────┐
│  Vercel Edge    │    │  Cloudflare     │
│  (Interlingo    │    │  Workers        │
│   Next.js App)  │    │  (API Proxy)    │
└────────┬────────┘    └────────┬────────┘
         │                      │
         │           ┌──────────┴──────────┐
         │           │                     │
         │    ┌──────▼────────┐   ┌───────▼────────┐
         │    │  PAI Service  │   │  Voice Service  │
         │    │  (Fly.io or   │   │  (Fly.io)       │
         │    │   Railway)    │   │  Port: 8888     │
         │    │  Port: 8889   │   │                 │
         │    └──────┬────────┘   └─────────────────┘
         │           │
         └───────────┴───────────────┐
                                     │
                          ┌──────────▼──────────┐
                          │    SUPABASE         │
                          │  (PostgreSQL +      │
                          │   Realtime +        │
                          │   Storage)          │
                          └──────────┬──────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     │                               │
           ┌─────────▼────────┐         ┌───────────▼──────────┐
           │  FastMail IMAP   │         │  Google Calendar API  │
           │  (Email Watch)   │         │  (CalDAV)             │
           └──────────────────┘         └──────────────────────┘
```

### Deployment Configurations

**Interlingo Web App (Vercel):**
```bash
# vercel.json
{
  "framework": "nextjs",
  "buildCommand": "bun run build",
  "env": {
    "NEXT_PUBLIC_SUPABASE_URL": "@supabase_url",
    "NEXT_PUBLIC_SUPABASE_ANON_KEY": "@supabase_anon_key",
    "PAI_API_URL": "https://pai.yourdomain.com"
  },
  "regions": ["sea1"], # Seattle (closest to you)
  "functions": {
    "api/**/*.ts": {
      "maxDuration": 10
    }
  }
}
```

**PAI Service (Fly.io):**
```toml
# fly.toml
app = "interlingo-pai"

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/nodejs"]

[env]
  PORT = "8889"
  NODE_ENV = "production"

[[services]]
  internal_port = 8889
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[services.concurrency]
  type = "connections"
  hard_limit = 25
  soft_limit = 20

[[services.http_checks]]
  interval = 10000
  timeout = 2000
  path = "/health"

[deploy]
  strategy = "rolling"
  region = "sea" # Seattle
```

**Voice Service (Fly.io):**
```toml
# fly.toml
app = "interlingo-voice"

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/nodejs"]

[env]
  PORT = "8888"

[[services]]
  internal_port = 8888
  protocol = "tcp"

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[deploy]
  strategy = "rolling"
  region = "sea"
```

### Environment Variables

**Development (.env.local):**
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# PAI Service
PAI_API_URL=http://localhost:8889
PAI_WEBHOOK_SECRET=dev-webhook-secret

# Voice Service
VOICE_SERVER_URL=http://localhost:8888
ELEVENLABS_API_KEY=your-elevenlabs-key
ELEVENLABS_VOICE_ID=your-voice-id

# FastMail
FASTMAIL_USER=your-email@fastmail.com
FASTMAIL_APP_PASSWORD=your-app-password

# Google Calendar
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-key
```

**Production (Environment Secrets):**
- Store in Vercel Secrets, Fly.io Secrets
- Never commit to git
- Rotate regularly

---

## Implementation Phases

### Phase 1: Foundation (Q4 2025 - 3 months)

**Month 1: Core Infrastructure**
- [ ] Set up PAI Service API server (Express + Bun)
- [ ] Create API endpoints for interpreter matching (simple version)
- [ ] Build email generation system with template engine
- [ ] Implement Supabase RLS policies for new AI tables
- [ ] Deploy PAI Service to Fly.io
- [ ] Create webhook system (Interlingo → PAI)

**Deliverables:**
- PAI Service running on `pai.yourdomain.com:8889`
- API endpoint: `POST /api/match-interpreter` (rule-based matching)
- API endpoint: `POST /api/generate-email` (template rendering)
- Webhooks firing on job creation

**Month 2: Email Automation**
- [ ] Integrate FastMail IMAP for email monitoring
- [ ] Build email response parser (Claude API)
- [ ] Implement auto-status updates based on email responses
- [ ] Create communication_log tracking
- [ ] Test end-to-end: REQ sent → Response received → Status updated

**Deliverables:**
- IMAP watcher running 24/7
- Email responses automatically parsed
- Job statuses auto-updated
- Voice notifications on email events

**Month 3: Basic Voice Integration**
- [ ] Extend voice server with command endpoints
- [ ] Implement simple voice command parsing (regex-based)
- [ ] Add voice responses for key events
- [ ] Test hands-free job creation

**Deliverables:**
- Voice commands: "What's my schedule?", "Assign Elena to Kent job"
- Voice notifications on: job created, interpreter accepted, conflicts detected
- 50% reduction in time-to-assign

---

### Phase 2: Intelligence (Q1 2026 - 3 months)

**Month 4: AI Matching Engine**
- [ ] Build ML-based interpreter matching
- [ ] Train on historical data
- [ ] Add confidence scoring
- [ ] Implement auto-suggestion UI in Interlingo

**Deliverables:**
- AI matching with 85%+ accuracy
- Match scores with reasoning
- Auto-assign on high-confidence matches (with approval)

**Month 5: Smart Dashboard**
- [ ] Build analytics pipeline
- [ ] Create pattern recognition jobs
- [ ] Implement predictive insights
- [ ] Add proactive alerts

**Deliverables:**
- Weekly analytics reports
- Demand forecasting
- Proactive capacity warnings
- Interpreter preference learning

**Month 6: Natural Language**
- [ ] Implement NL job creation via Claude API
- [ ] Build multi-turn conversation manager
- [ ] Add context awareness
- [ ] Polish voice UX

**Deliverables:**
- Create jobs via voice in <1 minute
- Multi-turn dialogs working
- 80% voice command success rate

---

### Phase 3: Scale (Q2 2026 - 3 months)

**Month 7-9:**
- [ ] Google Calendar full integration
- [ ] Case history auto-lookup
- [ ] Mobile PWA optimization
- [ ] Offline capability
- [ ] Advanced automation workflows

**Deliverables:**
- Zero manual calendar lookups
- Mobile-first experience
- 90%+ automation rate for routine tasks

---

### Phase 4: Advanced AI (Q3-Q4 2026 - 6 months)

**Month 10-15:**
- [ ] Predictive analytics dashboard
- [ ] Autopilot mode (with human oversight)
- [ ] Advanced conflict resolution
- [ ] Business intelligence suite
- [ ] Multi-user collaboration features

**Deliverables:**
- Handle 3-5x volume without additional staff
- Predictive scheduling
- Full business analytics
- Clinton and 3rd onboarded

---

## Technical Stack

### Frontend (Interlingo Web)
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **UI:** React + shadcn/ui + Tailwind CSS
- **State:** React Query + Zustand
- **Auth:** Supabase Auth
- **Realtime:** Supabase Realtime
- **Deployment:** Vercel (Edge Functions)

### Backend (PAI Service)
- **Runtime:** Bun (fast TypeScript runtime)
- **Framework:** Express or Hono
- **Language:** TypeScript
- **Database:** Supabase (PostgreSQL)
- **ORM:** Supabase JS Client
- **AI:** Anthropic Claude API
- **Email:** Nodemailer + IMAP
- **Calendar:** Google Calendar API
- **Deployment:** Fly.io or Railway

### Voice Service
- **Runtime:** Bun
- **TTS:** ElevenLabs API
- **STT:** Whisper API (future)
- **Deployment:** Fly.io

### Infrastructure
- **Database:** Supabase PostgreSQL
- **Storage:** Supabase Storage
- **CDN:** Cloudflare
- **SSL:** Cloudflare + Let's Encrypt
- **Monitoring:** Sentry + Vercel Analytics
- **Logs:** Fly.io Logs + CloudWatch

### Development Tools
- **Package Manager:** Bun
- **Linting:** ESLint + Prettier
- **Testing:** Bun Test (built-in)
- **CI/CD:** GitHub Actions
- **Version Control:** Git + GitHub

---

## Success Metrics

### Phase 1 Targets (Q4 2025)
- Job creation time: 10+ min → <5 min ✅
- Email draft time: 5-10 min → <1 min ✅
- Manual status tracking: 100% → 50% ✅
- Time to assign: 15+ min → 8 min ✅

### Phase 2 Targets (Q1 2026)
- AI matching accuracy: → 85%+ ✅
- Voice command success: → 80%+ ✅
- Time to assign: 8 min → 3 min ✅
- Manual interventions: 50% → 30% ✅

### Phase 3 Targets (Q2 2026)
- Mobile usage: → 50% of actions ✅
- Automation rate: 50% → 70% ✅
- Volume capacity: 1x → 3x ✅

### Phase 4 Targets (Q3-Q4 2026)
- Automation rate: 70% → 90% ✅
- Volume capacity: 3x → 5x ✅
- Predictive accuracy: → 85% ✅
- Team members: 1 → 3 (without proportional time increase) ✅

---

## Next Steps

### Immediate Actions (This Week)
1. **Review and approve this architecture document**
2. **Set up development environment for PAI Service**
   ```bash
   mkdir pai-service
   cd pai-service
   bun init
   bun add express @supabase/supabase-js @anthropic-ai/sdk
   ```
3. **Create API endpoint stubs**
4. **Test first integration: Interlingo → PAI webhook**

### Next Month
1. Build interpreter matching v1 (rule-based)
2. Implement email template engine
3. Deploy PAI Service to production
4. Test end-to-end workflow

---

**Document Version:** 1.0.0
**Last Updated:** 2025-10-22
**Next Review:** Weekly during Phase 1, Monthly after

---

*This architecture is a living document. Update as requirements evolve and new insights emerge.*
