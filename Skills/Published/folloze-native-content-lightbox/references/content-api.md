# Content API ingestion

The [Folloze Content API 1.0.0 contract](https://folloze-documentation.s3.amazonaws.com/folloze-content-api-1.0.0.json) documents `POST https://content-api.folloze.com/v1/items`. It accepts a URL item or a remotely downloadable file, can attach the item to a board at creation time, and returns HTTP `202` with `folloze_id` and provider identity. The published contract has no GET/readback path or idempotency key. Its update identity is ambiguous, so do not automate `PUT` from this example until the target environment's current update contract is confirmed.

## Authenticate in the target environment

Dev obtains a **dedicated Content API key for that tenant** from its admin or Support. Send the request from a trusted backend with `Authorization: Basic <Base64(client_id:client_secret)>` and `Content-Type: application/json`. If Dev receives a pre-encoded Base64 API key, use that as the Basic value. The key is not Board MCP OAuth and must never be sent to a public board or HTML section. Verify the credential's organization before posting; a successful authentication to a different tenant is not the requested outcome.

## Create a board URL item

Replace every example value with reviewed target-environment values. `provider_name` and `provider_asset_id` should be stable identifiers for the source. Set `is_public`, `status`, `is_gated`, and categories deliberately. `open_in_new_tab:false` matters for a URL item intended for the board viewer.

```json
{
  "title": "Reviewed item title",
  "description": "Short source-grounded description",
  "creator_email": "folloze-user@example.com",
  "is_public": true,
  "provider_name": "target-content-program",
  "provider_asset_id": "stable-source-asset-id",
  "item_type": "url",
  "url_item": {"url": "https://source.example/content"},
  "board_item": {
    "board_id": 123456,
    "status": "online",
    "is_gated": false,
    "open_in_new_tab": false,
    "category_ids": []
  }
}
```

For a file, use `item_type:"file"` and `file_item:{"file_name":"asset.pdf","download_url":"https://source.example/asset.pdf"}` instead of `url_item`. The API downloads the file from that URL. `thumbnail_url` and `tags` are optional. Prefer HTTPS source and thumbnail URLs without embedded credentials. A remote video page is a URL item; a downloadable video file is a file item. Confirm how the viewer renders each type in the target tenant.

This is the server-side call shape. Dev must supply `readTargetTenantKey` from its approved secret mechanism and a reviewed `request` object. Do not use this in board HTML or retry it automatically.

```js
async function createContentItemOnce(request, readTargetTenantKey) {
  const base64Key = await readTargetTenantKey();
  let response;
  try {
    response = await fetch('https://content-api.folloze.com/v1/items', {
      method: 'POST',
      headers: {
        Authorization: `Basic ${base64Key}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request),
      redirect: 'error'
    });
  } catch {
    throw new Error('Create outcome unknown; inspect the board before retry');
  }
  if (response.status !== 202) throw new Error(`Content API returned HTTP ${response.status}`);
  let accepted;
  try { accepted = await response.json(); }
  catch { throw new Error('Accepted but unreadable; inspect the board before retry'); }
  if (!accepted?.folloze_id) throw new Error('Accepted without a readable Folloze ID; reconcile before retry');
  if (accepted.provider_name !== request.provider_name || accepted.provider_asset_id !== request.provider_asset_id) {
    throw new Error('Accepted identity mismatch; inspect the target tenant before retry');
  }
  return {state: 'accepted_async', follozeId: accepted.folloze_id};
}
```

## Apply once, then reconcile

1. Inspect the board and Content Center for the source first. The [board content guide](https://help.folloze.com/s/article/Adding-Content-to-a-Board) recommends reusing detected duplicates.
2. Have a trusted backend load the key from a secret store or one-time hidden input and POST the reviewed JSON. No key belongs in the spec file, shell arguments, stdout, or checked-in receipt. Do not call the Content API from browser JavaScript.
3. Record only nonsecret request identity and the returned `folloze_id`. Call a `202` **accepted_async**. On timeout, transport error, or unreadable `202`, inspect the board before any retry; the item may already have been created.
4. In the signed-in target tenant, verify the Content Center item and attached board item, its source, online status, public/gated choice, new-tab choice, and actual item link. Only then map that link into the HTML section. Content Center IDs and board item IDs are different; do not derive an item URL from either ID or from the title.

This skill does not include a credential, tenant host, or automatic bulk uploader. The target developer chooses the server-side secret mechanism and explicitly authorizes each target-board mutation.
