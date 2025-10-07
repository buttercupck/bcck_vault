---
document_type: Logic Rule
silo: intercom
topic: Interpreter Management
sub_topics: 
  - Data Validation
  - Location
location_type:
applies_to_process:
  - Interpreter Assignments
status: Active
modified: 2025-08-06
date_created: 2025-08-06
---

## Purpose
To determine if an interpreter is considered **local** and therefore eligible for In-Person assignments. This is a foundational rule that other logic notes will call upon.

## Trigger
This logic is executed by a calling workflow (e.g., [[ASSIGN - Filter - Modality]]) that needs to determine an interpreter's location status.

## Conditions
1. The system checks the `timezone_preference` field in the interpreter's profile.
2. The value of this field must be `PDT` or `PST`.

## Action
The rule returns a boolean value:
- **`TRUE`** if the interpreter's timezone preference is `PDT/PST`. The interpreter is considered local.
- **`FALSE`** if the interpreter's timezone preference is not `PDT/PST`. The interpreter is considered non-local.

## Dependencies
- This is a foundational rule and has no dependencies on other logic notes.
- It is a key dependency for the [[ASSIGN - Filter - Modality]] rule.