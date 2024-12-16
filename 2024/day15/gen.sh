#!/bin/sh

pypy3 gen-long-walk.py 499 299 500000 > aoc-2024-day-15-challenge-1.txt
pypy3 gen-long-walk.py 1999 999 10000000 | pypy3 remove-loops.py > aoc-2024-day-15-challenge-2.txt
pypy3 gen-big-push.py 51 > aoc-2024-day-15-challenge-3.txt
pypy3 gen-big-push.py 501 > aoc-2024-day-15-challenge-4.txt
