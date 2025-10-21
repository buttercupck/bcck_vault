`[[CRM Common DLB Index.js - 1.3890]]` note. Detail the `makeRequestBody` and `makeRequestKey` structures.
/api/inbounddb-objects/v2/batch-mutation/dynamic-search
`{"type":"UPDATE","objectTypeId":"0-1","properties":[{"name":"hs_content_membership_status","value":"inactive"}],"objectIdList":["159295655623","157450606329","156060327613"]}`

**CRM Object Management:** * 
`[[Data Import Vulnerabilities]]` 
* *Update (2025-07-15):* Direct batch API endpoint `/inbounddb-objects/v2/batch-mutation/dynamic-search` appears well-guarded by robust CSRF protection for direct replay. Pivoting investigation to other areas. 
* `[[Bulk Delete Functionality]]` 
* *Update (2025-07-15):* See notes on [[InboundDB Batch Mutations]] regarding CSRF challenge. 

Current Investigation Focus: * **Pivoting to: [[Planout A/B Testing Framework]] to explore client-side feature flag bypasses.** * **Also exploring: [[CRM Common DLB Bundle]] for alternative API endpoints or different batching mechanisms.** * (Add any other areas you decide to focus on next)