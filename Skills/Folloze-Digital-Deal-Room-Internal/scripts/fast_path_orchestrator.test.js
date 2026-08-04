"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");

const { runOrchestrator, validateSpec } = require("./fast_path_orchestrator.js");

function spec(command, overrides = {}) {
  return validateSpec({
    run_id: "test-run-001",
    account: "Example Co",
    usage_tracking: { token_source: "codex_goal_receipt", cost_source: "model_pricing_receipt" },
    stages: [
      {
        id: "preflight",
        command,
        timeout_seconds: 5,
        write_capability: "read_only",
        parallel_group: "intake",
        ...overrides,
      },
      {
        id: "assets",
        command: [process.execPath, "-e", "process.exit(0)"],
        timeout_seconds: 5,
        write_capability: "read_only",
        parallel_group: "intake",
      },
      {
        id: "final_verify",
        role: "final_verifier",
        command: [process.execPath, "-e", "console.log('DSR_VERIFY_JSON_END')"],
        timeout_seconds: 5,
        write_capability: "read_only",
        depends_on: ["preflight", "assets"],
        required_output_marker: "DSR_VERIFY_JSON_END",
      },
    ],
  });
}

test("dry-run validates but does not execute adapters", async (context) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "dsr-orchestrator-"));
  context.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const sentinel = path.join(root, "must-not-exist");
  const runSpec = spec([process.execPath, "-e", `require('fs').writeFileSync(${JSON.stringify(sentinel)}, 'bad')`]);
  const receipt = await runOrchestrator(runSpec);
  assert.equal(receipt.ready, true);
  assert.equal(receipt.mode, "dry_run");
  assert(receipt.stages.every((stage) => stage.status === "planned_not_executed"));
  assert.equal(receipt.usage_measurement.tokens_available, true);
  assert.equal(fs.existsSync(sentinel), false);
});

test("apply state makes a successful stage idempotently resumable", async (context) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "dsr-orchestrator-"));
  context.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const statePath = path.join(root, "state.json");
  const runSpec = spec([process.execPath, "-e", "process.exit(0)"]);
  const options = { apply: true, confirmRunId: runSpec.run_id, statePath };
  const first = await runOrchestrator(runSpec, options);
  const second = await runOrchestrator(runSpec, options);
  assert.equal(first.ready, true);
  assert.equal(first.stages[0].status, "passed");
  assert.equal(first.parallel_batches[0].ran_concurrently, true);
  assert.equal(second.ready, true);
  assert(second.stages.every((stage) => stage.status === "resumed_completed"));
});

test("retryable adapters receive no more than one retry", async (context) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "dsr-orchestrator-"));
  context.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const runSpec = spec([process.execPath, "-e", "process.exit(9)"], { retryable: true });
  const receipt = await runOrchestrator(runSpec, {
    apply: true,
    confirmRunId: runSpec.run_id,
    statePath: path.join(root, "state.json"),
  });
  assert.equal(receipt.ready, false);
  assert.equal(receipt.stages[0].attempts, 2);
  assert.equal(receipt.stages[0].retry_used, true);
});
