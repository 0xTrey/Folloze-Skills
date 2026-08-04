#!/usr/bin/env node
"use strict";

/**
 * Account-neutral, config-driven Folloze DSR production orchestrator.
 *
 * Dry-run is the default and executes no adapters. Apply mode requires an exact
 * run-id confirmation; stages marked external_write require an additional
 * explicit flag. Adapter commands are argument arrays and never run in a shell.
 */

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const { performance } = require("perf_hooks");
const { spawn } = require("child_process");

const DEADLINES = Object.freeze({ target_seconds: 480, escalation_seconds: 540, hard_cap_seconds: 600 });
const WRITE_CAPABILITIES = new Set(["read_only", "local_write", "external_write"]);
const SECRET_KEY_PATTERN = /(token|secret|cookie|password|authorization|private[_-]?key)/i;

class OrchestratorError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "OrchestratorError";
    this.code = code;
  }
}

function stableStringify(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
    .join(",")}}`;
}

function fingerprint(value) {
  return crypto.createHash("sha256").update(stableStringify(value)).digest("hex");
}

function readJson(filePath, label) {
  const absolute = path.resolve(filePath);
  if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) {
    throw new OrchestratorError(`${label}_missing`, `${label} does not exist: ${absolute}`);
  }
  try {
    return { path: absolute, data: JSON.parse(fs.readFileSync(absolute, "utf8")) };
  } catch {
    throw new OrchestratorError(`${label}_invalid`, `${label} is not valid JSON.`);
  }
}

function validateSpec(raw) {
  if (!raw || typeof raw !== "object") throw new OrchestratorError("spec_invalid", "Run spec must be an object.");
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{2,80}$/.test(String(raw.run_id || ""))) {
    throw new OrchestratorError("run_id_invalid", "run_id must be 3-81 safe characters.");
  }
  if (!String(raw.account || "").trim()) throw new OrchestratorError("account_missing", "account is required.");
  if (!Array.isArray(raw.stages) || !raw.stages.length || raw.stages.length > 20) {
    throw new OrchestratorError("stages_invalid", "stages must contain 1-20 adapter stages.");
  }
  const seen = new Set();
  const stages = raw.stages.map((stage, index) => {
    if (!/^[a-z][a-z0-9_-]{1,48}$/.test(String(stage.id || ""))) {
      throw new OrchestratorError("stage_id_invalid", `Stage ${index + 1} has an invalid id.`);
    }
    if (seen.has(stage.id)) throw new OrchestratorError("stage_id_duplicate", `Duplicate stage id: ${stage.id}`);
    seen.add(stage.id);
    if (!Array.isArray(stage.command) || !stage.command.length || !stage.command.every((part) => typeof part === "string")) {
      throw new OrchestratorError("stage_command_invalid", `Stage ${stage.id} command must be a string array.`);
    }
    const timeoutSeconds = Number(stage.timeout_seconds);
    if (!Number.isFinite(timeoutSeconds) || timeoutSeconds <= 0 || timeoutSeconds > DEADLINES.hard_cap_seconds) {
      throw new OrchestratorError("stage_timeout_invalid", `Stage ${stage.id} timeout must be 1-600 seconds.`);
    }
    const capability = stage.write_capability || "read_only";
    if (!WRITE_CAPABILITIES.has(capability)) {
      throw new OrchestratorError("stage_capability_invalid", `Stage ${stage.id} has an invalid write_capability.`);
    }
    const dependencies = stage.depends_on || [];
    if (!Array.isArray(dependencies) || dependencies.some((dependency) => !seen.has(dependency))) {
      throw new OrchestratorError(
        "stage_dependency_invalid",
        `Stage ${stage.id} dependencies must reference earlier stages only.`
      );
    }
    const environment = stage.env || {};
    if (Object.keys(environment).some((key) => SECRET_KEY_PATTERN.test(key))) {
      throw new OrchestratorError(
        "secret_in_spec",
        `Stage ${stage.id} embeds a secret-like environment key; inherit credentials from the process environment instead.`
      );
    }
    if (Object.values(environment).some((value) => typeof value !== "string")) {
      throw new OrchestratorError("stage_env_invalid", `Stage ${stage.id} env values must be strings.`);
    }
    return {
      id: stage.id,
      command: stage.command,
      cwd: stage.cwd ? path.resolve(stage.cwd) : process.cwd(),
      env: environment,
      depends_on: dependencies,
      timeout_seconds: timeoutSeconds,
      write_capability: capability,
      retryable: stage.retryable === true,
      optional: stage.optional === true,
      required_output_marker: stage.required_output_marker || null,
      parallel_group: stage.parallel_group ? String(stage.parallel_group) : null,
      role: stage.role ? String(stage.role) : null,
    };
  });
  const groupCounts = new Map();
  for (const stage of stages) {
    if (!stage.parallel_group) continue;
    if (!/^[a-z][a-z0-9_-]{1,48}$/.test(stage.parallel_group)) {
      throw new OrchestratorError("parallel_group_invalid", `Stage ${stage.id} has an invalid parallel_group.`);
    }
    groupCounts.set(stage.parallel_group, (groupCounts.get(stage.parallel_group) || 0) + 1);
    if (stage.depends_on.some((dependency) => stages.find((candidate) => candidate.id === dependency)?.parallel_group === stage.parallel_group)) {
      throw new OrchestratorError("parallel_dependency_invalid", `Stage ${stage.id} depends on a member of its own parallel group.`);
    }
  }
  if (![...groupCounts.values()].some((count) => count >= 2)) {
    throw new OrchestratorError("parallel_group_required", "Production specs require at least one parallel group with two stages.");
  }
  const finalVerifiers = stages.filter((stage) => stage.role === "final_verifier");
  if (finalVerifiers.length !== 1) {
    throw new OrchestratorError("final_verifier_required", "Exactly one stage must have role=final_verifier.");
  }
  const finalVerifier = finalVerifiers[0];
  if (finalVerifier !== stages.at(-1) || finalVerifier.optional) {
    throw new OrchestratorError("final_verifier_order", "The required final verifier must be the last, non-optional stage.");
  }
  if (finalVerifier.required_output_marker !== "DSR_VERIFY_JSON_END") {
    throw new OrchestratorError(
      "final_verifier_marker",
      "The final verifier must require the compact DSR_VERIFY_JSON_END marker."
    );
  }
  const requiredPredecessors = stages.slice(0, -1).filter((stage) => !stage.optional).map((stage) => stage.id);
  if (requiredPredecessors.some((stageId) => !finalVerifier.depends_on.includes(stageId))) {
    throw new OrchestratorError(
      "final_verifier_dependencies",
      "The final verifier must depend on every preceding required stage."
    );
  }
  const usageTracking = raw.usage_tracking || {};
  return {
    schema_version: String(raw.schema_version || "1.0"),
    run_id: String(raw.run_id),
    account: String(raw.account).trim(),
    template_id: Number(raw.template_id || 248623),
    usage_tracking: {
      token_source: usageTracking.token_source ? String(usageTracking.token_source) : null,
      cost_source: usageTracking.cost_source ? String(usageTracking.cost_source) : null,
    },
    stages,
  };
}

function loadState(statePath, runId) {
  if (!statePath || !fs.existsSync(statePath)) return { schema_version: "1.0", run_id: runId, completed: {} };
  const state = JSON.parse(fs.readFileSync(statePath, "utf8"));
  if (state.run_id !== runId) throw new OrchestratorError("state_run_mismatch", "State file belongs to another run_id.");
  if (!state.completed || typeof state.completed !== "object") state.completed = {};
  return state;
}

function writeStateAtomic(statePath, state) {
  const absolute = path.resolve(statePath);
  fs.mkdirSync(path.dirname(absolute), { recursive: true });
  const temporary = `${absolute}.tmp-${process.pid}`;
  fs.writeFileSync(temporary, `${JSON.stringify(state)}\n`, { flag: "wx" });
  fs.renameSync(temporary, absolute);
}

function executableAvailable(command, cwd) {
  if (command.includes(path.sep)) {
    const resolved = path.resolve(cwd, command);
    try {
      fs.accessSync(resolved, fs.constants.X_OK);
      return true;
    } catch {
      return false;
    }
  }
  if (!/^[A-Za-z0-9._+-]+$/.test(command)) return false;
  for (const directory of String(process.env.PATH || "").split(path.delimiter)) {
    if (!directory) continue;
    try {
      fs.accessSync(path.join(directory, command), fs.constants.X_OK);
      return true;
    } catch {
      // Continue through PATH without invoking a shell.
    }
  }
  return false;
}

function sanitizedStage(stage) {
  return {
    id: stage.id,
    executable: stage.command[0],
    argument_count: stage.command.length - 1,
    cwd: stage.cwd,
    depends_on: stage.depends_on,
    timeout_seconds: stage.timeout_seconds,
    write_capability: stage.write_capability,
    retryable: stage.retryable,
    optional: stage.optional,
    parallel_group: stage.parallel_group,
    role: stage.role,
    fingerprint: fingerprint(stage),
  };
}

function runAdapter(stage, timeoutMs, inheritedEnv) {
  return new Promise((resolve) => {
    const startedAt = performance.now();
    const outputHash = crypto.createHash("sha256");
    let markerWindow = "";
    let spawnError = null;
    let timedOut = false;
    const child = spawn(stage.command[0], stage.command.slice(1), {
      cwd: stage.cwd,
      env: { ...inheritedEnv, ...stage.env },
      shell: false,
      stdio: ["ignore", "pipe", "pipe"],
    });
    const observe = (chunk) => {
      outputHash.update(chunk);
      if (stage.required_output_marker) {
        markerWindow = `${markerWindow}${chunk.toString("utf8")}`.slice(-4096);
      }
    };
    child.stdout.on("data", observe);
    child.stderr.on("data", observe);
    child.on("error", (error) => {
      spawnError = error;
    });
    const timer = setTimeout(() => {
      timedOut = true;
      child.kill("SIGKILL");
    }, Math.max(1, timeoutMs));
    child.on("close", (exitCode, signal) => {
      clearTimeout(timer);
      const markerPresent = !stage.required_output_marker || markerWindow.includes(stage.required_output_marker);
      const failureCode = timedOut
        ? "adapter_timeout"
        : spawnError
          ? "adapter_spawn_failed"
          : exitCode !== 0
            ? "adapter_failed"
            : !markerPresent
              ? "adapter_receipt_missing"
              : null;
      resolve({
        success: failureCode === null,
        exit_code: exitCode,
        signal: signal || null,
        elapsed_ms: Math.round(performance.now() - startedAt),
        failure_code: failureCode,
        output_sha256: outputHash.digest("hex"),
      });
    });
  });
}

async function runOrchestrator(spec, options = {}, runtime = {}) {
  const startedAt = performance.now();
  const mode = options.apply ? "apply" : "dry_run";
  const specHash = fingerprint(spec);
  const statePath = options.statePath ? path.resolve(options.statePath) : null;
  const stagePlan = spec.stages.map(sanitizedStage);
  const receipt = {
    schema_version: "1.0",
    run_id: spec.run_id,
    account: spec.account,
    template_id: spec.template_id,
    mode,
    deadlines: DEADLINES,
    spec_sha256: specHash,
    terminal_state: mode === "dry_run" ? "dry_run_validated" : "running",
    ready: false,
    stages: [],
    blockers: [],
    warnings: [],
    external_write_stages_executed: 0,
    usage_measurement: {
      tokens_available: Boolean(spec.usage_tracking.token_source),
      token_source: spec.usage_tracking.token_source,
      cost_available: Boolean(spec.usage_tracking.cost_source),
      cost_source: spec.usage_tracking.cost_source,
    },
    parallel_batches: [],
  };

  for (const stage of spec.stages) {
    if (!fs.existsSync(stage.cwd) || !fs.statSync(stage.cwd).isDirectory()) {
      receipt.blockers.push({ code: "stage_cwd_missing", stage: stage.id });
    } else if (!executableAvailable(stage.command[0], stage.cwd)) {
      receipt.blockers.push({ code: "stage_executable_missing", stage: stage.id, executable: stage.command[0] });
    }
  }
  if (mode === "dry_run") {
    receipt.stages = stagePlan.map((stage) => ({ ...stage, status: "planned_not_executed" }));
    receipt.ready = receipt.blockers.length === 0;
    receipt.terminal_state = receipt.ready ? "dry_run_validated" : "dry_run_blocked";
    receipt.elapsed_ms = Math.round(performance.now() - startedAt);
    return receipt;
  }

  if (options.confirmRunId !== spec.run_id) {
    throw new OrchestratorError("run_confirmation_missing", "Apply mode requires --confirm-run-id matching run_id.");
  }
  if (!statePath) throw new OrchestratorError("state_path_required", "Apply mode requires --state for idempotent resume.");
  if (spec.stages.some((stage) => stage.write_capability === "external_write") && !options.allowExternalWrites) {
    throw new OrchestratorError(
      "external_writes_not_authorized",
      "Run contains external_write stages; --allow-external-writes is required."
    );
  }
  if (receipt.blockers.length) {
    receipt.terminal_state = "apply_blocked";
    receipt.elapsed_ms = Math.round(performance.now() - startedAt);
    return receipt;
  }

  const state = loadState(statePath, spec.run_id);
  const pending = new Map(spec.stages.map((stage) => [stage.id, stage]));
  for (const stage of spec.stages) {
    const stageHash = fingerprint(stage);
    const prior = state.completed[stage.id];
    if (prior?.fingerprint === stageHash && prior.status === "passed") {
      receipt.stages.push({ id: stage.id, status: "resumed_completed", attempts: 0, fingerprint: stageHash });
      pending.delete(stage.id);
    }
  }

  const executeStage = async (stage) => {
    const stageHash = fingerprint(stage);
    const maxAttempts = stage.retryable ? 2 : 1;
    const attempts = [];
    let passed = false;
    for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
      const nowSeconds = (performance.now() - startedAt) / 1000;
      if (nowSeconds >= DEADLINES.escalation_seconds && attempt > 1) break;
      const hardRemainingMs = Math.max(1, DEADLINES.hard_cap_seconds * 1000 - (performance.now() - startedAt));
      const timeoutMs = Math.min(stage.timeout_seconds * 1000, hardRemainingMs);
      const result = await runAdapter(stage, timeoutMs, runtime.env || process.env);
      attempts.push({ attempt, ...result });
      if (result.success) {
        passed = true;
        break;
      }
    }
    return {
      id: stage.id,
      status: passed ? "passed" : "failed",
      attempts: attempts.length,
      retry_used: attempts.length > 1,
      fingerprint: stageHash,
      elapsed_ms: attempts.reduce((total, attempt) => total + attempt.elapsed_ms, 0),
      attempt_results: attempts,
    };
  };

  while (pending.size) {
    const elapsedSeconds = (performance.now() - startedAt) / 1000;
    if (elapsedSeconds >= DEADLINES.hard_cap_seconds) {
      receipt.blockers.push({ code: "hard_deadline_reached" });
      break;
    }
    if (elapsedSeconds >= DEADLINES.target_seconds && !receipt.warnings.some((item) => item.code === "target_exceeded")) {
      receipt.warnings.push({ code: "target_exceeded", elapsed_seconds: Math.round(elapsedSeconds) });
    }
    if (elapsedSeconds >= DEADLINES.escalation_seconds) {
      for (const stage of [...pending.values()].filter((candidate) => candidate.optional)) {
        receipt.stages.push({ id: stage.id, status: "skipped_at_escalation_deadline", attempts: 0 });
        pending.delete(stage.id);
      }
      if (!pending.size) break;
    }
    const ready = [...pending.values()].filter((stage) =>
      stage.depends_on.every((dependency) => state.completed[dependency]?.status === "passed")
    );
    if (!ready.length) {
      for (const stage of pending.values()) {
        receipt.stages.push({ id: stage.id, status: "blocked_by_dependency", attempts: 0, fingerprint: fingerprint(stage) });
      }
      receipt.blockers.push({ code: "dependency_failed" });
      break;
    }
    const first = ready[0];
    const batch = first.parallel_group
      ? ready.filter((stage) => stage.parallel_group === first.parallel_group)
      : [first];
    const batchStartedAt = performance.now();
    const batchResults = await Promise.all(batch.map(executeStage));
    receipt.parallel_batches.push({
      group: first.parallel_group || null,
      stage_ids: batch.map((stage) => stage.id),
      elapsed_ms: Math.round(performance.now() - batchStartedAt),
      ran_concurrently: batch.length > 1,
    });
    for (const result of batchResults) {
      receipt.stages.push(result);
      pending.delete(result.id);
      const stage = spec.stages.find((candidate) => candidate.id === result.id);
      if (result.status !== "passed") {
        if (stage.optional) receipt.warnings.push({ code: "optional_stage_failed", stage: stage.id });
        else receipt.blockers.push({ code: result.attempt_results.at(-1)?.failure_code || "adapter_failed", stage: stage.id });
        continue;
      }
      if (stage.write_capability === "external_write") receipt.external_write_stages_executed += 1;
      state.completed[stage.id] = {
        status: "passed",
        fingerprint: result.fingerprint,
        completed_at: new Date().toISOString(),
      };
    }
    state.spec_sha256 = specHash;
    writeStateAtomic(statePath, state);
    if (receipt.blockers.length) break;
  }

  receipt.elapsed_ms = Math.round(performance.now() - startedAt);
  receipt.deadline_status =
    receipt.elapsed_ms >= DEADLINES.hard_cap_seconds * 1000
      ? "hard_cap_exceeded"
      : receipt.elapsed_ms >= DEADLINES.escalation_seconds * 1000
        ? "escalated"
        : receipt.elapsed_ms >= DEADLINES.target_seconds * 1000
          ? "target_exceeded"
          : "within_target";
  receipt.ready =
    receipt.blockers.length === 0 &&
    spec.stages.filter((stage) => !stage.optional).every((stage) => state.completed[stage.id]?.status === "passed");
  receipt.terminal_state = receipt.ready ? "completed" : "nonterminal_blocked";
  return receipt;
}

function parseArgs(argv) {
  const options = {};
  const valueFlags = new Set(["spec", "state", "receipt", "confirm-run-id"]);
  for (let index = 0; index < argv.length; index += 1) {
    const raw = argv[index];
    if (!raw.startsWith("--")) throw new OrchestratorError("argument_invalid", `Unexpected argument: ${raw}`);
    const name = raw.slice(2);
    if (valueFlags.has(name)) {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new OrchestratorError("argument_value_missing", `${raw} requires a value.`);
      index += 1;
      options[name.replace(/-([a-z])/g, (_, character) => character.toUpperCase())] = value;
      continue;
    }
    if (name === "apply") options.apply = true;
    else if (name === "allow-external-writes") options.allowExternalWrites = true;
    else if (name === "help") options.help = true;
    else throw new OrchestratorError("argument_invalid", `Unknown option: ${raw}`);
  }
  return options;
}

function helpText() {
  return `Usage:
  fast_path_orchestrator.js --spec RUN.json

