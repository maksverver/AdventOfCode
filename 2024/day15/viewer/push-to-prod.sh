#!/bin/sh

set -e -E -o pipefail

rsync -av . styx:public_html/aoc-2024-day-15/ --delete
