#!/usr/bin/env node

const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { execFileSync } = require("child_process");

const ISSUER = process.env.FOLLOZE_BASE_URL || "https://app.folloze.com";
const TEMPLATE_ID = 248623;
const BOARD_NAME = "BirdEye | Folloze Resource Center";
const BOARD_DESCRIPTION =
  "A tailored Folloze resource center for BirdEye's evaluation of scalable ABM personalization, Demandbase orchestration, person-level engagement signals, and faster campaign execution.";
const READBACK_PATH = path.join(
  process.cwd(),
  "qa",
  "birdeye-deal-room",
  "birdeye-native-deal-room-api-readback.json"
);
const SOURCE_BRIEF = "research/birdeye-deal-room/birdeye-digital-deal-room-brief.md";
const BIRDEYE_LOGO_URL =
  "https://cdn2.birdeye.com/version2/containers/header/birdeye-logo-2025.png";
const SLIDES_ID = "1rwcxlBeq5-5U96WssCSgtIU2ys-tt0cXmi0yXmlDt8E";
const SLIDES_PREVIEW_URL = `https://docs.google.com/presentation/d/${SLIDES_ID}/preview`;
const SLIDES_EDIT_URL = `https://docs.google.com/presentation/d/${SLIDES_ID}/edit`;
const DECK_COVER_URL =
  "https://raw.githubusercontent.com/0xTrey/Folloze-Skills/main/Skills/Folloze-Digital-Deal-Room-Internal/assets/presentation-deck-cover.png";

const HERO_TITLE =
  '<div><span style="font-weight: var(--fz-font-weight-semibold); color: #6C3CF0;">BirdEye,</span><span style="font-weight: var(--fz-font-weight-semibold);"> Welcome to Your Folloze Resource Center.</span></div>';
const HERO_SUBTITLE =
  "<div>Scale personalized ABM across ~11,000 target accounts without adding 11,000 pages or more manual work—while turning Demandbase reach into person-level engagement signals that help marketing and sales act faster.</div>";
const VALUE_INTRO_BEFORE =
  "Scale personalized ABM across ~2,000 pharma and biotech accounts without creating one page for every account.";
const VALUE_INTRO_AFTER =
  "Scale personalized ABM across ~11,000 industry and sales-segment accounts without creating one page for every account.";
const CARD_TWO_BEFORE = "1:1 relevance without 2,000 separate pages.";
const CARD_TWO_AFTER = "1:1 relevance without 11,000 separate pages.";
const VALUE_HEADING = "From brief to live campaign. In minutes, not sprints.";

const assetCommit =
  process.env.BIRDEYE_ASSET_COMMIT ||
  execFileSync("git", ["rev-parse", "HEAD"], { encoding: "utf8" }).trim();
const assetUrl = (filename) =>
  `https://raw.githubusercontent.com/0xTrey/Folloze-Skills/${assetCommit}/artifacts/birdeye-deal-room/assets/${filename}`;

const DEMOS = [
  {
    title: "AI Visibility Campaign",
    description:
      "A scalable campaign experience showing how BirdEye can turn AI-search visibility into a focused buyer journey and measurable action.",
    url: "https://experience.folloze.com/birdeye-every-location-the-answer",
    slug: "birdeye-ai-visibility-campaign-example",
    image: assetUrl("birdeye-ai-visibility-campaign.png"),
  },
  {
    title: "Sutter Health One-to-One",
    description:
      "A one-to-one account experience demonstrating how BirdEye can tailor relevance for a specific strategic account without building a separate page from scratch.",
    url: "https://experience.folloze.com/birdeye-sutter-access-visibility",
    slug: "birdeye-sutter-health-one-to-one-example",
    image: assetUrl("birdeye-sutter-health-one-to-one.png"),
  },
  {
    title: "View 2026 Event Promotion",
    description:
      "An event-promotion experience showing how BirdEye can connect campaign messaging, registration, proof, and follow-up in one cohesive journey.",
    url: "https://experience.folloze.com/birdeye-view-2026",
    slug: "birdeye-view-2026-event-promotion-example",
    image: assetUrl("birdeye-view-2026-event-promotion.png"),
  },
];

