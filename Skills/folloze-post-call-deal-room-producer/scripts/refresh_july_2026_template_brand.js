#!/usr/bin/env node

const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");

const BASE_URL = process.env.FOLLOZE_BASE_URL || "https://app.folloze.com";
const BOARD_ID = 248319;
const EXPECTED_NAME = "[Account Name] - Folloze Resource Center - July 2026 Template";
const OFFICIAL_LOGO =
  "https://cdn.prod.website-files.com/6464087fdf877a12a8bd4cd6/6464087fdf877a12a8bd4d26_folloze-logo.svg";
const CURRENT_PRODUCT_VISUAL =
  "https://cdn.prod.website-files.com/6464087fdf877a12a8bd4cd6/6a29ee9e50e43d6ae5db6abb_Campaigns%20That%20Practically%20Build%20Themselves-p-1600.webp";
const CURRENT_ICONS = [
  "https://cdn.prod.website-files.com/6464087fdf877a12a8bd4cd6/6a29ef42dda19395c99a7a87_build.svg",
  "https://cdn.prod.website-files.com/6464087fdf877a12a8bd4cd6/6a29ef429d9e35578adc8d68_activate.svg",
  "https://cdn.prod.website-files.com/6464087fdf877a12a8bd4cd6/6a29ef427835646e22929e8f_signal.svg",
];
const args = new Set(process.argv.slice(2));
const push = args.has("--push");
const publish = args.has("--publish");
if (publish && !push) throw new Error("--publish requires --push");

function readAccessToken() {
  if (process.env.FOLLOZE_ACCESS_TOKEN) return process.env.FOLLOZE_ACCESS_TOKEN;
  const authPath = path.join(os.homedir(), ".folloze-mcp", "auth.json");
  const raw = JSON.parse(fs.readFileSync(authPath, "utf8"));
  const key = crypto.createHash("sha256").update(BASE_URL).digest("hex").slice(0, 16);
  const tokenSet = raw[key] && raw[key].tokens;
  if (!tokenSet || !tokenSet.access_token) throw new Error("No Folloze access token found");
  if (tokenSet.expires_at && tokenSet.expires_at < Date.now()) {
    throw new Error("Folloze access token is expired");
  }
  return tokenSet.access_token;
}

const token = readAccessToken();

