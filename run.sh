#!/usr/bin/env bash
# Run the backend (uses venv if present).
set -e
cd "$(dirname "$0")"
if [[ -d venv ]]; then
  exec ./venv/bin/python app.py "$@"
fi
# Fallback: hope python3 has packages (e.g. after pip install --user)
exec python3 app.py "$@"
