"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");

const { runPreflight } = require("./fast_path_preflight.js");

function writeTinyWav(destination) {
  const sampleRate = 8_000;
  const samples = sampleRate;
  const dataSize = samples * 2;
  const buffer = Buffer.alloc(44 + dataSize);
  buffer.write("RIFF", 0);
  buffer.writeUInt32LE(36 + dataSize, 4);
  buffer.write("WAVE", 8);
  buffer.write("fmt ", 12);
  buffer.writeUInt32LE(16, 16);
  buffer.writeUInt16LE(1, 20);
  buffer.writeUInt16LE(1, 22);
  buffer.writeUInt32LE(sampleRate, 24);
  buffer.writeUInt32LE(sampleRate * 2, 28);
  buffer.writeUInt16LE(2, 32);
  buffer.writeUInt16LE(16, 34);
  buffer.write("data", 36);
  buffer.writeUInt32LE(dataSize, 40);
  fs.writeFileSync(destination, buffer);
}

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "dsr-fast-preflight-"));
  const handoff = path.join(root, "handoff");
  fs.mkdirSync(handoff);
  fs.writeFileSync(path.join(handoff, "transcript.txt"), "00:00 Customer-ready transcript\n");
  writeTinyWav(path.join(handoff, "meeting.wav"));
  const deck = path.join(root, "presentation.pdf");
  fs.writeFileSync(deck, "%PDF-1.4\n% test-only fixture\n");
  return { root, handoff, deck };
}

test("complete Trey handoff passes without creating files or exposing token", async (context) => {
  const data = fixture();
  context.after(() => fs.rmSync(data.root, { recursive: true, force: true }));
  const before = fs.readdirSync(data.root, { recursive: true }).sort();
  const secret = "test-token-that-must-not-appear";
  const receipt = await runPreflight(
    {
      account: "Example Co",
      operator: "trey",
      package: data.handoff,
      deck: data.deck,
      meetingMatchConfirmed: true,
      noAccountExamples: true,
      budgetSeconds: 30,
    },
    { env: { FOLLOZE_ACCESS_TOKEN: secret, FOLLOZE_MCP_PROFILE: "engage" } }
  );
  const after = fs.readdirSync(data.root, { recursive: true }).sort();
  assert.equal(receipt.ready, true);
  assert.equal(receipt.terminal_state, "preflight_ready");
  assert.equal(receipt.media.probe, "passed");
  assert.equal(receipt.folloze_writes_performed, 0);
  assert.equal(receipt.external_writes_performed, 0);
  assert.deepEqual(after, before);
  assert.equal(JSON.stringify(receipt).includes(secret), false);
});

test("Luke handoff blocks unless editor transport is preflighted", async (context) => {
  const data = fixture();
  context.after(() => fs.rmSync(data.root, { recursive: true, force: true }));
  const receipt = await runPreflight(
    {
      account: "Example Co",
      operator: "luke",
      package: data.handoff,
      deck: data.deck,
      meetingMatchConfirmed: true,
      noAccountExamples: true,
      budgetSeconds: 30,
    },
    { env: { FOLLOZE_ACCESS_TOKEN: "redacted-test-token" } }
  );
  assert.equal(receipt.ready, false);
  assert(receipt.blockers.some((blocker) => blocker.code === "editor_transport_unverified"));
});

test("keyed Folloze template readback is accepted after auth warmup", async (context) => {
  const data = fixture();
  context.after(() => fs.rmSync(data.root, { recursive: true, force: true }));
  const receipt = await runPreflight(
    {
      account: "Example Co",
      operator: "luke",
      package: data.handoff,
      deck: data.deck,
      meetingMatchConfirmed: true,
      noAccountExamples: true,
      networkReadback: true,
      editorReady: true,
      budgetSeconds: 30,
    },
    {
      env: { FOLLOZE_ACCESS_TOKEN: "redacted-test-token", FOLLOZE_MCP_PROFILE: "engage" },
      fetch: async () => ({
        ok: true,
        json: async () => ({
          "248623": {
            id: 248623,
            name: "Folloze Resource Center / Digital Deal Room Template - July 2026 Folloze Resource Center",
            is_template: true,
          },
        }),
      }),
    }
  );
  assert.equal(receipt.ready, true);
  assert.equal(receipt.auth.template.remote_readback.verified, true);
  assert.equal(receipt.auth.template.remote_readback.template_id, 248623);
});

test("ambiguous transcripts fail closed", async (context) => {
  const data = fixture();
  context.after(() => fs.rmSync(data.root, { recursive: true, force: true }));
  fs.writeFileSync(path.join(data.handoff, "second-transcript.srt"), "1\n00:00:00,000 --> 00:00:01,000\nHi\n");
  const receipt = await runPreflight(
    {
      account: "Example Co",
      operator: "trey",
      package: data.handoff,
      deck: data.deck,
      meetingMatchConfirmed: true,
      noAccountExamples: true,
      budgetSeconds: 30,
    },
    { env: { FOLLOZE_ACCESS_TOKEN: "redacted-test-token" } }
  );
  assert.equal(receipt.ready, false);
  assert(receipt.blockers.some((blocker) => blocker.code === "transcript_ambiguous"));
});
