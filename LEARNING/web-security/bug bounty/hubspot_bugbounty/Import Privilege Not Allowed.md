---
date_created: 2025-07-26 14:23
modified: Saturday 26th July 2025 14:23:21
silo: bug_bounty
"document_type:": Findings
topic: hubspot
sub_topics:
  - Privilege Escalation
process_step_id: 
involved_parties: 
tools used: Chrome
---
---
**`"__esModule"`**

- This is the key part! `__esModule` is a **non-standard, but widely adopted, "marker" property**. It's a convention primarily used by **transpilers (like Babel or TypeScript)** and **module bundlers (like Webpack, Rollup, Parcel, etc.)** to indicate that a particular CommonJS module was originally written as an **ES Module (ECMAScript Module)**.
Privilege Escalation 
# Import Privilege Not Allowed

### Found in
https://app-na2.hubspot.com/api/app-users/v1/users/permissions-and-seats/bulk?portalId=242862774&clienttimeout=14000&hs_static_app=settings-ui-users&hs_static_app_version=1.55917

[
    {
        "userId": 159548558,
        "roles": [
            "crm-importer",
            "contacts-base",
            "core-seat-base"
        ],
        "seatNames": [
            "core"
        ]
    }
]

### **Putting it Together & Next Steps**

These findings strongly suggest the following flow:

1. You (as a super admin) navigate to a user's settings.
2. You open an "Edit User" modal.
3. Inside this modal, you find and toggle the "Import Privilege" button (which has `data-test-toggle="crm-importer"`).
4. This toggle **updates the state of the form within the modal** (e.g., adds or removes `"crm-importer"` from a local list of roles in the JavaScript).
5. You then click the "Save" button (`id="edit-user-modal-save-button"`).
6. **This "Save" button click triggers the actual network request** to the backend, sending the _updated_ user roles (including or excluding `crm-importer`) to be saved. The first JSON snippet is likely the _payload_ of that request, or the _response_ from it.

const handleSave = (hasCheckedOut = false) => {
    if (checkoutRequired && !hasCheckedOut) {
      setShowCheckout(true);
    } else {
      if (isManagingPermissionSet) {
        dispatch(savePermissionSets({ // Path 1: Saving permission sets directly
          permissionSets: stagedPermissionSets,
          stagedPermissions: currentPermissions,
          isBulk,
          track: tracker.track,
          contextCallback,
          callback: banner => {
            onSave(banner);
            // TRUSH TODO: Is this still necessary? I can't seem to reproduce the previous issue without it anymore.
            if (shouldResetState) {
              dispatch(resetState());
            }
          },
          stagedPermissionSetUsers: stagedPermissionSetUsers.toSet(),
          permissionSetAssignments: (permissionSetAssignments === null || permissionSetAssignments === void 0 ? void 0 : permissionSetAssignments.assignments) || []
        })).catch(() => {});
      } else if (**restProps.use === USAGE_TYPES.EDIT_USER) { // Path 2: Editing individual users (your case!)**
        dispatch(updateUsers(updateUsersPayload, checkoutRequired, tracker.track, contextCallback, onSave, showViewUserLink));
      }
    }
  };
  
**`restProps.use === USAGE_TYPES.EDIT_USER`**: **This is your path!** When you are editing an individual user's permissions, this condition will be true.

## You have successfully traced the journey!

1. Your HTML toggle (`data-test-toggle="crm-importer"`) is part of a form/modal for editing user permissions.
2. Flipping the toggle modifies a local state variable (like `updateUsersPayload` or the `stagedPermissions` within the modal).
3. When you click the "Save" button, the `handleSave` function is called.
4. Inside `handleSave`, because you're editing an individual user, the `dispatch(updateUsers(...))` line is executed.
5. This `updateUsers` action (which is what `bulkUpdateUsersWithSeats` in `UsersApi.ts` likely calls) then sends the network request to the backend with the updated user roles, including the `crm-importer` status.

# Where is `updateUsers`  defined?

if (canApplyPermissionSets) {
    const permissionSetIds = getAppliedPermissionSets(state);
    if (permissionSetIds.length > 0 && permissionSetIds.every(id => id > 0)) {
      const onSuccessfulPermissionSetAssignment = () => {
        dispatch(getUpdateUsersSuccessAction(payload, isFromCheckout, callback, track, contextCallback, showViewUserLink));
      };
      const firstUser = payload.first();
      const seatNames = firstUser ? firstUser.seatNames : undefined;
      dispatch(bulkAssignPermissionSet(permissionSetIds, userIds, false, track, contextCallback, isFromCheckout, seatNames, onSuccessfulPermissionSetAssignment, callback));
    } else {
      dispatch(removePermissionSetAssignment(permissionSetIds, userIds, track, contextCallback));
      dispatch(updateUsersPermissions(payload, isFromCheckout, callback, track, contextCallback, showViewUserLink));
    }
  } else {
    **dispatch(updateUsersPermissions(payload, isFromCheckout, callback, track, contextCallback, showViewUserLink))**;
  }
};

"[{\"userId\":159548558,\"roles\":[\"contacts-base\",\"core-seat-base\"],\"seatNames\":[\"core\"]}]"

**`j: 3`**: This is likely some internal variable, perhaps related to the state or a counter.

{"nudgeEvents":[{"type":"ACTION_TAKEN","session_id":"a503e0f0-224b-4dae-9ec7-17c0111a533a","from_automated_test":false,"event_timestamp":1753569045666,"url":"app-na2.hubspot.com/settings/242862774/users","app_name":"settings","locale":"en-us","xpath":"/html/body/div[10]/div/div/div/div/div/div/section/div/div/div/div[3]/button","nudge":{"type":"MODAL","title":"user-configuration-lib.labels.editModalHeader"},"action_component":{"type":"button","id":"edit-user-modal-save-button","text":"user-configuration-lib.labels.save","variant":"other","locale":"en-us"}}]}

{
    "userId": 159548558,
    "roles": [
        "crm-importer", 0
        "contacts-base", 1
        "core-seat-base" 2
    ],
    "seatNames": [
        "core"
    ]
}


## !You now know the exact data structure used to communicate this permission to the backend.

You toggled "import to on" for a user in the Super Admin browser. Let's assume that user ID was `12345`. So your captured JSON payload likely has `"userId": 12345`.

Low-Privilaeged userId: 159548558
Super Admin userId: 
portalId: 242862774

ATTACK:   
https://app-na2.hubspot.com/api/app-users/v1/users/permissions-and-seats/bulk?portalId=242862774&clienttimeout=14000&hs_static_app=settings-ui-users&hs_static_app_version=1.55917

PAYLOAD:
{
    "userId": 159548558,
    "roles": [
        "contacts-base",
        "core-seat-base"
    ],
    "seatNames": [
        "core"
    ]
}

**Congratulations!** While you didn't find a vulnerability (which is often the goal in security, but not always what testers secretly hope for!), you successfully executed a proper privilege escalation test and verified that a critical authorization control is in place.

**Recommendation: Pivot to XSS, but keep your knowledge of the API**
