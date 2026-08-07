# Skills

This directory contains Folloze internal-development and reusable skill sources.

For Etai, customers, partners, and general Folloze board agents, install [Folloze MCP Customer Skills](https://github.com/0xTrey/folloze-mcp-customer-skills). Do not infer that every folder here is customer-safe or enabled for installation.

`skills-manifest.json` is the only install allowlist:

- enabled entries may be installed by the repo sync helper;
- disabled/deprecated entries remain as learning sources and are not deleted;
- internal entries require the authorized systems and scope named in their skill;
- an unlisted folder is never auto-discovered or auto-installed.

Board routing:

- general 1:1, campaign, webinar/event, content, industry, customer, or partner build → customer pack router;
- explicit authorized internal demo-instance build or known internal demo-board update → `Folloze-MCP-Demo-Builder`;
- `folloze-campaign-board-builder` → deprecated historical source.

For Folloze-owned experiences, enabled internal workflows may use `folloze-brand-kit`. For any other brand, use Brand Harvester and require validated brand evidence before visual work.
