#!/bin/bash
cd /home/kavia/workspace/code-generation/fitstream-tv-41026-41036/fitness_api_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

