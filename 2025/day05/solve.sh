#!/bin/sh

sort -n $1 | grep . | (
    i=0
    ans1=0
    ans2=0
    while IFS=- read x y; do
        if [ "$y" ]; then
            test $i -lt $x && i=$x
            test $i -le $y && ans2=$((ans2 - i + (i=(y + 1))))
        else
            test $x -lt $i && ans1=$((ans1 + 1))
        fi
    done
    echo "Part 1: $ans1"
    echo "Part 2: $ans2"
)
