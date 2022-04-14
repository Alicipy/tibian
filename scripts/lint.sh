#!/usr/bin/env bash

# Check style of the code.

set -eu

targets="src tests"

FIX=false

for i in "$@"; do
  case $i in
    --fix)
      FIX=true
      ;;
    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
    *)
      ;;
  esac
done

if [ "$FIX" = true ]; then
  echo "Fixing style..."
  for target in "${targets[@]}"; do
    isort $target
    black -q $target
  done
fi

isort --check $targets
black --check $targets
pflake8 $targets
mypy $targets
