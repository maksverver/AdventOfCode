Solutions to Advent of Code 2023 (https://adventofcode.com/2023/)
implemented in Zig (https://ziglang.org/).


To build and run:

% zig build run                             (runs in debug mode)
% zig build run -Doptimize=ReleaseFast      (runs in with optimizations)

The last-built executable is written to zig-out/bin/aoc, which can be run like this:

% time zig-out/bin/aoc

To run all tests:

% zig build test


Individual days can be run with:

% zig run src/day1.zig

Or with slightly more information:

% zig build test --summary all


To run tests for a single day:

% zig test src/day1.zig