async function api(pathname, method = "GET", body) {
  const response = await fetch(`${BASE_URL}${pathname}`, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/json",
      "Content-Type": "application/json",
      "User-Agent": "Folloze",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!response.ok) {
    const detail = typeof data === "string" ? data : JSON.stringify(data);
    throw new Error(`${method} ${pathname} -> ${response.status}: ${detail.slice(0, 1000)}`);
  }
  return { status: response.status, data };
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function stableStringify(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
    .join(",")}}`;
}

function stripTransientScripts(node) {
  if (!node || typeof node !== "object") return;
  if (Array.isArray(node)) {
    node.forEach(stripTransientScripts);
    return;
  }
  delete node._widgetScripts;
  Object.values(node).forEach(stripTransientScripts);
}

function recomputeHash(config) {
  const hashInput = clone(config);
  hashInput.meta = null;
  const newHash = crypto.createHash("sha1").update(stableStringify(hashInput)).digest("hex");
  config.meta = config.meta || {};
  config.meta.newHash = newHash;
  config.meta.localSaveTime = Date.now();
  config.meta.currentPageName = "default";
  return newHash;
}

function setImage(image, url, alt, bankCategory = "images") {
  image.url = url;
  image.alt = alt;
  image.fit = "contain";
  image.position = "middle-center";
  image.bankCategory = bankCategory;
  image.optimized_url = null;
}

function personalize(config) {
  const page = config.pages.default;
  const sections = page.sections;
  const widgets = page.widgets;
  const ribbons = page.ribbons;

  sections.s_a37f960c.name = "Customer Proof";
  sections.s_bf53c258.name = "Account Priorities";
  sections.s_b6dd011a.name = "Integration And Data Guides";
  sections.s_d9718b7e.name = "Resources From Our Calls";
  sections.s_3f14ea81.name = "Account Resource Center Hero";

  const header = widgets.w_086848fc.data;
  setImage(header.primary_logo.image, OFFICIAL_LOGO, "Folloze", "logos");
  header.primary_logo.size = "small";
  header.primary_logo.with_padding = true;
  header.color.tag_line = "#1C293F";
  header.visibility.secondary_logo = false;
  header.secondary_logo.image = {
    url: "",
    fit: "contain",
    name: "Customer logo placeholder",
    bankCategory: "logos",
    optimized_url: null,
  };

  const hero = widgets.w_a3cbc4b6.data;
  hero.left.paragraph.title =
    '<div class="ql-style-heading1"><span style="color: #5B5BFF;">[Company Name]</span><span style="color: #FFFFFF;">, Welcome to Your Folloze Resource Center.</span></div>';
  hero.left.paragraph.subtitle =
    '<div class="ql-style-heading5"><span style="color: #FFFFFF;" class="ql-weight-lighter">A focused resource center with the presentation, demo recording, examples, integrations, and customer proof your team needs to evaluate Folloze and plan the next step.</span></div>';
  hero.left.paragraph.cta = {
    text: "Book A Meeting",
    type: "flz-secondary",
    action: {
      type: "open_url",
      open_url: {
        open_in_new_window: true,
        url: "https://www.folloze.com/request-demo",
      },
    },
  };
  setImage(hero.right.image.image, CURRENT_PRODUCT_VISUAL, "Folloze campaign builder", "images");
  hero.right.image.image.maxWidth = 680;
  hero.right.image.image_size = "large";
  hero.right.image.horizontal_alignment = "center";

  widgets.w_da2f8d2f.data.subtitle =
    "<div>Start with the account-specific presentation, platform and analytics resources, and the strongest proof for the buyer's evaluation.</div>";
  widgets.w_a364e9cf.data.title =
    '<div class="ql-style-heading4">How Folloze Supports [Company Name]\'s Priorities</div>';
  widgets.w_a364e9cf.data.subtitle =
    "<div>Connect personalized experiences, deal acceleration, buyer signal, and open data workflows in one governed platform.</div>";
  widgets.w_a364e9cf.data.repeatable.columns.forEach((column, index) => {
    setImage(column.icon, CURRENT_ICONS[index % CURRENT_ICONS.length], column.title, "icons");
    column.icon.width = 48;
  });
  widgets.w_361cacdc.data.subtitle =
    "<div>Review the edited demo recording, custom examples, and follow-up resources from our conversations.</div>";
  widgets.w_824bce48.data.title = "<div>Integration Guides For [Company Name]</div>";
  widgets.w_824bce48.data.subtitle =
    "<div>Technical resources for the buyer's CRM, MAP, data, analytics, and activation workflows.</div>";
  widgets.w_a7c29c7c.data.title =
    '<div class="ql-style-heading2">Folloze Customer Stories For <span style="color: #5B5BFF;">[Company Name]</span></div>';

  ribbons.r_946fa8a7.data.background = "background: #FFFFFF";
  ribbons.r_58d6a3dd.data.background =
    "background: radial-gradient(circle at 76% 24%, rgba(91, 91, 255, 0.34), transparent 34%), linear-gradient(135deg, #071428 0%, #0A1230 55%, #1C293F 100%)";
  ribbons.r_714d5d7a.data.background = "background: #F4F8FC";
  ribbons.r_69684a3a.data.background =
    "background: linear-gradient(180deg, #FFFFFF 0%, #F4F8FC 100%)";
  ribbons.r_1fe52ef8.data.background = "background: #FFFFFF";
  ribbons.r_2ec01429.data.background = "background: #FFFFFF";
  ribbons.r_f7787bad.data.background = "background: #F4F8FC";

  stripTransientScripts(config);
  return recomputeHash(config);
}

function itemPayload(item, updates) {
  return {
    id: item.id,
    board_id: item.board_id,
    title: updates.title ?? item.title,
    description: updates.description ?? item.description,
    url: updates.url ?? item.url,
    item_type: item.item_type,
    item_source: item.item_source,
    availability: item.availability,
    item_visibility: item.item_visibility || { status: 1, start_date: null, end_date: null },
    audience_permissions: item.audience_permissions || {},
    categories_ids: updates.categories_ids ?? item.categories_ids ?? [],
    snapshot_disabled: Boolean(item.snapshot_disabled),
    image: item.image,
  };
}

function backup(before) {
  const root = path.join(os.tmpdir(), "folloze-board-248319-backups");
  fs.mkdirSync(root, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const target = path.join(root, `${stamp}.json`);
  fs.writeFileSync(target, `${JSON.stringify(before, null, 2)}\n`);
  return target;
}

async function main() {
  const metadataResponse = await api(`/api/v1/boards/${BOARD_ID}`);
  const metadata = metadataResponse.data[String(BOARD_ID)];
  if (!metadata || metadata.id !== BOARD_ID) throw new Error("Board 248319 could not be resolved");
  if (metadata.name !== EXPECTED_NAME) throw new Error(`Unexpected board name: ${metadata.name}`);
  if (metadata.is_template !== true) throw new Error("Board 248319 is not marked as a template");

  const configResponse = await api(`/api/v1/boards/${BOARD_ID}/config`);
  const config = clone(configResponse.data.unpublished_config);
  const oldHash = config.meta && config.meta.newHash;
  const newHash = personalize(config);
  const transformedText = JSON.stringify(config).toLowerCase();
  const plannedResidue = ["TruTechnologies", "Tru Technologies", "ModoMind", "pharma", "biotech"].filter(
    (term) => transformedText.includes(term.toLowerCase())
  );

  const deckItem = (await api("/api/v1/items/2337351")).data;
  const oncologyItem = (await api("/api/v1/items/2337350")).data;
  const backupPath = backup({ metadata, config: configResponse.data, deckItem, oncologyItem });

  const planned = {
    board_id: BOARD_ID,
    is_template: metadata.is_template,
    mode: push ? "push" : "dry_run",
    publish,
    old_hash: oldHash,
    new_hash: newHash,
    backup_path: backupPath,
    brand: {
      navy: "#071428",
      violet: "#5B5BFF",
      pale_blue: "#F4F8FC",
      official_logo: OFFICIAL_LOGO,
    },
    planned_residue: plannedResidue,
  };
  if (!push) {
    console.log(JSON.stringify(planned, null, 2));
    return;
  }

  await api(`/prism/${BOARD_ID}`, "PUT", {
    board: {
      name: EXPECTED_NAME,
      description:
        "A focused Folloze resource-center template for presentations, demo recordings, examples, integration guides, customer proof, and next-step resources.",
      is_public: false,
    },
  });
  const save = await api(`/api/v1/boards/${BOARD_ID}/config`, "PUT", { config });
  await api(
    "/api/v1/items/2337351",
    "PUT",
    itemPayload(deckItem, {
      title: "Folloze Overview Presentation",
      description:
        "A concise overview of the Folloze platform, capabilities, and buyer experience.",
      categories_ids: [],
    })
  );
  await api(
    "/api/v1/items/2337350",
    "PUT",
    itemPayload(oncologyItem, {
      description:
        "An oncology example showing how live protocol execution, source evidence, and operational action can come together in one focused buyer journey.",
    })
  );
  let publishResult = null;
  if (publish) publishResult = await api(`/api/v1/boards/${BOARD_ID}/publish`, "POST");

  const afterMetadataResponse = await api(`/api/v1/boards/${BOARD_ID}`);
  const afterMetadata = afterMetadataResponse.data[String(BOARD_ID)];
  const afterConfigResponse = await api(`/api/v1/boards/${BOARD_ID}/config`);
  const afterDeck = (await api("/api/v1/items/2337351")).data;
  const activeConfig = afterConfigResponse.data.unpublished_config;
  const publishedConfig = afterConfigResponse.data.published_config;
  const text = JSON.stringify(activeConfig);
  const residue = ["TruTechnologies", "Tru Technologies", "ModoMind", "pharma", "biotech"].filter(
    (term) => text.toLowerCase().includes(term.toLowerCase())
  );

  const result = {
    ...planned,
    save_status: save.status,
    publish_status: publishResult && publishResult.status,
    readback: {
      name: afterMetadata.name,
      is_template: afterMetadata.is_template,
      is_public: afterMetadata.is_public,
      has_published_version: afterMetadata.has_published_version,
      activation_state: afterMetadata.activation_state,
      public_link: afterMetadata.public_link,
      unpublished_hash: activeConfig.meta && activeConfig.meta.newHash,
      published_hash: publishedConfig && publishedConfig.meta && publishedConfig.meta.newHash,
      hashes_match:
        Boolean(publishedConfig && publishedConfig.meta) &&
        activeConfig.meta.newHash === publishedConfig.meta.newHash,
      residue,
      deck_title: afterDeck.title,
      deck_url_preserved: afterDeck.url === deckItem.url,
      stale_deck_hidden_from_categories:
        Array.isArray(afterDeck.categories_ids) && afterDeck.categories_ids.length === 0,
    },
  };

  if (result.readback.is_template !== true) throw new Error("Template flag changed unexpectedly");
  if (result.readback.residue.length) throw new Error(`Template residue remains: ${residue.join(", ")}`);
  if (!result.readback.stale_deck_hidden_from_categories) {
    throw new Error("The stale account-specific deck remains visible in a template category");
  }
  if (publish && !result.readback.hashes_match) throw new Error("Published and unpublished hashes differ");
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
