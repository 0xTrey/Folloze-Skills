"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");
const { verify } = require("./verify_deal_room_receipt.js");

function validReceipt() {
  return {
    operator: "luke",
    board: {
      id: 249999,
      is_template: false,
      is_public: true,
      online: true,
      has_published_version: true,
      designer_url: "https://app.folloze.com/app/board/249999/designer",
      public_url: "https://experience.folloze.com/example-resource-center",
      slug: "example-resource-center",
    },
    template: { id: 248623, is_template: true },
    config: {
      saved_hash: "same",
      published_hash: "same",
      hashes_match: true,
      roi_byte_identical_to_template: true,
      value_html_diff_allowlist_passed: true,
      approved_html_widget_count: 2,
      new_html_widgets_added: 0,
      raw_full_page_html_absent: true,
    },
    essentials: {
      recording: {
        ready: true,
        recording_clipped: true,
        folloze_playback: "passed",
        buyer_title_verified: true,
        correct_cover_verified: true,
      },
      deck: { ready: true, working_destination: true, buyer_title_verified: true, correct_cover_verified: true },
    },
    value_framework: {
      core_cards: [
        { id: "build_speed_scalability", evidence_verified: true, buyer_text: "Speed" },
        { id: "personalization_enrichment", evidence_verified: true, buyer_text: "Personalization" },
        { id: "analytics_optimization", evidence_verified: true, buyer_text: "Analytics" },
      ],
      ai_signal_present: false,
      card_4_mode: "operational_scale_reuse",
      private_language_removed: true,
      desktop_visual_qa: "passed",
      mobile_visual_qa: "passed",
    },
    examples: { baseline_items_preserved: true, added_examples_verified: true },
    roi: { renders: true, calculates_at_original_defaults: true },
    brand: {
      logo_verified: true,
      accent_source: "https://example.com/brand",
      accent_hex: "#123456",
      accessible_contrast: true,
      authenticated_visual_qa: "passed",
    },
    editor: { required: true, verified: true, stable_identity: "invite-123", display_name: "Luke Rafferty" },
    tracker: { verified: true, updated: true },
    slack: {
      sent: true,
      automated_codex_disclosure: true,
      designer_url_included: true,
      public_url_included: true,
      customer_share_pending: true,
    },
    performance: {
      elapsed_seconds: 420,
      stages: [{ id: "build", elapsed_seconds: 100 }],
      tokens: { available: true },
      cost: { available: true },
    },
    anonymous_visitor_gating: "email_verification_required",
  };
}

test("complete canonical receipt passes", () => {
  const result = verify(validReceipt());
  assert.equal(result.verified, true);
  assert.equal(result.failures.length, 0);
});

test("publication and hard-budget failures block completion", () => {
  const receipt = validReceipt();
  receipt.board.online = false;
  receipt.performance.elapsed_seconds = 601;
  const result = verify(receipt);
  assert.equal(result.verified, false);
  assert(result.failures.some((failure) => failure.code === "board_not_online"));
  assert(result.failures.some((failure) => failure.code === "performance_budget_failed"));
});
