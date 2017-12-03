#!/bin/bash

# Runs all tests, for reference files ending with .ref*.
source test-lib.sh && run_tests "${TESTDIR}"/*.ref*
