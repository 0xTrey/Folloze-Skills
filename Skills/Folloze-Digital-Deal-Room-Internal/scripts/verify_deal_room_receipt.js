#!/usr/bin/env node
"use strict";

/** Validate one canonical adapter-produced deal-room receipt without live I/O. */

const fs = require("fs");
const path = require("path");

function requireCheck(failures, condition, code, field) {
  if (!condition) failures.push({ code, field });
}

function verify(receipt) {
  const failures = [];
  const warnings = [];
  const board = receipt.board || {};
  const template = receipt.template || {};
  const config = receipt.config || {};
  const essentials = receipt.essentials || {};
  const recording = essentials.recording || {};
  const deck = essentials.deck || {};
  const value = receipt.value_framework || {};
  const examples = receipt.examples || {};
  const roi = receipt.roi || {};
  const brand = receipt.brand || {};
  const editor = receipt.editor || {};
  const tracker = receipt.tracker || {};
  const slack = receipt.slack || {};
  const performance = receipt.performance || {};

  requireCheck(failures, Number.isInteger(Number(board.id)) && Number(board.id) > 0, "board_id_missing", "board.id");
  requireCheck(failures, board.is_template === false, "board_is_template", "board.is_template");
  requireCheck(failures, board.is_public === true, "board_not_public", "board.is_public");
  requireCheck(failures, board.online === true, "board_not_online", "board.online");
  requireCheck(failures, board.has_published_version === true, "board_not_published", "board.has_published_version");
  requireCheck(failures, /^https:\/\/app\.folloze\.com\//.test(board.designer_url || ""), "designer_url_invalid", "board.designer_url");
  requireCheck(
    failures,
    /^https:\/\/experience\.folloze\.com\//.test(board.public_url || board.public_link || ""),
    "public_url_invalid",
    "board.public_url"
  );
  requireCheck(failures, Boolean(board.slug), "vanity_slug_missing", "board.slug");
  requireCheck(failures, Number(template.id) === 248623 && template.is_template === true, "template_invalid", "template");
  requireCheck(failures, Boolean(config.saved_hash), "saved_hash_missing", "config.saved_hash");
  requireCheck(failures, Boolean(config.published_hash), "published_hash_missing", "config.published_hash");
  requireCheck(
    failures,
    config.hashes_match === true && config.saved_hash === config.published_hash,
    "config_hash_mismatch",
    "config.hashes_match"
  );
  requireCheck(
    failures,
    config.roi_byte_identical_to_template === true,
    "roi_changed",
    "config.roi_byte_identical_to_template"
  );
  requireCheck(failures, config.value_html_diff_allowlist_passed === true, "value_html_diff_failed", "config.value_html_diff_allowlist_passed");
  requireCheck(failures, Number(config.approved_html_widget_count) === 2, "embedded_widget_count_invalid", "config.approved_html_widget_count");
  requireCheck(failures, Number(config.new_html_widgets_added) === 0, "new_html_widget_added", "config.new_html_widgets_added");
  requireCheck(failures, config.raw_full_page_html_absent === true, "raw_html_payload_detected", "config.raw_full_page_html_absent");

  requireCheck(failures, recording.ready === true, "recording_not_ready", "essentials.recording.ready");
  requireCheck(failures, recording.buyer_title_verified === true, "recording_title_unverified", "essentials.recording.buyer_title_verified");
  requireCheck(failures, recording.correct_cover_verified === true, "recording_cover_unverified", "essentials.recording.correct_cover_verified");
  requireCheck(failures, recording.recording_clipped === true || recording.clip_required === false, "clip_unverified", "essentials.recording");
  requireCheck(
    failures,
    recording.folloze_playback === "passed" || recording.playback_verified === true,
    "recording_playback_unverified",
    "essentials.recording.folloze_playback"
  );
  requireCheck(failures, deck.ready === true, "deck_not_ready", "essentials.deck.ready");
  requireCheck(failures, deck.buyer_title_verified === true, "deck_title_unverified", "essentials.deck.buyer_title_verified");
  requireCheck(failures, deck.correct_cover_verified === true, "deck_cover_unverified", "essentials.deck.correct_cover_verified");
  requireCheck(
    failures,
    deck.working_destination === true || deck.destination_verified === true,
    "deck_destination_unverified",
    "essentials.deck.working_destination"
  );
  requireCheck(failures, value.private_language_removed === true, "private_value_language_detected", "value_framework.private_language_removed");
  requireCheck(failures, value.desktop_visual_qa === "passed", "value_desktop_qa_failed", "value_framework.desktop_visual_qa");
  requireCheck(failures, value.mobile_visual_qa === "passed", "value_mobile_qa_failed", "value_framework.mobile_visual_qa");

  requireCheck(failures, examples.baseline_items_preserved === true, "baseline_examples_changed", "examples.baseline_items_preserved");
  requireCheck(failures, examples.added_examples_verified === true, "added_examples_unverified", "examples.added_examples_verified");
  requireCheck(failures, roi.renders === true, "roi_render_failed", "roi.renders");
  requireCheck(failures, roi.calculates_at_original_defaults === true, "roi_behavior_changed", "roi.calculates_at_original_defaults");
  requireCheck(failures, brand.logo_verified === true, "brand_logo_unverified", "brand.logo_verified");
  requireCheck(failures, Boolean(brand.accent_source) && Boolean(brand.accent_hex), "brand_accent_unverified", "brand");
  requireCheck(failures, brand.accessible_contrast === true, "brand_contrast_failed", "brand.accessible_contrast");
  requireCheck(failures, brand.authenticated_visual_qa === "passed", "brand_visual_qa_failed", "brand.authenticated_visual_qa");

  const coreCards = Array.isArray(value.core_cards) ? value.core_cards : [];
  for (const required of ["build_speed_scalability", "personalization_enrichment", "analytics_optimization"]) {
    requireCheck(
      failures,
      coreCards.some((card) => card.id === required && card.evidence_verified === true && Boolean(card.buyer_text)),
      "value_card_unverified",
      `value_framework.core_cards.${required}`
    );
  }
  requireCheck(failures, typeof value.ai_signal_present === "boolean", "ai_signal_missing", "value_framework.ai_signal_present");
  requireCheck(
    failures,
    value.ai_signal_present === true
      ? value.card_4_mode === "openness_ai_connectivity"
      : value.card_4_mode === "operational_scale_reuse",
    "card_4_mode_invalid",
    "value_framework.card_4_mode"
  );

  if ((receipt.operator || "trey") === "luke" || editor.required === true) {
    requireCheck(
      failures,
      editor.verified === true && Boolean(editor.stable_identity) && editor.display_name === "Luke Rafferty",
      "editor_unverified",
      "editor"
    );
  }
  requireCheck(failures, tracker.verified === true && tracker.updated === true, "tracker_unverified", "tracker");
  requireCheck(failures, slack.sent === true, "slack_not_sent", "slack.sent");
  requireCheck(
    failures,
    slack.automated_codex_disclosure === true,
    "slack_disclosure_missing",
    "slack.automated_codex_disclosure"
  );
  requireCheck(failures, slack.customer_share_pending === true, "customer_share_state_missing", "slack.customer_share_pending");
  requireCheck(
    failures,
    typeof receipt.anonymous_visitor_gating === "string",
    "visitor_gating_unrecorded",
    "anonymous_visitor_gating"
  );
  requireCheck(
    failures,
    slack.designer_url_included === true && slack.public_url_included === true,
    "slack_urls_missing",
    "slack"
  );

  requireCheck(
    failures,
    Number.isFinite(Number(performance.elapsed_seconds)) && Number(performance.elapsed_seconds) <= 600,
    "performance_budget_failed",
    "performance.elapsed_seconds"
  );
  requireCheck(failures, Array.isArray(performance.stages) && performance.stages.length > 0, "stage_timings_missing", "performance.stages");
  requireCheck(
    failures,
    typeof performance.tokens?.available === "boolean",
    "token_availability_missing",
    "performance.tokens.available"
  );
  requireCheck(
    failures,
    typeof performance.cost?.available === "boolean",
    "cost_availability_missing",
    "performance.cost.available"
  );
  if (performance.tokens?.available === false) warnings.push({ code: "tokens_not_measured" });
  if (performance.cost?.available === false) warnings.push({ code: "cost_not_measured" });

  return {
    schema_version: "1.0",
    verified: failures.length === 0,
    terminal_state: failures.length === 0 ? "verified_complete" : "verification_blocked",
    board_id: Number(board.id) || null,
    elapsed_seconds: Number(performance.elapsed_seconds) || null,
    failures,
    warnings,
    live_writes_performed: 0,
  };
}

function main(argv = process.argv.slice(2)) {
  const index = argv.indexOf("--receipt");
  if (index < 0 || !argv[index + 1]) {
    process.stdout.write(
      `DSR_VERIFY_JSON_BEGIN\n${JSON.stringify({ verified: false, failures: [{ code: "receipt_required", field: "--receipt" }], live_writes_performed: 0 })}\nDSR_VERIFY_JSON_END\n`
    );
    return 2;
  }
  try {
    const receiptPath = path.resolve(argv[index + 1]);
    const receipt = JSON.parse(fs.readFileSync(receiptPath, "utf8"));
    const result = verify(receipt);
    process.stdout.write(`DSR_VERIFY_JSON_BEGIN\n${JSON.stringify(result)}\nDSR_VERIFY_JSON_END\n`);
    return result.verified ? 0 : 2;
  } catch {
    process.stdout.write(
      `DSR_VERIFY_JSON_BEGIN\n${JSON.stringify({ verified: false, failures: [{ code: "receipt_unreadable", field: "--receipt" }], live_writes_performed: 0 })}\nDSR_VERIFY_JSON_END\n`
    );
    return 2;
  }
}

if (require.main === module) process.exitCode = main();

module.exports = { verify };
