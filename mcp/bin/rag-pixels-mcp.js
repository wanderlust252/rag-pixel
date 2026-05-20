#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn, spawnSync } = require("child_process");

const PACKAGE_ROOT = path.resolve(__dirname, "..");
const VENV_DIR =
  process.env.RAG_PIXELS_MCP_VENV_DIR ||
  path.join(os.homedir(), ".cache", "rag-pixels-mcp", "venv");
const POSIX_VENV_PYTHON = path.join(VENV_DIR, "bin", "python");
const WINDOWS_VENV_PYTHON = path.join(VENV_DIR, "Scripts", "python.exe");
const MIN_PYTHON = [3, 11];
const PYTHON_CANDIDATES = [
  process.env.RAG_PIXELS_MCP_PYTHON,
  "python3.14",
  "python3.13",
  "python3.12",
  "python3.11",
  "python3",
  "python"
].filter(Boolean);

function isWindows() {
  return process.platform === "win32";
}

function venvPythonPath() {
  return isWindows() ? WINDOWS_VENV_PYTHON : POSIX_VENV_PYTHON;
}

function versionTuple(versionText) {
  const [major, minor] = versionText.trim().split(".").map(Number);
  return [major, minor];
}

function isCompatiblePython(versionText) {
  const [major, minor] = versionTuple(versionText);
  return (
    Number.isInteger(major) &&
    Number.isInteger(minor) &&
    (major > MIN_PYTHON[0] || (major === MIN_PYTHON[0] && minor >= MIN_PYTHON[1]))
  );
}

function runOrThrow(command, args, options = {}) {
  const result = spawnSync(command, args, {
    stdio: "inherit",
    ...options
  });

  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    throw new Error(`${command} exited with status ${result.status}`);
  }
}

function capture(command, args) {
  const result = spawnSync(command, args, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"]
  });

  if (result.error || result.status !== 0) {
    return null;
  }
  return result.stdout.trim();
}

function findPython() {
  for (const candidate of PYTHON_CANDIDATES) {
    const version = capture(candidate, [
      "-c",
      "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"
    ]);
    if (version && isCompatiblePython(version)) {
      return { command: candidate, version };
    }
  }
  return null;
}

function ensureVenv(basePython) {
  if (!fs.existsSync(venvPythonPath())) {
    runOrThrow(basePython, ["-m", "venv", VENV_DIR], {
      cwd: PACKAGE_ROOT
    });
  }
}

function ensureInstalled() {
  const marker = path.join(VENV_DIR, ".rag-pixels-mcp-version");
  const packageVersion = require(path.join(PACKAGE_ROOT, "package.json")).version;
  const currentMarker = fs.existsSync(marker) ? fs.readFileSync(marker, "utf8").trim() : "";

  if (currentMarker === packageVersion) {
    return;
  }

  runOrThrow(venvPythonPath(), ["-m", "pip", "install", "--upgrade", "pip"], {
    cwd: PACKAGE_ROOT
  });
  runOrThrow(
    venvPythonPath(),
    ["-m", "pip", "install", "--upgrade", PACKAGE_ROOT],
    { cwd: PACKAGE_ROOT }
  );
  fs.writeFileSync(marker, `${packageVersion}\n`);
}

function main() {
  const python = findPython();
  if (!python) {
    console.error(
      "rag-pixels-mcp requires Python 3.11+ on PATH. " +
        "Set RAG_PIXELS_MCP_PYTHON to a compatible interpreter if needed."
    );
    process.exit(1);
  }

  ensureVenv(python.command);
  ensureInstalled();

  const child = spawn(
    venvPythonPath(),
    ["-m", "rag_pixels_mcp.server"],
    {
      cwd: PACKAGE_ROOT,
      stdio: "inherit",
      env: process.env
    }
  );

  child.on("exit", (code, signal) => {
    if (signal) {
      process.kill(process.pid, signal);
      return;
    }
    process.exit(code ?? 0);
  });
}

main();
