#!/bin/sh

export PYTHON=${PYTHON:-/usr/bin/python2}
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
	else
		echo "$1 FAILED: expected $expected, received $received"
	fi
}

for input in "${TESTDIR}"/*.ref; do
	run_test "$(basename "$input" .ref)"
done
