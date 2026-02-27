#!/usr/bin/env bash
# One-time setup: create venv and install dependencies.
#
# FIRST (once):  sudo apt install python3.12-venv
# THEN:           ./setup_venv.sh
# RUN BACKEND:    ./run.sh
set -e
cd "$(dirname "$0")"
if ! python3 -m venv venv; then
  echo ""
  echo "Venv failed. Install the venv package (one-time):"
  echo "  sudo apt install python3.12-venv"
  echo ""
  echo "Then run this script again: ./setup_venv.sh"
  exit 1
fi
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
echo "Setup done. Run the backend with: ./run.sh  (or: source venv/bin/activate && python app.py)"
