---
date_created: 2025-07-14 20:53
modified: Monday 14th July 2025 20:53:37
silo: bug_bounty
"document_type:": .js
topic: hubspot
sub_topics: 
process_step_id: 
tools used: chrome, caido
---
---
**Why:** This filename is a dead giveaway. `settings-ui-users` explicitly indicates it's the JavaScript bundle responsible for the **User Interface (UI) and logic related to user settings and management**. This is where you'll most likely find:
- **Form submission logic for adding/editing users.**
- **Client-side validation rules** for user roles, permissions, email addresses, etc. (which we'll want to bypass).
- **API endpoints** specifically for user creation, modification, and permission assignment.
- Definitions of **available user roles** and their associated granular permissions.
- Any **hardcoded default permissions** for new users.
  
  createUser: {
    name: "Create User",
    class: "usage",
    properties: {
        createdUserId: {
            type: "number",
            isOptional: !0 // This means 'true'
        },
        teamCount: {
            type: "number",
            isOptional: !0
        },
        existing: {
            type: "boolean",
            isOptional: !0
        },
        roleNames: "array", // <-- CRITICAL!
        userCount: "number",
        basePermissionsContacts: "boolean", // <-- CRITICAL!
        basePermissionsMarketing: "boolean", // <-- CRITICAL!
        basePermissionsSales: "boolean",     // <-- CRITICAL!
        basePermissionsAdmin: "boolean",     // <-- CRITICAL!
        grantedSuperAdmin: "boolean",        // <-- EXTREMELY CRITICAL!
        requiredCheckout: "boolean",
        assignedToTeam: "boolean",
        importFromCsv: "boolean",
        emailSent: "boolean",
        hasDefaultPermissionSetsAccess: "boolean",
        permissionChoiceSelected: {
            type: ["defaultPermissionSetChoice", "permissionSetChoice", "startFromScratchChoice", "manuallyAssignPermissions", "defaultPermissionsForSeat", "standardUserAccess", "makeSuperAdmin"], // <-- CRITICAL!
            isOptional: !0
        },
        defaultPermissionSet: {
            type: ["super-admin", "cms-developer", "content-marketer", "marketing-manager", "view-only", "sales-manager", "sales-rep", "service-manager", "service-rep", "standard-user", "developer"], // <-- EXTREMELY CRITICAL!
            isOptional: !0
        },
        isCloningUserPermission: "boolean",
        isSalesforceImport: "boolean",
        didUseGranularCobjectPermissions: "boolean",
        seatNames: "array"
    },

var r = n(5)
          , i = n.n(r)
          , a = n(645)
          , o = n(201)
          , s = n.n(o)
          , l = n(7)
          , c = n.n(l)
          , d = n(302)
          , u = n(247)
          , p = n(301);
        const m = "app-users/v1/users"
          , h = ({roleNames: e, usersCount: t}) => new Promise((n => {
            1 === t ? n(!1) : s().post(**"app-users/v1/payloads/adjusted-permissions-count"**, {
                data: {
                    roleNames: e,
                    usersCount: t
                }
            }).then(( ({requiresAsync: e}) => n(e))).catch(( () => n(!0)))
        }
### Next steps are:
1. **Document and Test `app-users/v1/payloads/adjusted-permissions-count`:**
- Add this as another key API endpoint discovery.
- **Immediately send requests to this endpoint via Burp Repeater.**
- **Method:** `POST`
- **Payload:** `{ "data": { "roleNames": ["standard-user"], "usersCount": 1 } }`
- **Variation Tests:**
    - Change `roleNames` to `["super-admin"]`, `["cms-developer"]`, `["developer"]`, or a combination of roles.
    - Vary `usersCount` (e.g., 0, 2, 100).
    - Observe the `requiresAsync` response. Does it give different values based on roles you _shouldn't_ be able to assign? Does it give any other informative error messages or data?