#!/bin/sh

# Runs tests from all subdirectories.
#
# Currently, the exit status doesn't reflect whether the tests passed or failed.

set -e -E -o pipefail

failed=0
processed=

TIMEFORMAT='Time taken: %U s (user) + %S s (system)'

for dir in *
do
  if [ -d "$dir" ]; then
    script=
    if [ -x "$dir"/run-all-tests.sh ]; then
      script=run-all-tests.sh
    elif [ -x "$dir"/run-tests.sh ]; then
      script=run-tests.sh
    fi
    if [ -z "$script" ]; then
      echo "Skipping directory $dir"
    else
      echo "Executing $dir/$script..."
      time (cd "$dir" && ./"$script") || failed=1
      processed="${processed} ${dir}"
    fi
  fi
done
echo "Directories processed:$processed"
if [ $failed = 0 ]; then
  echo "🎄 All tests passed! ☃️ "
else
  echo "Some tests failed :-("
fi
exit $failed
