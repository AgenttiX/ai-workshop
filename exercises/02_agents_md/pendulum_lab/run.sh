#!/usr/bin/env bash
# Runs the analysis in the virtualenv of the workshop repository.
set -euo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "${SCRIPT_DIR}/../../../venv/bin/activate"
python "${SCRIPT_DIR}/analyse.py"
