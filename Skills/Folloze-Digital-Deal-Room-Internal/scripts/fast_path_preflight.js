#!/usr/bin/env node
"use strict";

/**
 * Read-only, bounded preflight for a native Folloze digital deal-room run.
 *
 * The helper intentionally performs no Folloze, Drive, Sheet, Slack, or local
 * writes by default. It validates the materialized handoff that those systems
 * produced and emits a compact receipt suitable for the production runner.
 */

const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { performance } = require("perf_hooks");
const { spawnSync } = require("child_process");

const SCHEMA_VERSION = "1.0";
const DEFAULT_BUDGET_SECONDS = 600;
const MAX_BUDGET_SECONDS = 600;
const DEFAULT_TEMPLATE_ID = 248623;
const TRANSCRIPT_EXTENSIONS = new Set([".txt", ".md", ".vtt", ".srt", ".pdf", ".docx"]);
const MEDIA_EXTENSIONS = new Set([".mp3", ".mp4", ".m4a", ".mov", ".wav"]);
const DECK_EXTENSIONS = new Set([".pdf", ".ppt", ".pptx"]);
const STAGE_TARGETS_MS = Object.freeze({
  dependencies: 5_000,
  inputs: 15_000,
  auth: 15_000,
  media: 20_000,
  examples: 10_000,
});
const PRODUCTION_SLO = Object.freeze({
  stretch_target_seconds: 300,
  normal_target_seconds: 480,
  hard_cap_seconds: 600,
  stage_caps_seconds: {
    preflight: 45,
    source_and_asset_resolution: 75,
    media_processing: 120,
    board_build_and_publish: 120,
    verification_and_handoff: 90,
  },
});

class PreflightError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "PreflightError";
    this.code = code;
  }
}

class BudgetClock {
  constructor(limitSeconds = DEFAULT_BUDGET_SECONDS) {
    if (!Number.isFinite(limitSeconds) || limitSeconds <= 0 || limitSeconds > MAX_BUDGET_SECONDS) {
      throw new PreflightError(
        "invalid_budget",
        `Budget must be greater than 0 and no more than ${MAX_BUDGET_SECONDS} seconds.`
      );
    }
    this.startedAt = performance.now();
    this.limitMs = Math.round(limitSeconds * 1000);
    this.stages = [];
  }

  elapsedMs() {
    return Math.round(performance.now() - this.startedAt);
  }

  remainingMs() {
    return Math.max(0, this.limitMs - this.elapsedMs());
  }

  assertRemaining(stageName) {
    if (this.remainingMs() <= 0) {
      throw new PreflightError("hard_budget_exceeded", `Hard time budget exhausted before ${stageName}.`);
    }
  }

  async stage(name, fn) {
    this.assertRemaining(name);
    const startedAt = performance.now();
    let status = "passed";
    try {
      return await fn(Math.min(this.remainingMs(), STAGE_TARGETS_MS[name] || this.remainingMs()));
    } catch (error) {
      status = "failed";
      throw error;
    } finally {
      const elapsedMs = Math.round(performance.now() - startedAt);
      this.stages.push({
        name,
        status,
        elapsed_ms: elapsedMs,
        target_ms: STAGE_TARGETS_MS[name] || null,
        within_stage_target: elapsedMs <= (STAGE_TARGETS_MS[name] || elapsedMs),
      });
    }
  }

  receipt() {
    const elapsedMs = this.elapsedMs();
    return {
      limit_seconds: this.limitMs / 1000,
      elapsed_ms: elapsedMs,
      remaining_ms: Math.max(0, this.limitMs - elapsedMs),
      within_hard_budget: elapsedMs <= this.limitMs,
    };
  }
}

function extension(fileName) {
  return path.extname(fileName).toLowerCase();
}

