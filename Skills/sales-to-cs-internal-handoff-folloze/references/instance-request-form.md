# Instance Request Form

## Form

- Title: `New Client Org Request v2`
- Public view URL: `https://docs.google.com/forms/d/e/1FAIpQLSehvz2GwGYX3gdOmgKkIyVEdB8d0rLWYgwfwRX4dnl33Zdxww/viewform`

Prefer the helper script at `scripts/submit_instance_request.py`.

## Field mapping

### Required / high-signal fields

- Work email
  - entry: `1647054609`
- Client email domain
  - entry: `784997538`
- Client type
  - entry: `653536717`
  - options:
    - `Direct Customer`
    - `Agency`
    - `Agency Customer`
    - `OEM Customer`
- Plan
  - entry: `1166270677`
  - options:
    - `Professional`
    - `Premium`
    - `Agency Customer`
- Launch date
  - base entry: `851012498`
  - submit as:
    - `entry.851012498_month`
    - `entry.851012498_day`
    - `entry.851012498_year`
- Admin users
  - entry: `1447814038`
  - plain text
- Non-admin users
  - entry: `869798197`
  - plain text
- Custom subdomain?
  - entry: `2054741714`
  - options:
    - `Yes`
    - `No`
- Requested subdomain
  - entry: `298855314`
- Integration needs
  - entry: `541351615`
  - checkbox options:
    - `None`
    - `Demandbase`
    - `6Sense`
    - `Marketo`
    - `Eloqua`
    - `Salesforce`
    - `MS Dynamics`
    - `SSO`
    - `Advanced Cookie Settings`
    - `Live Events purchased`
    - `Hubspot`
- CC recipients
  - entry: `1331947512`
- Creator licenses
  - entry: `1688581247`
- Collaborators
  - entry: `1422600127`
- Additional technical details
  - entry: `1859564084`

## Default rules

- Default plan to `Professional` if fuzzy plan matching does not produce a reliable answer.
- Only include confirmed admin users.
- Default collaborator count to `0` unless the signed contract says otherwise.
- Only check integration boxes if integrations are included in the signed contract.
- If integrations are included, select every matching integration from the deal notes tech stack.
- Subdomain should usually be `Yes`.
- Exact subdomain value is often `TBD`.

## Recommended details-field content

Use the details field to capture anything that does not fit cleanly in the form:

- starter / custom package nuance when the form only offers coarse plan choices
- signed-scope exclusions
- second admin still pending confirmation
- launch assumptions
- cookie / privacy setup
- brand book implementation needs
- future integrations that are not in launch scope

## Submission notes

- Fetch a fresh `viewform` before submitting so `fbzx` and `partialResponse` are current.
- Submit to the matching `formResponse` endpoint.
- Treat a page containing `Your response has been recorded` as success.
- Prefer dry-run mode first when testing the script.