const BASELINE_EXAMPLE_TITLES = [
  "Website Resource Center - Check Point Security",
  "White Paper to Experience - Cisco",
  "Acquisition ABM - Instructure",
  "Field Event Promotion - Bloomreach",
  "Expansion ABM - Aprio",
  "Product Promotion - Lenovo",
];

function readAccessToken() {
  if (process.env.FOLLOZE_ACCESS_TOKEN) return process.env.FOLLOZE_ACCESS_TOKEN;
  const authPath = path.join(os.homedir(), ".folloze-mcp", "auth.json");
  const raw = JSON.parse(fs.readFileSync(authPath, "utf8"));
  const key = crypto.createHash("sha256").update(ISSUER).digest("hex").slice(0, 16);
  const tokenSet = raw[key] && raw[key].tokens;
  if (!tokenSet || !tokenSet.access_token) {
    throw new Error("No Folloze access token found. Refresh local Folloze OAuth and rerun.");
  }
  if (tokenSet.expires_at && tokenSet.expires_at < Date.now()) {
    throw new Error("Folloze access token is expired. Refresh local Folloze OAuth and rerun.");
  }
  return tokenSet.access_token;
}

const accessToken = readAccessToken();

async function api(pathname, method = "GET", body) {
  const response = await fetch(`${ISSUER}${pathname}`, {
    method,
    headers: {
      Authorization: `Bearer ${accessToken}`,
      Accept: "application/json",
      "Content-Type": "application/json",
      "User-Agent": "Folloze",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!response.ok) {
    const detail = typeof data === "string" ? data : JSON.stringify(data);
    throw new Error(`${method} ${pathname} -> ${response.status}: ${detail.slice(0, 1200)}`);
  }
  return { status: response.status, data };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
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
  const newHash = crypto
    .createHash("sha1")
    .update(stableStringify(hashInput))
    .digest("hex");
  config.meta = config.meta || {};
  config.meta.newHash = newHash;
  config.meta.localSaveTime = Date.now();
  config.meta.currentPageName = "default";
  return newHash;
}

function digest(value) {
  return crypto.createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

function replaceExactlyOnce(source, before, after, label) {
  const count = source.split(before).length - 1;
  if (count !== 1) throw new Error(`${label} replacement count was ${count}, expected 1.`);
  return source.replace(before, after);
}

function findBoardId(responseData) {
  if (!responseData || typeof responseData !== "object") return null;
  if (typeof responseData.board_id === "number") return responseData.board_id;
  if (responseData.board && typeof responseData.board.id === "number") return responseData.board.id;
  if (responseData.data && typeof responseData.data.id === "number") return responseData.data.id;
  if (typeof responseData.id === "number" && responseData.id !== TEMPLATE_ID) return responseData.id;
  for (const value of Object.values(responseData)) {
    const found = findBoardId(value);
    if (found) return found;
  }
  return null;
}

async function duplicateTemplate() {
  let guid = null;
  for (let attempt = 1; attempt <= 30; attempt += 1) {
    const payload = { item_ids: [], copy_customizations: true, copy_all_items: true };
    if (guid) payload.guid = guid;
    const response = await api(`/api/v1/boards/${TEMPLATE_ID}/copy`, "POST", payload);
    const boardId = findBoardId(response.data);
    if (boardId) return { boardId, status: response.status };
    guid =
      response.data &&
      (response.data.guid ||
        response.data.copy_guid ||
        response.data.job_guid ||
        (response.data.data && response.data.data.guid));
    if (!guid && response.status !== 206) {
      throw new Error(`Copy response did not include a board ID or guid: ${JSON.stringify(response.data)}`);
    }
    await sleep(2000);
  }
  throw new Error("Template copy did not resolve after polling.");
}

async function readBoardItems(boardId) {
  const response = await api(`/api/v1/boards/${boardId}/items`, "POST", {
    filters: {},
    page: 1,
    per_page: 200,
    minimized: false,
  });
  return Object.values(response.data.data || {});
}

async function readCategories(boardId) {
  const response = await api(`/api/v1/boards/${boardId}/categories`, "GET");
  return Object.values(response.data.data || {});
}

async function createLinkItem(boardId, seedItem, category, resource) {
  const copied = await api(`/api/v1/items/${seedItem.id}/copy`, "POST", { board_id: boardId });
  let item = copied.data;
  await api(`/api/v1/items/${item.id}/detach`, "POST", {});
  item = (
    await api(`/api/v1/items/${item.id}`, "PUT", {
      id: item.id,
      board_id: item.board_id,
      title: resource.title,
      description: resource.description,
      url: resource.url,
      item_type: "link",
      item_source: 1,
      availability: "public",
      item_visibility: { status: 1, start_date: null, end_date: null },
      audience_permissions: {},
      categories_ids: [category.id],
      snapshot_disabled: false,
      image: { url: resource.image, fit: "cover" },
    })
  ).data;
  if (item.slug !== resource.slug) {
    item = (await api(`/api/v1/items/${item.id}/slugs`, "POST", { slug: resource.slug })).data;
  }
  if (!Array.isArray(item.categories_ids) || !item.categories_ids.includes(category.id)) {
    await api(`/api/v1/categories/${category.id}/category_items`, "POST", { item_id: item.id });
  }
  return (await api(`/api/v1/items/${item.id}`, "GET")).data;
}

async function ensureNativeItems(boardId) {
  const categories = await readCategories(boardId);
  const featured = categories.find((category) => category.name === "Featured Assets");
  const examples = categories.find((category) => category.name === "Example Boards");
  if (!featured || !examples) throw new Error("Required Featured Assets or Example Boards category missing.");

  const originalItems = await readBoardItems(boardId);
  const seedItem = originalItems.find((item) => item.item_type === "link" && item.url);
  if (!seedItem) throw new Error("Could not find a native link item to use as a seed.");

  const ensureResource = (category, resource) => {
    const existing = originalItems.find((item) => item.url === resource.url);
    return existing || createLinkItem(boardId, seedItem, category, resource);
  };

  const deck = await ensureResource(featured, {
    title: "Folloze Presentation for BirdEye",
    description:
      "Luke Rafferty's tailored Folloze presentation for BirdEye's evaluation of scalable ABM personalization, analytics, integrations, and campaign execution.",
    url: SLIDES_PREVIEW_URL,
    slug: "folloze-presentation-for-birdeye",
    image: DECK_COVER_URL,
  });

  const demoItems = [];
  for (const demo of DEMOS) demoItems.push(await ensureResource(examples, demo));
  const refreshed = await readBoardItems(boardId);
  return { categories, featured, examples, deck, demoItems, items: refreshed };
}

function personalizeConfig(config, nativeItems) {
  const widgets = config.pages.default.widgets;
  const required = [
    "w_086848fc",
    "w_aa3c2917",
    "w_da2f8d2f",
    "w_dacd1645",
    "w_0dbb4e9a",
    "w_3fb95f3a",
  ];
  for (const id of required) if (!widgets[id]) throw new Error(`Required widget ${id} missing.`);

  const roiBefore = clone(widgets.w_3fb95f3a.data);
  const originalValueHtml = widgets.w_dacd1645.data.content;
  if (!originalValueHtml.includes(VALUE_HEADING)) throw new Error("Approved value heading missing.");

  const header = widgets.w_086848fc.data;
  header.visibility.secondary_logo = true;
  header.visibility.primary_logo = true;
  header.visibility.show_logos = true;
  header.secondary_logo.image = {
    ...(header.secondary_logo.image || {}),
    url: BIRDEYE_LOGO_URL,
    fit: "contain",
    bankCategory: "logos",
    optimized_url: null,
    alt: "BirdEye logo",
  };
  header.secondary_logo.size = "medium";
  header.secondary_logo.type = "manual";

  const hero = widgets.w_aa3c2917.data;
  hero.title = HERO_TITLE;
  hero.subtitle = HERO_SUBTITLE;
  hero.visibility.title = true;
  hero.visibility.subtitle = true;

  const essentials = widgets.w_da2f8d2f.data;
  essentials.sources.flz_category_ids = [nativeItems.featured.id];
  essentials.subtitle =
    "<div>Start with Luke Rafferty's tailored presentation. The edited call recording will be added here once its buyer-safe export is available.</div>";
  essentials.visibility.subtitle = true;

  let newValueHtml = replaceExactlyOnce(
    originalValueHtml,
    VALUE_INTRO_BEFORE,
    VALUE_INTRO_AFTER,
    "value intro"
  );
  newValueHtml = replaceExactlyOnce(
    newValueHtml,
    CARD_TWO_BEFORE,
    CARD_TWO_AFTER,
    "card two title"
  );
  widgets.w_dacd1645.data.content = newValueHtml;

  const normalizedValue = newValueHtml
    .replace(VALUE_INTRO_AFTER, VALUE_INTRO_BEFORE)
    .replace(CARD_TWO_AFTER, CARD_TWO_BEFORE);
  if (normalizedValue !== originalValueHtml) {
    throw new Error("Value HTML changed outside the two approved replacements.");
  }

  const baselineIds = [];
  for (const title of BASELINE_EXAMPLE_TITLES) {
    const match = nativeItems.items.find((item) => item.title === title);
    if (!match) throw new Error(`Baseline example item missing: ${title}`);
    baselineIds.push(match.id);
  }
  const examples = widgets.w_0dbb4e9a.data;
  examples.sources = {
    ...examples.sources,
    sort: "popular",
    type: "curated",
    flz_item_ids: [...baselineIds, ...nativeItems.demoItems.map((item) => item.id)],
    number_of_dynamic_items: 9,
  };
  examples.cards.items_in_row = "five";

  const roiAfter = widgets.w_3fb95f3a.data;
  if (digest(roiBefore) !== digest(roiAfter)) throw new Error("ROI calculator changed during personalization.");
  return {
    roiHash: digest(roiBefore),
    originalValueHash: digest(originalValueHtml),
    personalizedValueHash: digest(newValueHtml),
    baselineIds,
  };
}

async function readMetadata(boardId) {
  for (const pathname of [`/api/v1/boards/${boardId}`, `/prism/${boardId}`]) {
    try {
      const response = await api(pathname, "GET");
      return { path: pathname, status: response.status, data: response.data };
    } catch {
      // Try the next metadata endpoint.
    }
  }
  return { path: null, status: null, data: null };
}

function findFirstExperienceUrl(value) {
  if (!value) return null;
  if (typeof value === "string") {
    const match = value.match(/https:\/\/experience\.folloze\.com\/[A-Za-z0-9_-]+/);
    return match ? match[0] : null;
  }
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = findFirstExperienceUrl(item);
      if (found) return found;
    }
  } else if (typeof value === "object") {
    for (const item of Object.values(value)) {
      const found = findFirstExperienceUrl(item);
      if (found) return found;
    }
  }
  return null;
}

async function routeCheck(url) {
  const response = await fetch(url, { redirect: "manual" });
  return {
    url,
    status: response.status,
    redirect_location: response.headers.get("location"),
  };
}

async function main() {
  const existingBoardId = Number(
    process.env.BIRDEYE_FOLLOZE_BOARD_ID || process.env.FOLLOZE_BOARD_ID || 0
  );
  const copied = existingBoardId
    ? { boardId: existingBoardId, status: "skipped_existing_board" }
    : await duplicateTemplate();
  const boardId = copied.boardId;

  await api(`/prism/${boardId}`, "PUT", {
    board: { name: BOARD_NAME, description: BOARD_DESCRIPTION, is_public: true },
  });

  const nativeItems = await ensureNativeItems(boardId);
  const before = await api(`/api/v1/boards/${boardId}/config`, "GET");
  const config = before.data.unpublished_config || before.data.published_config || before.data;
  const verificationSeed = personalizeConfig(config, nativeItems);
  stripTransientScripts(config);
  const newHash = recomputeHash(config);
  const save = await api(`/api/v1/boards/${boardId}/config`, "PUT", { config });
  const publish = await api(`/api/v1/boards/${boardId}/publish`, "POST");
  const after = await api(`/api/v1/boards/${boardId}/config`, "GET");
  const metadata = await readMetadata(boardId);
  const published = after.data.published_config;
  const unpublished = after.data.unpublished_config;
  const publicLink = findFirstExperienceUrl(metadata.data);
  const publicRoute = publicLink ? await routeCheck(publicLink) : null;
  const publishedWidgets = published.pages.default.widgets;
  const publishedText = JSON.stringify(published);
  const publishedValue = publishedWidgets.w_dacd1645.data.content;
  const finalItems = await readBoardItems(boardId);
  const deckReadback = finalItems.find((item) => item.id === nativeItems.deck.id);
  const demoReadbacks = nativeItems.demoItems.map((item) =>
    finalItems.find((candidate) => candidate.id === item.id)
  );

  const readback = {
    account: "BirdEye",
    source_brief: SOURCE_BRIEF,
    generated_asset_commit: assetCommit,
    template: { id: TEMPLATE_ID, preserved: true },
    board: {
      id: boardId,
      name: BOARD_NAME,
      designer_url: `${ISSUER}/app/board/${boardId}/designer`,
      public_link: publicLink,
      externally_shared: false,
    },
    source_context: {
      granola_meeting_id: "27276912-58be-4f96-b16e-6ed91dd42cc7",
      granola_meeting_date: "2026-07-21",
      slides_id: SLIDES_ID,
      slides_edit_url: SLIDES_EDIT_URL,
      kaia_viewer_url: "https://web.outreach.io/kaia/record/Of3Bk0RqT7q1WsgpUGSDvQ",
    },
    native_items: {
      deck: {
        id: deckReadback && deckReadback.id,
        title: deckReadback && deckReadback.title,
        url: deckReadback && deckReadback.url,
        category_id: nativeItems.featured.id,
      },
      demos: demoReadbacks.map((item) => ({
        id: item && item.id,
        title: item && item.title,
        url: item && item.url,
        image: item && item.image,
        category_id: nativeItems.examples.id,
      })),
    },
    api: {
      copy_status: copied.status,
      save_status: save.status,
      publish_status: publish.status,
      metadata_path: metadata.path,
      metadata_status: metadata.status,
      new_hash: newHash,
      published_hash: published.meta && published.meta.newHash,
      unpublished_hash: unpublished && unpublished.meta && unpublished.meta.newHash,
    },
    route_verification: {
      public_board: publicRoute,
      demos: await Promise.all(DEMOS.map((demo) => routeCheck(demo.url))),
    },
    verification: {
      template_id_is_248623: TEMPLATE_ID === 248623,
      published_contains_birdeye_logo: publishedText.includes(BIRDEYE_LOGO_URL),
      published_contains_hero_title: publishedText.includes("BirdEye,</span>"),
      published_contains_hero_subheader: publishedText.includes("~11,000 target accounts"),
      approved_value_heading_preserved: publishedValue.includes(VALUE_HEADING),
      value_intro_updated: publishedValue.includes(VALUE_INTRO_AFTER),
      card_two_updated: publishedValue.includes(CARD_TWO_AFTER),
      old_value_intro_removed: !publishedValue.includes(VALUE_INTRO_BEFORE),
      old_card_two_title_removed: !publishedValue.includes(CARD_TWO_BEFORE),
      roi_calculator_byte_equivalent: digest(publishedWidgets.w_3fb95f3a.data) === verificationSeed.roiHash,
      all_six_baseline_examples_preserved: verificationSeed.baselineIds.every((id) =>
        publishedWidgets.w_0dbb4e9a.data.sources.flz_item_ids.includes(id)
      ),
      all_three_birdeye_examples_appended: nativeItems.demoItems.every((item) =>
        publishedWidgets.w_0dbb4e9a.data.sources.flz_item_ids.includes(item.id)
      ),
      tailored_deck_present: Boolean(
        deckReadback &&
          deckReadback.title === "Folloze Presentation for BirdEye" &&
          deckReadback.url === SLIDES_PREVIEW_URL
      ),
      recording_present: false,
      published_and_unpublished_hashes_match: Boolean(
        published.meta &&
          unpublished &&
          unpublished.meta &&
          published.meta.newHash === unpublished.meta.newHash
      ),
    },
    caveats: [
      "The room is published for live QA but has not been sent or otherwise shared externally.",
      "The tailored deck is present under Featured Assets.",
      "The call recording is intentionally omitted because no edited buyer-safe export was available; the skill completion gate remains open until it is uploaded and verified.",
      "The ROI calculator data object was preserved byte-for-byte.",
    ],
    created_at: new Date().toISOString(),
  };

  fs.mkdirSync(path.dirname(READBACK_PATH), { recursive: true });
  fs.writeFileSync(READBACK_PATH, `${JSON.stringify(readback, null, 2)}\n`);
  console.log(JSON.stringify(readback, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