function sha256File(filePath) {
  const digest = crypto.createHash("sha256");
  const descriptor = fs.openSync(filePath, "r");
  const buffer = Buffer.allocUnsafe(1024 * 1024);
  try {
    let count;
    while ((count = fs.readSync(descriptor, buffer, 0, buffer.length, null)) > 0) {
      digest.update(buffer.subarray(0, count));
    }
  } finally {
    fs.closeSync(descriptor);
  }
  return digest.digest("hex");
}

function safeArchiveEntry(entry) {
  const normalized = entry.replaceAll("\\", "/");
  return Boolean(
    normalized &&
      !normalized.startsWith("/") &&
      !normalized.split("/").includes("..") &&
      !normalized.startsWith("__MACOSX/") &&
      !normalized.endsWith("/")
  );
}

function listDirectoryFiles(root, maximum = 2_000) {
  const files = [];
  const pending = [root];
  while (pending.length) {
    const current = pending.pop();
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      if (entry.name === ".DS_Store" || entry.name === "__MACOSX") continue;
      const absolute = path.join(current, entry.name);
      if (entry.isDirectory()) pending.push(absolute);
      if (entry.isFile()) {
        files.push({ name: path.relative(root, absolute), path: absolute, size: fs.statSync(absolute).size });
        if (files.length > maximum) {
          throw new PreflightError("package_too_large", `Package contains more than ${maximum} files.`);
        }
      }
    }
  }
  return files.sort((left, right) => left.name.localeCompare(right.name));
}

function listZipFiles(archivePath, timeoutMs) {
  const commandTimeoutMs = Math.max(1, Math.floor(timeoutMs / 2));
  const integrity = spawnSync("unzip", ["-tqq", archivePath], {
    encoding: "utf8",
    timeout: commandTimeoutMs,
    maxBuffer: 1024 * 1024,
  });
  if (integrity.error || integrity.status !== 0) {
    const detail = integrity.error?.message || integrity.stderr?.trim() || "ZIP integrity test failed";
    throw new PreflightError("zip_corrupt", `ZIP package failed its integrity test: ${detail}`);
  }
  const completed = spawnSync("unzip", ["-l", archivePath], {
    encoding: "utf8",
    timeout: commandTimeoutMs,
    maxBuffer: 8 * 1024 * 1024,
  });
  if (completed.error || completed.status !== 0) {
    const detail = completed.error?.message || completed.stderr?.trim() || "unknown unzip error";
    throw new PreflightError("zip_unreadable", `Unable to inspect ZIP package: ${detail}`);
  }
  const files = [];
  for (const line of completed.stdout.split(/\r?\n/)) {
    // Info-ZIP uses locale/build-dependent date order (MM-DD-YYYY on macOS,
    // YYYY-MM-DD on some Linux builds), so only rely on the stable columns.
    const match = line.match(/^\s*(\d+)\s+\S+\s+\S+\s+(.+?)\s*$/);
    if (!match) continue;
    const name = match[2];
    if (!safeArchiveEntry(name)) continue;
    files.push({ name, archive_path: name, size: Number(match[1]) });
  }
  if (!files.length) throw new PreflightError("zip_empty", "ZIP package contains no safe, readable files.");
  return files;
}

function selectSingle(files, allowedExtensions, typeName) {
  const matches = files.filter((file) => allowedExtensions.has(extension(file.name)) && file.size > 0);
  if (!matches.length) {
    throw new PreflightError(`${typeName}_missing`, `No non-empty supported ${typeName} was found.`);
  }
  if (matches.length > 1) {
    throw new PreflightError(
      `${typeName}_ambiguous`,
      `Multiple ${typeName} candidates were found: ${matches.map((file) => file.name).join(", ")}`
    );
  }
  return matches[0];
}

