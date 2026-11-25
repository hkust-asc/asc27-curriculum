#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../../.." && pwd)"
SITE_DIR="$ROOT_DIR/site"
STATE_DIR="${ASC27_VERIFY_STATE_DIR:-/tmp/asc27-verify-state}"
PORT="${ASC27_VERIFY_PORT:-0}"

mkdir -p "$STATE_DIR"
PID_FILE="$STATE_DIR/server.pid"
PORT_FILE="$STATE_DIR/server.port"
LOG_FILE="$STATE_DIR/server.log"

cmd="${1:-}"

case "$cmd" in
  start)
    if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
      echo "already running pid=$(cat "$PID_FILE") url=http://127.0.0.1:$(cat "$PORT_FILE")"
      exit 0
    fi
    if [[ "$PORT" == "0" ]]; then
      PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')"
    fi
    PID="$(python3 - "$PORT" "$SITE_DIR" "$LOG_FILE" <<'PY'
import subprocess, sys
port, site_dir, log_file = sys.argv[1], sys.argv[2], sys.argv[3]
with open(log_file, "ab", buffering=0) as log:
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", port, "--bind", "127.0.0.1", "--directory", site_dir],
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        close_fds=True,
    )
print(proc.pid)
PY
)"
    echo "$PID" > "$PID_FILE"
    echo "$PORT" > "$PORT_FILE"
    for _ in $(seq 1 30); do
      if curl -fsS "http://127.0.0.1:$PORT/index.html" >/dev/null 2>&1; then
        echo "started pid=$PID url=http://127.0.0.1:$PORT"
        exit 0
      fi
      sleep 0.1
    done
    kill "$PID" 2>/dev/null || true
    rm -f "$PID_FILE" "$PORT_FILE"
    echo "failed to start server; see $LOG_FILE" >&2
    exit 1
    ;;
  doctor)
    if [[ ! -f "$PID_FILE" || ! -f "$PORT_FILE" ]]; then
      echo "FAIL: no managed server state in $STATE_DIR" >&2
      exit 1
    fi
    PID="$(cat "$PID_FILE")"
    PORT="$(cat "$PORT_FILE")"
    if ! kill -0 "$PID" 2>/dev/null; then
      echo "FAIL: recorded pid $PID is not running" >&2
      exit 1
    fi
    HTTP_CODE="$(curl -sS -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/index.html")"
    if [[ "$HTTP_CODE" != "200" ]]; then
      echo "FAIL: http://127.0.0.1:$PORT/index.html returned $HTTP_CODE" >&2
      exit 1
    fi
    for page in index.html stage1-foundations.html stage2-parallelism.html stage3-ai-systems.html stage4-asc-sprint.html past-problems.html assets/common.js assets/style.css; do
      code="$(curl -sS -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/$page")"
      if [[ "$code" != "200" ]]; then
        echo "FAIL: /$page returned $code" >&2
        exit 1
      fi
    done
    echo "OK: pid=$PID url=http://127.0.0.1:$PORT pages=8/8 rev=$(git -C "$ROOT_DIR" rev-parse --short HEAD)"
    ;;
  stop)
    if [[ -f "$PID_FILE" ]]; then
      PID="$(cat "$PID_FILE")"
      if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        for _ in $(seq 1 20); do
          kill -0 "$PID" 2>/dev/null || break
          sleep 0.1
        done
      fi
    fi
    rm -rf "$STATE_DIR"
    echo "stopped and cleaned $STATE_DIR"
    ;;
  *)
    echo "usage: $0 {start|doctor|stop}" >&2
    exit 2
    ;;
esac
