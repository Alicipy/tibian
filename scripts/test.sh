#!/usr/bin/env bash

# Run all tests

pytest \
    -p no:cacheprovider --cov="${1-src}" --cov-branch \
    --cov-report xml:reports/coverage.xml --cov-report term \
    --junitxml=junit-reports/test_results.xml