function inspectPackage(packagePath, timeoutMs) {
  const absolute = path.resolve(packagePath);
  if (!fs.existsSync(absolute)) throw new PreflightError("package_missing", `Package does not exist: ${absolute}`);
  const stat = fs.statSync(absolute);
  let kind;
  let files;
  if (stat.isDirectory()) {
    kind = "directory";
    files = listDirectoryFiles(absolute);
  } else if (stat.isFile() && extension(absolute) === ".zip") {
    kind = "zip";
    files = listZipFiles(absolute, timeoutMs);
  } else {
    throw new PreflightError("package_unsupported", "Package must be a directory or .zip archive.");
  }
  const transcript = selectSingle(files, TRANSCRIPT_EXTENSIONS, "transcript");
  const recording = selectSingle(files, MEDIA_EXTENSIONS, "recording");
  return {
    kind,
    path: absolute,
    file_count: files.length,
    transcript,
    recording,
  };
}

function inspectExplicitFile(filePath, allowedExtensions, typeName) {
  const absolute = path.resolve(filePath);
  if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) {
    throw new PreflightError(`${typeName}_missing`, `${typeName} does not exist: ${absolute}`);
  }
  const size = fs.statSync(absolute).size;
  if (!allowedExtensions.has(extension(absolute)) || size <= 0) {
    throw new PreflightError(`${typeName}_invalid`, `${typeName} is empty or has an unsupported extension.`);
  }
  return { name: path.basename(absolute), path: absolute, size };
}

function commandVersion(command, args = ["-version"]) {
  const completed = spawnSync(command, args, { encoding: "utf8", timeout: 3_000 });
  if (completed.error || completed.status !== 0) return { available: false, version: null };
  const output = `${completed.stdout || ""}\n${completed.stderr || ""}`.trim();
  return { available: true, version: output.split(/\r?\n/, 1)[0].slice(0, 160) };
}

function probeMedia(filePath, timeoutMs) {
  const completed = spawnSync(
    "ffprobe",
    [
      "-v",
      "error",
      "-show_entries",
      "format=duration:stream=codec_type,codec_name",
      "-of",
      "json",
      filePath,
    ],
    { encoding: "utf8", timeout: Math.max(1, timeoutMs), maxBuffer: 1024 * 1024 }
  );
  if (completed.error || completed.status !== 0) {
    const detail = completed.error?.message || completed.stderr?.trim() || "unknown ffprobe error";
    throw new PreflightError("recording_unreadable", `ffprobe could not read recording: ${detail}`);
  }
  const data = JSON.parse(completed.stdout);
  const duration = Number(data.format?.duration);
  const streams = (data.streams || []).map((stream) => ({
    type: stream.codec_type,
    codec: stream.codec_name,
  }));
  if (!Number.isFinite(duration) || duration <= 0 || !streams.some((stream) => stream.type === "audio")) {
    throw new PreflightError("recording_invalid", "Recording must have a readable duration and an audio stream.");
  }
  return { duration_seconds: Math.round(duration * 1000) / 1000, streams };
}

function probeZipMedia(archivePath, entryName, timeoutMs) {
  const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "dsr-media-probe-"));
  const temporaryMedia = path.join(temporaryDirectory, `recording${extension(entryName)}`);
  const descriptor = fs.openSync(temporaryMedia, "wx", 0o600);
  try {
    const extraction = spawnSync("unzip", ["-p", archivePath, entryName], {
      timeout: Math.max(1, Math.floor(timeoutMs / 2)),
      stdio: ["ignore", descriptor, "pipe"],
    });
    fs.closeSync(descriptor);
    if (extraction.error || extraction.status !== 0) {
      const detail = extraction.error?.message || extraction.stderr?.toString("utf8").trim() || "ZIP extraction failed";
      throw new PreflightError("zip_media_extract_failed", `Could not materialize the exact recording entry: ${detail}`);
    }
    if (fs.statSync(temporaryMedia).size <= 0) {
      throw new PreflightError("zip_media_empty", "Materialized ZIP recording is empty.");
    }
    return {
      probe: "passed",
      ...probeMedia(temporaryMedia, Math.max(1, Math.floor(timeoutMs / 2))),
      source: "bounded_temporary_zip_entry",
      temporary_media_cleaned: true,
    };
  } finally {
    try {
      fs.closeSync(descriptor);
    } catch {
      // The descriptor was already closed after extraction.
    }
    fs.rmSync(temporaryDirectory, { recursive: true, force: true });
  }
}

