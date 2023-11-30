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
	received=$(${PYTHON} "${base}.py" <"$input")
	expected=$(cat "${TESTDIR}/$1")
	if [ "$expected" = "$received" ]; then
		echo "$1 passed"
	else
		echo "$1 FAILED: expected $expected, received $received"
	fi
}

run_tests() {
  for input in "$@"; do
    run_test "$(basename "$input")"
  done
}
