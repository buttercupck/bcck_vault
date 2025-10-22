---
date_created: 2025-07-15 13:10
modified: Tuesday 15th July 2025 13:10:29
silo: Language Interpretation Services
"document_type:": Client Specifics
topic: Client Management
sub_topics:
  - Court Requirements
  - Interpreter Instructions
  - ZOOM Modality
location_type: Court
applies_to_communication: Interpreter Confirmations, Interpreter Reminders
status: Active
organization_name: Yakima County District
---
---
Include the format for names on confirmations and reminders:
**Please double-check that your name on ZOOM appears as: INT 1st initial last name**

Example: **INT H** **Hughes**

`{{ $json.body.data.properties['name.interpeters'].rollup.array[0].title[0].text.content.slice(0,1) }}{{ $json.body.data.properties['name.interpeters'].rollup.array[0].title[0].text.content.substring(8)}}`