function tokenCacheDetails(env, issuer) {
  if (env.FOLLOZE_ACCESS_TOKEN) {
    return { source: "environment", profile: env.FOLLOZE_MCP_PROFILE || "engage", token: env.FOLLOZE_ACCESS_TOKEN };
  }
  const profile = env.FOLLOZE_MCP_PROFILE || "engage";
  const issuerKey = crypto.createHash("sha256").update(issuer).digest("hex").slice(0, 16);
  const candidates = [
    path.join(os.homedir(), ".folloze-mcp", "profiles", profile, "auth.json"),
    path.join(os.homedir(), ".folloze-mcp", "auth.json"),
  ];
  const authPath = candidates.find((candidate) => fs.existsSync(candidate));
  if (!authPath) throw new PreflightError("auth_cache_missing", `No Folloze auth cache found for profile ${profile}.`);
  let raw;
  try {
    raw = JSON.parse(fs.readFileSync(authPath, "utf8"));
  } catch {
    throw new PreflightError("auth_cache_unreadable", "Folloze auth cache is not valid JSON.");
  }
  const tokenSet = raw[issuerKey]?.tokens;
  if (!tokenSet?.access_token) throw new PreflightError("auth_token_missing", "Folloze access token is missing.");
  const expiresAt = Number(tokenSet.expires_at || 0);
  const expiresAtMs = expiresAt && expiresAt < 1_000_000_000_000 ? expiresAt * 1000 : expiresAt;
  if (expiresAtMs && expiresAtMs <= Date.now() + 60_000) {
    throw new PreflightError("auth_token_expired", "Folloze access token is expired or expires within 60 seconds.");
  }
  return { source: "cache", profile, auth_path: authPath, expires_at_ms: expiresAtMs || null, token: tokenSet.access_token };
}

