#!/bin/sh

export PYTHON=${PYTHON:-/usr/bin/python3}
export TESTDIR=${TESTDIR:-testdata}

run_test() {
  input=${TESTDIR}/$1.in
  if [ ! -e "$input" ]; then
    input=${TESTDIR}/${1%?}.in
  fi
  received=$(${PYTHON} "$1.py" <"$input")
  expected=$(cat "${TESTDIR}/$1.ref")
  if [ "$expected" = "$received" ]; then
    echo "$1 passed"
    return 0
  else
    echo "$1 FAILED: expected $expected, received $received"
    return 1
  fi
}

failed=0
for input in "${TESTDIR}"/*.ref; do
  run_test "$(basename "$input" .ref)" || failed=1
done
exit $failed
