# In Scope Features

## Beta Features:

We encourage researchers to test and submit any bugs or vulnerabilities you may identify within beta features. [Current Beta Version](https://app-na2.hubspot.com/l/product-updates/?rollout=260906)
### Customer portal

_(1)_ The customer portal feature is in scope. Please set up your own instance in your test HubSpot account. For instructions, navigate to: [https://knowledge.hubspot.com/inbox/set-up-a-customer-portal](https://knowledge.hubspot.com/inbox/set-up-a-customer-portal)

### Customer connected domain

_(2)_ HubSpot Marketing and CMS customers often host content on the HubSpot platform. Customer connected domains are in scope and CNAME'd to a subdomain like:

- groupXX.sites.hscoscdnYY.net, where XX and YY are the numeric identifiers for the content path.

# In Scope Vulnerabilities

In general, vulnerabilities thought to be introduced by HubSpot's hosting platform, and therefore may affect multiple HubSpot customers, are in-scope for this program. Please report those here. Vulnerabilities that are not HubSpot-introduced will still be investigated and will be reported to the affected customer, but they are not rewardable.

## Cross-site scripting (XSS)

XSS found while authenticated to the app are only eligible for a reward if it executes in the context of hubspot.com. XSS found on [default system domains](https://knowledge.hubspot.com/inbox/set-up-a-customer-portal) (eg. _hs-sites_ or _hubspotpagebuilder_) are only eligible for a reward if all of the below criteria are met:

1. XSS also executes on the connected domain
2. The XSS was introduced by HubSpot

We’ve received XSS submissions on customer sites caused by a vulnerable HubL or JavaScript code written by the customer in the [Design Manager](https://knowledge.hubspot.com/design-manager/a-quick-tour-of-the-design-manager). Those are not rewardable.

_We will make exceptions to these rules for any XSS submitted with an exploit that shows clear security impact to the HubSpot platform._

## Subdomain takeovers

HubSpot owns thousands of subdomains. Researchers who submit a valid subdomain takeover will be rewarded at either P2 or P3 level, depending on impact.

Subdomain takeover reports are in scope only if they meet the following criteria:

- You must include proof that the subdomain is owned by HubSpot.
- You must demonstrate proof-of-concept by hosting a simple, nonmalicious html file under the taken-over subdomain.

## Insecure direct object references (IDORs)

Cross-portal IDORs or privilege escalation issues that allow unauthorized access to sensitive data, different customer portals, or administrative functions are eligible for rewards and will be prioritized based on their impact.

Same-portal IDORs on the HubSpot app where a low-privileged user accesses higher-privileged APIs may be eligible for rewards depending on the impact and data accessed.

**Higher Priority IDORs** (eligible for standard rewards):

- Cross-portal data access or leakage
- Access to [sensitive properties](https://knowledge.hubspot.com/properties/store-health-data#create-phi-properties) or PHI/PII data
- Financial, billing, or payment information access
- Privilege escalation to Super Admin functions
- User account takeover capabilities

**Lower Priority/Informational IDORs** (may be marked as informational):

- Basic CRUD operations on non-sensitive objects within the same portal
- Sharing/permission modifications on non-sensitive content

A same portal IDOR submission may not be eligible for a reward if:

- We determine that the low-privileged user is granted the necessary scope to perform a function.
- The owning team decides it is working as designed. Often, this means that if the IDOR is fixed other functionalities within the app will break.
- It’s a previously accepted (and documented) risk. E.g. Users without `User table access` are still able to view a list of users elsewhere in their HubSpot account as documented [here](https://knowledge.hubspot.com/user-management/hubspot-user-permissions-guide).

**Note:** We reserve the right to mark authorization bypass issues as informational when they involve low-impact administrative functions, even if they represent a technical violation of intended permissions. This allows our team to focus resources on higher-impact security issues while still acknowledging valid findings.

---

# Out Of Scope Vulnerabilities:

The following submission types are excluded from the bounty and therefore not rewardable:

- Reports related to the rate limits applied to an API endpoint
- Login or Forgot Password page brute force
- Denial of service attacks
- Perceived excessive volumes of sent email (e.g., mail flooding)
- Race condition bugs that bypass subscription limits
- Social-engineering of any kind against HubSpot employees or its users
- Vulnerable libraries without a working proof-of-concept
- Clickjacking
- Absent or misconfigured HTTP headers
- Missing best-practice bugs that don’t pose a direct/immediate risk to our company or our users (e.g. missing certificate authority authorization)
- XSS that don’t execute in the context of *.hubspot.com or customer connected domains, and instead only executes on preview domains like hs-sites.com, hubspotpagebuilder.com, hubspotpreview.com, cdn.hubspot.net, and similar domains. These domains are intentionally designed to host untrusted user-supplied data.