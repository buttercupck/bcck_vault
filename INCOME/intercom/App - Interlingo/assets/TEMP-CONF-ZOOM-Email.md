---
title: TEMP-CONFIRMATION-ZOOM-Email
type: template
category: CONF
status: active
tags:
  - email
  - template
  - confirmation
---
# Standard Confirmation Email Template

## Purpose
This is the default email template used for all interpreter reminder emails. Specific instructions or information are inserted into the designated placeholder.

---

**Subject:** CONFIRMATION: {{CommitmentBlock.date.time}} {{CommitmentBlock.modality}} 

**Body:**
{{CommitmentBlock.date}}
{{CommitmentBlock.time}} {{CommitmentBlock.modality}}

{{CommitmentBlock.organization}} 

![[Standard Zoom Confirmation (Interpreter)#^cefc35]]

{{CommitmentBlock.zoomInformation}}
{#each CommitmentBlock.clientRequests}}
		{{ClientRequest.clientName}}
	{{ClientRequest.caseNumber}} - {{ClientRequest.hearingType}}
	{{ClientRequest.charges}}
{{/each}}