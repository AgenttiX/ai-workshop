#!/usr/bin/env bash
# PostToolUse hook: lint an edited Python file with ruff and report the problems back to the agent.
# The tool call is given as JSON on stdin. See https://code.claude.com/docs/en/hooks
set -euo pipefail

FILE_PATH="$(python3 -c 'import json, sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))')"

# Only Python files are of interest.
if [[ "${FILE_PATH}" != *.py ]] || [[ ! -f "${FILE_PATH}" ]]; then
  exit 0
fi

# Prefer the ruff of the virtualenv of the workshop repository.
RUFF="ruff"
if [[ -n "${CLAUDE_PROJECT_DIR:-}" ]] && [[ -x "${CLAUDE_PROJECT_DIR}/venv/bin/ruff" ]]; then
  RUFF="${CLAUDE_PROJECT_DIR}/venv/bin/ruff"
fi

if ! OUTPUT="$("${RUFF}" check "${FILE_PATH}" 2>&1)"; then
  # Exit code 2 feeds stderr back to the agent so that it can fix the problems.
  echo "ruff found problems in ${FILE_PATH}:" >&2
  echo "${OUTPUT}" >&2
  exit 2
fi
exit 0
