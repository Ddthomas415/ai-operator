#!/usr/bin/env bash
set -euo pipefail

python3 -m pytest -q
python3 -m evals.run_all
