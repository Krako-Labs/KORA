#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if [[ "${KORA_STUDIO_BROWSER_KEYBOARD_SMOKE:-}" != "1" ]]; then
  echo "[browser-keyboard-smoke] skipped; set KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 to run the optional browser smoke"
  exit 0
fi

PORT="${KORA_STUDIO_BROWSER_KEYBOARD_PORT:-8765}"
BASE_URL="${KORA_STUDIO_BROWSER_KEYBOARD_BASE_URL:-http://127.0.0.1:${PORT}}"
TIMEOUT="${KORA_STUDIO_BROWSER_KEYBOARD_TIMEOUT:-20000}"
LOG_FILE="$(mktemp "${TMPDIR:-/tmp}/kora-studio-browser-keyboard.XXXXXX.log")"
SERVER_PID=""

cleanup() {
  if [[ -n "${SERVER_PID}" ]] && kill -0 "${SERVER_PID}" 2>/dev/null; then
    kill "${SERVER_PID}" 2>/dev/null || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
  rm -f "${LOG_FILE}"
}
trap cleanup EXIT

python3 -m kora studio --no-browser --port "${PORT}" >"${LOG_FILE}" 2>&1 &
SERVER_PID="$!"

python3 - "${BASE_URL}" "${SERVER_PID}" "${LOG_FILE}" <<'PY'
import sys
import time
import urllib.request

base_url, server_pid, log_file = sys.argv[1:4]
health_url = f"{base_url.rstrip('/')}/health"
deadline = time.monotonic() + 15
while time.monotonic() < deadline:
    try:
        with urllib.request.urlopen(health_url, timeout=1) as response:
            if response.status == 200:
                raise SystemExit(0)
    except Exception:
        pass
    time.sleep(0.25)

print(
    f"KORA Studio did not become ready at {health_url}; "
    f"server pid {server_pid}; log: {log_file}",
    file=sys.stderr,
)
raise SystemExit(1)
PY

python3 scripts/check_kora_studio_browser_keyboard.py --base-url "${BASE_URL}" --timeout "${TIMEOUT}"
