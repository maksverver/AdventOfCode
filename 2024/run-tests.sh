#!/bin/bash

# Runs tests for reference files matchin *.ref.
#
# Can be invoked with an argument to only run tests matching a given prefix.
source test-lib.sh && run_tests "${TESTDIR}"/"$1"*.ref
