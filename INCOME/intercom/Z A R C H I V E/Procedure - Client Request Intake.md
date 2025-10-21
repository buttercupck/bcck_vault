---
date_created: 2025-07-14 12:38
modified: Monday 14th July 2025 12:38:49
silo: Language Interpretation Services
"document_type:": Procedure
topic: Client Request Intake
sub_topics:
  - "[Request Documentation, Information Collection, Initial Logging, Communication Workflow"
process_step_id: "1.0"
involved_parties: Court, Law Office, Internal Coordinator
tools used: Apple Mail, Apple Calendar, OCourt Database
status: Active
---
---

## 1.0 Purpose
To accurately receive, document, and process incoming interpretation requests from organizations via email, ensuring all required details are captured to initiate a **Commitment Block** and its initial **Client Request**, thereby preparing for subsequent **Interpreter Assignment** procedures.

## 1.1 Roles & Responsibilities

### Responsible Party
Currently handled manually by an Internal Coordinator. This role may be reassigned or automated in future [[Interlingo CRM Development - State of Silo|Interlingo CRM]] versions.

### Source of Client Request
Requests originate via email from an organization Point of Contact (POC), typically a court clerk or coordinator.

## 1.2 Required Information to Collect
Ensure the following details are explicitly included in the initial request. If any are missing, check the OCourt Database or reply to the sender to request them.
### Information for the **Commitment Block**:
- **Requesting Entity:** Full name of the organization (e.g., Kent Municipal Court).
- **Modality:** How the interpretation will occur (e.g., Zoom, In-Person, Phone).
- **Date and Time:** Exact date and time the interpretation is required.
- **Duration:** Estimated length of the interpretation (default = 2 hours if not specified).
- **Courtroom Number:** (If applicable for court requests).
- **Zoom Link:** Required if Zoom modality is requested.
### Information for the Initial **Client Request**:
- **Language:** The specific language requested for this initial case (e.g., Swahili).
- **Defendant Full Name:** First and Last Name of the defendant (e.g., Chepsat, Wilfred).
- **Case Number:** (If available for court requests).
- **Hearing Type:** The nature of the court proceeding or attorney meeting (e.g., DUI pretrial).
- **Charges:** Legal charges related to the case.

## 1.3 Tools Used
-   **Apple Mail:** To receive incoming job requests.
-   **Apple Calendar:** **Apple Calendar:** To temporarily log and track initial **Commitment Blocks** and their associated **Client Requests** before **Interpreter Assignment**.
-   **OCourt Database:** For cross-referencing or retrieving missing client/case details.

## 1.4 Procedure Steps

### 1.4.1 Review Incoming Request

1. Confirm all required details for both the **Commitment Block** and the initial **Client Request** are present in the incoming email.
2.  If any required information is missing:
    * First, check the [[OCourt Database]] for the missing details.
    * If not found in OCourt, reply to the sender (the POC) to request the missing information.

### 1.4.2 Create Calendar Event (Pending Calendar)
1.  Open Apple Calendar.
2.  Assign the new client request to the `Pending` calendar.
3.  Use the following format for the calendar event description:
    * **Title:** `[Language] - [Interpreter Name (leave blank initially)] [Modality]`
    * **Location:** `[Oragization Name]`
        * `[Day, Month, Date]`
        * `[Time]`
    * **Body:**
        * `Courtroom [Number]`
        * `Meeting ID: [Zoom ID]`
        * `Password: [Zoom Password]`
        * `[Defendant Last Name, First Name] [Case Number (if available)] — [Hearing Type] [Charges]`
**Important Note for Internal Coordinators:** While the Apple Calendar entry itself represents the initial interpretation request, consider this entry as the **Commitment Block** for the interpreter's time. All subsequent **Client Requests** added to this _same time slot_ (even if a different language that extends duration) must be manually appended to the _body_ of this single calendar event. If an additional language request changes the duration, you _must_ also manually update the event's `Time` to reflect the new **Commitment Block** duration (e.g., changing from a 2-hour to a 3-hour event).
### 1.4.3 Add Interpreter Name (Post-Outreach)
1. Once an interpreter has been successfully contacted and confirmed (following [[Interpreter Assignment SOP]]), update the Apple Calendar event title for the **Commitment Block** to include their name:
    * `Title: [Language] - [Interpreter Name] [Modality]`

### 1.4.4 Begin Interpreter Outreach
1.  Proceed directly to the [[Interpreter Assignment SOP]] for detailed steps on contacting and confirming interpreters.