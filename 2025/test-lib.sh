#!/bin/sh

export PYTHON=${PYTHON:-/usr/bin/python}
export PYPY=${PYPY:-/usr/bin/pypy3}
export TESTDIR=${TESTDIR:-testdata}

if [ -x "$PYPY" ]; then
  # Use PyPy instead of Python if it's available.
  PYTHON=$PYPY
fi

run_test() {
  base=${1%.ref*}
  input=${TESTDIR}/${base}.in
  if [ ! -e "$input" ]; then
    input=${input%?.in}.in
  fi
  failed=0
  for solver in ${base}*.py; do
    id=${solver%.py}
    received=$(${PYTHON} "${solver}" <"$input")
    expected=$(cat "${TESTDIR}/$1")
    if [ "$expected" = "$received" ]; then
      echo "$id passed"
    else
      echo "$id FAILED: expected $expected, received $received"
      failed=1
    fi
  done
  return $failed
}

run_tests() {
  failed=0
  for input in "$@"; do
    run_test "$(basename "$input")" || failed=1
  done
  return $failed
}
