#!/bin/bash

# Runs all tests, for reference files ending with .ref*.
# This includes the slow tests.
source test-lib.sh && run_tests "${TESTDIR}"/*.ref*
