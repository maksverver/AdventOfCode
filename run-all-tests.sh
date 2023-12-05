#!/bin/sh

# Runs tests from all subdirectories.
#
# Currently, the exit status doesn't reflect whether the tests passed or failed.

set -e -E -o pipefail

for dir in *
do
  if [ -d "$dir" ]; then
    cd "$dir"
    if [ -x run-all-tests.sh ]; then
      echo "Executing $dir/run-all-tests.sh"
      ./run-all-tests.sh
    elif [ -x run-tests.sh ]; then
      echo "Executing $dir/run-tests.sh"
      ./run-tests.sh
    else
      echo "Skipping directory $dir"
    fi
    cd ..
  fi
done