async function readOnlyTemplateCheck({ issuer, templateId, token, timeoutMs, fetchImpl }) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), Math.max(1, timeoutMs));
  try {
    const response = await fetchImpl(`${issuer}/api/v1/boards/${templateId}`, {
      method: "GET",
      headers: { Authorization: `Bearer ${token}`, Accept: "application/json" },
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new PreflightError("auth_remote_failed", `Read-only template check returned HTTP ${response.status}.`);
    }
    const data = await response.json();
    if (Number(data.id) !== Number(templateId) || data.is_template !== true) {
      throw new PreflightError("template_identity_failed", `Board ${templateId} was not returned as a template.`);
    }
    return { verified: true, template_id: Number(data.id), is_template: true };
  } catch (error) {
    if (error.name === "AbortError") {
      throw new PreflightError("auth_remote_timeout", "Read-only Folloze auth/template check timed out.");
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

function inspectExamplesManifest(manifestPath) {
  const absolute = path.resolve(manifestPath);
  if (!fs.existsSync(absolute) || !fs.statSync(absolute).isFile()) {
    throw new PreflightError("examples_manifest_missing", `Examples manifest does not exist: ${absolute}`);
  }
  let raw;
  try {
    raw = JSON.parse(fs.readFileSync(absolute, "utf8"));
  } catch {
    throw new PreflightError("examples_manifest_invalid", "Examples manifest is not valid JSON.");
  }
  if (!Array.isArray(raw.examples) || !raw.examples.length) {
    throw new PreflightError("examples_missing", "Examples manifest must contain a non-empty examples array.");
  }
  const compactExamples = raw.examples.map((example, index) => {
    const boardId = Number(example.board_id);
    const deploymentUrl = String(example.deployment_url || "");
    const tileId = example.tile_file_id || example.tile?.file_id;
    if (!Number.isInteger(boardId) || boardId <= 0) {
      throw new PreflightError("example_board_id_missing", `Example ${index + 1} has no valid Board ID.`);
    }
    if (!deploymentUrl.startsWith("https://experience.folloze.com/")) {
      throw new PreflightError("example_url_invalid", `Example ${index + 1} has no production Folloze deployment URL.`);
    }
    if (!tileId) {
      throw new PreflightError("example_tile_missing", `Example ${index + 1} has no company-wide Drive tile file ID.`);
    }
    return { board_id: boardId, deployment_url: deploymentUrl, tile_file_id: String(tileId) };
  });
  return {
    path: absolute,
    tracker_verified: raw.tracker_verified === true,
    tile_library_verified: raw.tile_library_verified === true,
    examples: compactExamples,
  };
}

function compactPathFile(file, packageKind) {
  return {
    name: file.name,
    size_bytes: file.size,
    location: packageKind === "zip" ? "zip_entry" : "local_file",
  };
}

async function runPreflight(options, runtime = {}) {
  const env = runtime.env || process.env;
  const fetchImpl = runtime.fetch || globalThis.fetch;
  const clock = new BudgetClock(options.budgetSeconds || DEFAULT_BUDGET_SECONDS);
  const blockers = [];
  const warnings = [];
  const issuer = options.issuer || env.FOLLOZE_BASE_URL || "https://app.folloze.com";
  const templateId = Number(options.templateId || DEFAULT_TEMPLATE_ID);
  let dependencies;
  let inputs;
  let auth;
  let media;
  let examples;

  const capture = async (stageName, fn) => {
    try {
      return await clock.stage(stageName, fn);
    } catch (error) {
      blockers.push({ code: error.code || "preflight_error", message: error.message });
      return null;
    }
  };

  dependencies = await capture("dependencies", async () => {
    const ffmpeg = commandVersion("ffmpeg");
    const ffprobe = commandVersion("ffprobe");
    const unzip = commandVersion("unzip", ["-v"]);
    if (!ffmpeg.available) throw new PreflightError("ffmpeg_missing", "ffmpeg is required.");
    if (!ffprobe.available) throw new PreflightError("ffprobe_missing", "ffprobe is required.");
    if (options.package && extension(options.package) === ".zip" && !unzip.available) {
      throw new PreflightError("unzip_missing", "unzip is required for a ZIP package.");
    }
    return {
      node: process.version,
      ffmpeg: ffmpeg.version,
      ffprobe: ffprobe.version,
      unzip: unzip.available,
    };
  });

  inputs = await capture("inputs", async (stageTimeoutMs) => {
    if (!options.account) throw new PreflightError("account_missing", "--account is required.");
    if (!options.meetingMatchConfirmed) {
      throw new PreflightError("meeting_match_unconfirmed", "Explicit meeting/account match confirmation is required.");
    }
    let source;
    if (options.package) {
      source = inspectPackage(options.package, stageTimeoutMs);
    } else if (options.transcript && options.recording) {
      source = {
        kind: "explicit_files",
        transcript: inspectExplicitFile(options.transcript, TRANSCRIPT_EXTENSIONS, "transcript"),
        recording: inspectExplicitFile(options.recording, MEDIA_EXTENSIONS, "recording"),
      };
    } else {
      throw new PreflightError(
        "call_inputs_missing",
        "Supply --package or both --transcript and --recording; browser fallback is not a fast-path preflight."
      );
    }
    const deck = inspectExplicitFile(options.deck, DECK_EXTENSIONS, "deck");
    return {
      account: options.account,
      operator: options.operator || "trey",
      meeting_match_confirmed: true,
      package_kind: source.kind,
      package_path: source.path || null,
      transcript: compactPathFile(source.transcript, source.kind),
      recording: compactPathFile(source.recording, source.kind),
      deck: {
        name: deck.name,
        size_bytes: deck.size,
        sha256: sha256File(deck.path),
      },
      _recording_path: source.recording.path || null,
      _recording_archive_entry: source.recording.archive_path || null,
    };
  });

  auth = await capture("auth", async (stageTimeoutMs) => {
    if ((options.operator || "trey") === "luke" && !options.editorReady) {
      blockers.push({
        code: "editor_transport_unverified",
        message: "Luke's board-specific Editor invitation transport/session must be verified before production.",
      });
    }
    const tokenDetails = tokenCacheDetails(env, issuer);
    let remote = { verified: false, reason: "not_requested" };
    if (options.networkReadback) {
      remote = await readOnlyTemplateCheck({
        issuer,
        templateId,
        token: tokenDetails.token,
        timeoutMs: Math.min(stageTimeoutMs, 8_000),
        fetchImpl,
      });
    }
    return {
      source: tokenDetails.source,
      profile: tokenDetails.profile,
      expires_at_ms: tokenDetails.expires_at_ms || null,
      template: { id: templateId, remote_readback: remote },
      editor_transport_verified: Boolean(options.editorReady),
    };
  });

  media = await capture("media", async (stageTimeoutMs) => {
    if (!inputs) throw new PreflightError("inputs_not_ready", "Media validation requires valid call inputs.");
    if (!inputs._recording_path && inputs.package_kind === "zip" && inputs._recording_archive_entry) {
      return probeZipMedia(inputs.package_path, inputs._recording_archive_entry, stageTimeoutMs);
    }
    if (!inputs._recording_path) throw new PreflightError("recording_path_unresolved", "Recording path could not be resolved.");
    return { probe: "passed", ...probeMedia(inputs._recording_path, stageTimeoutMs) };
  });

  examples = await capture("examples", async () => {
    if (options.noAccountExamples) return { mode: "explicitly_skipped", count: 0 };
    if (!options.examplesManifest) {
      throw new PreflightError(
        "examples_manifest_required",
        "Provide --examples-manifest from the MCP tracker and company-wide Drive tile resolver, or use --no-account-examples."
      );
    }
    const manifest = inspectExamplesManifest(options.examplesManifest);
    if (!manifest.tracker_verified) {
      throw new PreflightError("tracker_unverified", "Examples manifest does not verify the canonical MCP tracker readback.");
    }
    if (!manifest.tile_library_verified) {
      throw new PreflightError("tile_library_unverified", "Examples manifest does not verify the company-wide tile library.");
    }
    return { count: manifest.examples.length, examples: manifest.examples };
  });

  if (inputs) {
    delete inputs._recording_path;
    delete inputs._recording_archive_entry;
  }
  const budget = clock.receipt();
  if (!budget.within_hard_budget) {
    blockers.push({ code: "hard_budget_exceeded", message: "Preflight exceeded the hard time budget." });
  }
  const ready = blockers.length === 0 && Boolean(dependencies && inputs && auth && media && examples);
  const allStagesWithinTarget = clock.stages.every((stage) => stage.within_stage_target);
  const runtimeProfile = !ready
    ? "blocked"
    : allStagesWithinTarget && media?.probe === "passed" && auth?.template?.remote_readback?.verified === true
      ? "fast_ready"
      : "standard_ready";
  return {
    schema_version: SCHEMA_VERSION,
    mode: "dry_run_read_only",
    ready,
    terminal_state: ready ? "preflight_ready" : "preflight_blocked",
    runtime_profile: runtimeProfile,
    account: options.account || null,
    template_id: templateId,
    production_slo: PRODUCTION_SLO,
    budget,
    stages: clock.stages,
    inputs,
    auth,
    media,
    examples,
    blockers,
    warnings,
    folloze_writes_performed: 0,
    external_writes_performed: 0,
  };
}

function parseArgs(argv) {
  const options = {};
  const valueFlags = new Set([
    "account",
    "operator",
    "package",
    "transcript",
    "recording",
    "deck",
    "examples-manifest",
    "issuer",
    "template-id",
    "budget-seconds",
    "write-receipt",
  ]);
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) throw new PreflightError("invalid_argument", `Unexpected argument: ${token}`);
    const name = token.slice(2);
    if (valueFlags.has(name)) {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) throw new PreflightError("missing_argument_value", `${token} requires a value.`);
      index += 1;
      const key = name.replace(/-([a-z])/g, (_, character) => character.toUpperCase());
      options[key] = value;
      continue;
    }
    const booleanFlags = {
      "meeting-match-confirmed": "meetingMatchConfirmed",
      "network-readback": "networkReadback",
      "editor-ready": "editorReady",
      "no-account-examples": "noAccountExamples",
      "allow-local-write": "allowLocalWrite",
      help: "help",
    };
    if (!booleanFlags[name]) throw new PreflightError("invalid_argument", `Unknown option: ${token}`);
    options[booleanFlags[name]] = true;
  }
  if (options.budgetSeconds !== undefined) options.budgetSeconds = Number(options.budgetSeconds);
  if (options.templateId !== undefined) options.templateId = Number(options.templateId);
  return options;
}