Default: validates the account-neutral adapter plan and executes nothing.

Apply/resume:
  --apply --confirm-run-id RUN_ID --state STATE.json
  --allow-external-writes   Required when any stage can write to Folloze/Drive/Sheet/Slack
  --receipt RECEIPT.json    Optional compact local receipt (apply mode only)

Deadlines: 480s target, 540s escalation/no retry, 600s hard process cap.`;
}

async function main(argv = process.argv.slice(2)) {
  try {
    const options = parseArgs(argv);
    if (options.help) {
      process.stdout.write(`${helpText()}\n`);
      return 0;
    }
    if (!options.spec) throw new OrchestratorError("spec_required", "--spec is required.");
    if (!options.apply && (options.state || options.receipt || options.confirmRunId || options.allowExternalWrites)) {
      throw new OrchestratorError("dry_run_write_option", "State, receipt, confirmation, and write flags are apply-only.");
    }
    const spec = validateSpec(readJson(options.spec, "spec").data);
    const receipt = await runOrchestrator(spec, {
      apply: options.apply,
      confirmRunId: options.confirmRunId,
      statePath: options.state,
      allowExternalWrites: options.allowExternalWrites,
    });
    const compact = `${JSON.stringify(receipt)}\n`;
    if (options.receipt) {
      const receiptPath = path.resolve(options.receipt);
      fs.mkdirSync(path.dirname(receiptPath), { recursive: true });
      fs.writeFileSync(receiptPath, compact, { flag: "wx" });
    }
    process.stdout.write(`DSR_RUN_JSON_BEGIN\n${compact}DSR_RUN_JSON_END\n`);
    return receipt.ready ? 0 : 2;
  } catch (error) {
    const receipt = {
      schema_version: "1.0",
      mode: "dry_run_or_apply_error",
      ready: false,
      terminal_state: "orchestrator_error",
      blockers: [{ code: error.code || "orchestrator_error", message: error.message }],
      external_write_stages_executed: 0,
    };
    process.stdout.write(`DSR_RUN_JSON_BEGIN\n${JSON.stringify(receipt)}\nDSR_RUN_JSON_END\n`);
    return 2;
  }
}

if (require.main === module) {
  main().then((exitCode) => {
    process.exitCode = exitCode;
  });
}

module.exports = { DEADLINES, OrchestratorError, runOrchestrator, validateSpec };
