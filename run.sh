#!/usr/bin/env bash
set -u

cd "$(dirname "$0")" || exit 2

pip install -q -r requirements.txt
install_rc=$?
if [ "$install_rc" -ne 0 ]; then
  echo "dependency installation failed"
  exit "$install_rc"
fi

python -m agent --selfcheck
check_rc=$?
if [ "$check_rc" -ne 0 ]; then
  echo "selfcheck failed"
  exit "$check_rc"
fi

python -m pytest -q
pytest_rc=$?
if [ "$pytest_rc" -gt 1 ]; then
  echo "pytest could not run"
  exit "$pytest_rc"
fi

if [ "$pytest_rc" -eq 1 ]; then
  echo "invariant tests are expected to fail until the task is completed"
fi

echo "ready"
exit 0
