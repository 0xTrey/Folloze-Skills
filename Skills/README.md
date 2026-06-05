# Skills

This directory contains standalone Folloze skill projects.

- `account-org-chart` - org-chart generation plus Google Drive placement
- `folloze-sales-doc` - branded Folloze sales and lifecycle document generation
- `folloze-order-form-builder` - net-new Folloze customer order forms from pricing guides, templates, add-ons, discounts, and contract terms
- `folloze-brand-kit` - reusable Folloze messaging, product capability references, proof, voice, colors, and logo source material for downstream skills
- `folloze-morning-brief` - daily read-only GTM brief with calendar, Granola, Gmail, Salesforce, and outbound follow-up verification
- `folloze-campaign-board-builder` - customer-facing marketer workflow from campaign brief to design context, approved wireframe, local editable HTML, automatic QA, and Folloze publish readiness
- `folloze-zoom-deal-room` - Zoom recap intake, buyer-safe deal-room briefs, and MCP/API Folloze board routing
- `Folloze-MCP-Demo-Builder` - vendor-branded Folloze MCP microsite, account page, demo board, and buyer experience builder
- `folloze-one-pager` - account-specific Folloze follow-up one-pagers from call notes, Salesforce, Drive, and account research
- `folloze-sales-handoff` - O&E-facing new-logo Sales Handoff DOCX generation from deal sources and the approved fixed template
- `sales-to-cs-internal-handoff-folloze` - closed-won sales-to-CS handoff docs, kickoff deck, and instance request workflow
- `Salesforce-Update` - evidence-backed Salesforce opportunity updates with manual-only stage recommendations
- `skills-update-folloze` - bootstrap and refresh shared skills from the central GitHub repo and create the standard weekly team updater automation
- `weekly-customer-action-items` - weekly by-account summary of unresolved customer follow-ups from meetings, email, and Slack

Each skill directory is intended to be synced into `~/.codex/skills/<skill-name>` by the repo-level sync script.

The `folloze-brand-kit` skill is the shared source for product capability references. Use its internal pointer for Folloze-employee work, its customer-ready reference for buyer-facing output, and its public-safe reference for public/no-Drive contexts.
