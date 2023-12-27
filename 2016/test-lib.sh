#!/bin/sh

export PYTHON=${PYTHON:-/usr/bin/python2}
export TESTDIR=${TESTDIR:-testdata}

run_test() {
  base=${1%.ref*}
  input=${TESTDIR}/${base}.in
  if [ ! -e "$input" ]; then
    input=${input%?.in}.in
  fi
  received=$(${PYTHON} "${base}.py" <"$input")
  expected=$(cat "${TESTDIR}/$1")
  if [ "$expected" = "$received" ]; then
    echo "$1 passed"
    return 0
  else
    echo "$1 FAILED: expected $expected, received $received"
    return 1
  fi
}

run_tests() {
  failed=0
  for input in "$@"; do
    run_test "$(basename "$input")" || failed=1
  done
  return $failed
}