function helpText() {
  return `Usage:
  fast_path_preflight.js --account NAME --operator trey|luke \\
    --package CALL.zip --deck DECK.pdf --meeting-match-confirmed \\
    --examples-manifest EXAMPLES.json [--network-readback] [--editor-ready]

Alternative intake:
  --transcript FILE --recording FILE

Controls:
  --no-account-examples       Explicitly confirm no account examples are required
  --budget-seconds N          Hard budget; defaults to and cannot exceed 600 seconds
  --write-receipt FILE        Optional local receipt (requires --allow-local-write)
  --allow-local-write         Permit only the explicitly requested receipt write

Default behavior is dry-run/read-only and performs zero external writes.`;
}

async function main(argv = process.argv.slice(2)) {
  let options;
  try {
    options = parseArgs(argv);
    if (options.help) {
      process.stdout.write(`${helpText()}\n`);
      return 0;
    }
    if (options.writeReceipt && !options.allowLocalWrite) {
      throw new PreflightError(
        "local_write_not_authorized",
        "--write-receipt requires --allow-local-write; default dry-run performs no writes."
      );
    }
    const receipt = await runPreflight(options);
    const compact = `${JSON.stringify(receipt)}\n`;
    if (options.writeReceipt) {
      const receiptPath = path.resolve(options.writeReceipt);
      fs.mkdirSync(path.dirname(receiptPath), { recursive: true });
      fs.writeFileSync(receiptPath, compact, { flag: "wx" });
    }
    process.stdout.write(`DSR_PREFLIGHT_JSON_BEGIN\n${compact}DSR_PREFLIGHT_JSON_END\n`);
    return receipt.ready ? 0 : 2;
  } catch (error) {
    const failure = {
      schema_version: SCHEMA_VERSION,
      mode: "dry_run_read_only",
      ready: false,
      terminal_state: "preflight_error",
      runtime_profile: "blocked",
      blockers: [{ code: error.code || "preflight_error", message: error.message }],
      folloze_writes_performed: 0,
      external_writes_performed: 0,
    };
    process.stdout.write(`DSR_PREFLIGHT_JSON_BEGIN\n${JSON.stringify(failure)}\nDSR_PREFLIGHT_JSON_END\n`);
    return 2;
  }
}

if (require.main === module) {
  main().then((exitCode) => {
    process.exitCode = exitCode;
  });
}

module.exports = {
  BudgetClock,
  PreflightError,
  inspectExamplesManifest,
  inspectPackage,
  parseArgs,
  runPreflight,
};
