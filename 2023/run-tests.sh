#!/bin/bash

# Runs most tests, for reference files ending with .ref.
# This excludes the slow tests.
source test-lib.sh && run_tests "${TESTDIR}"/*.ref
