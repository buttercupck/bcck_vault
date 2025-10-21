---
title: REM - Standard Email Template
type: template
category: REM
status: active
tags:
  - email
  - template
  - reminders
---
# Standard Reminders Email Template

## Purpose
This is the default email template used for all interpreter reminder emails. Specific instructions or information are inserted into the designated placeholder.

---

**Subject:** Reminder: {{CommitmentBlock.time}} {{CommitmentBlock.modality}} Assignment Tomorrow

**Body:**
You are scheduled for {{CommitmentBlock.organization}} tomorrow, {{CommitmentBlock.date.time}}.

[Org Specific Instructions]

{#each CommitmentBlock.clientRequests}}
	{{CommitmentBlock.zoomInformation}}

	{{ClientRequest.clientName}}
	{{ClientRequest.caseNumber}} - {{ClientRequest.hearingType}}
	{{ClientRequest.charges}}
{{/each}}