This document will be used as a silo key for Intercom/Interlingo's properties that can be referenced if later on we have a question about what type of document a certain file is.

## Purpose of the Intercom Company:
	To connect organizations in need of a specific language interpreter for their own clients that speak any language other than English. We are the middle-man between the organizations and the interpreters. 
## Purpose of Project Interlingo:
The primary purpose of this web application is to streamline and enhance communication within the 3-person Intercom Team regarding all interpretation jobs. This includes managing new, pending, and confirmed Interpreter Assignments.
The application will facilitate clear communication with both interpreters and organizations by providing comprehensive details about:
 * Commitment Blocks: The specific time an interpreter is engaged, whether an initial 2-hour period or a modified duration, for a particular organization.
 * Client Requests: Individual interpretation needs for specific clients or cases that fall within an interpreter's Commitment Block, including details like client names, case numbers, and required languages.
The system will enable the Intercom Team to efficiently handle all job-related modifications, such as:
 * Organizational changes like cancellations.
 * Adding new Client Requests to an existing Commitment Block, even if it involves a different language or alters the Commitment Block's total duration.
 * Any changes to an interpreter's availability or capacity to fulfill their Interpreter Assignment.
By consolidating and clearly presenting all necessary information about the Interpreter Assignment, the interpreter, and the organization, the Intercom Team will be empowered to make informed decisions and ensure everyone involved remains up-to-date with the latest information.
 

## Purpose of the Intercom Company:
To connect organizations in need of a specific language interpreter for their own clients that speak any language other than English. We are the middle-man between the organizations and the interpreters. 
## Purpose of Project Interlingo:
The primary purpose of this web application is to streamline and enhance communication within the 3-person Intercom Team regarding all interpretation jobs. This includes managing new, pending, and confirmed Interpreter Assignments.
The application will facilitate clear communication with both interpreters and organizations by providing comprehensive details about:
 * **Commitment Blocks:** The specific time an interpreter is engaged, whether an initial 2-hour period or a modified duration, for a particular organization.
 * **Client Requests**: Individual interpretation needs for specific clients or cases that fall within an interpreter's Commitment Block, including details like client names, case numbers, and required languages.
The system will enable the Intercom Team to efficiently handle all job-related modifications, such as:
 * Organizational changes like cancellations.
 * Adding new Client Requests to an existing Commitment Block, even if it involves a different language or alters the Commitment Block's total duration.
 * Any changes to an interpreter's availability or capacity to fulfill their **Interpreter Assignment.**
By consolidating and clearly presenting all necessary information about the Interpreter Assignment, the interpreter, and the organization, the Intercom Team will be empowered to make informed decisions and ensure everyone involved remains up-to-date with the latest information.

## Structure for system_logic notes:
1. **Categorized**: What type of logic?
2. **Specific**: Which scenario is this for?
3. **Concise**
4. **RAG-Friendly**
	Example: **`[CategoryPrefix]-[SpecificContext]-[Action/Detail]`**
	Prompt: I don't like any of these suggested prefixes. Let's give you a bit of context. Currently there are 3 n8n workflows that handle 3 types of communications, these are currently named with the old naming convention.
5. Request (REQ) - This is sending an email to the interpreter asking them if they are available for the Commitment Block. One branch of the workflow is as follows:
	- Notion Webhook
	- Time reformatting nodes
	- Merge all fields
	- Code node to check if the current time is AM or PM
	- Filter Node; AM or PM
		AM - Filter Node: Does the interpreter need PDT/PST?
		AM TRUE - Switch Node: Is the assignment modality 
		1. Phone 
		2. ZOOM 
		3. Other
- Gmail Nodes with respective email subject line, body information

1. Confirmation (CONF) - This is used once the interpreter accepts the assignment and is sent the confirmation of assignment.
	- Notion Webhook
	- Time reformatting nodes
	- Merge all fields
	- Filter Node: Does the interpreter need PDT/PST?
	- FALSE Switch Node: Which organization is this for?
		- IF Kent Switch Node: 
			- ZOOM
			- In Person
		- IF Federal Way Switch Node:
			- ZOOM
			- In Person
		- IF SLS Switch Node:
			- ZOOM
			- Phone
		- IF Fallback:
			- ZOOM
			- In Person
			- Phone
	- GMAIL Node: Create Draft email.

Reminders (REM) Workflow: This is used a day before of the scheduled assignment to remind the interpreter of their assignment:
- Notion Webhook
- Time reformatting nodes
- Merge all fields
- Filter Node: Does the interpreter need PDT/PST?
- TRUE Switch Node: Which organization is this for?
	- IF Kent
		- Gmail Node
	- IF Federal Way
		- Gmail Node
	- IF SLS Switch Node: 
		- ZOOM
		- Phone
	- Puyallup Switch Node: 
		- ZOOM
		- Phone
	- Kireshenbaum Switch Node: 
		- ZOOM
		- Phone
	- Yakima Switch Node: 
		- District Court
		- Superior Court
	- Fallback
		- ZOOM 
		- Phone
	- GMAIL Node: Create Draft email


==`documentation_types`==:
- **`Process Flow`**: High-level overview of a multi-step business process.
- **`Procedure`**: Detailed, step-by-step instructions for performing a task.
	- `process_step_id` 
- **`Business Rule`**: A specific policy, constraint, or condition that governs operations.
- **`Communication Template`**: Reusable content for outgoing messages (email, SMS).
- **`Data Field Definition`**: Detailed explanation of a specific data field.
- **`Client Specifics`**: Unique requirements, preferences, or instructions for a particular organization (client, court, law office).
- **`Workflow Automation`**: Documentation of an automated workflow's logic (like your N8N workflow's overall function).
	-  **Gmail nodes (`message` and `subject` fields):** These become `Communication Template` notes.
	- **`Switch` nodes (`conditions` and `outputKey`):** These become `Business Rule` notes detailing the selection logic.
	- **`dateTime` nodes (`operation`, `format`, `outputFieldName`):** These contribute to `Data Field Definition` notes (explaining formatting rules for specific data points).
- **`Supabase Schema`**: Documentation for your database tables/columns.

==`location_type:`== is indeed meant to be the _category_ of the location/organization, not the actual name of the organization.
- **`Court`**
- **`Law Offices`** 

==`organiztion_name`==: To store the exact name of the organization this note pertains to.

==`applies_to_communication`==: [Interpreter Confirmations, Interpreter Reminders]

==`template_scope_organization`==: