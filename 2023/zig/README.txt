Solutions to Advent of Code 2023 (https://adventofcode.com/2023/)
implemented in Zig (https://ziglang.org/).


## Requirements

These solutions require Zig to be installed. They were written for Zig 0.11.0.
To check which version of Zig is installed, run;

% zig version


## Running

To build and run all solutions on the official test data:

% zig build run                             (runs in debug mode)
% zig build run -Doptimize=ReleaseFast      (runs in with optimizations)

To run only some solutions, or the same solution multiple times (which is useful
for benchmarking):

% zig build run -Doptimize=ReleaseFast -- 7 7 7

The last-built executable is written to zig-out/bin/aoc, which can be run like this:

% time zig-out/bin/aoc


## Testing

To run all tests:

% zig build test

Or with slightly more information:

% zig build test --summary all


## Individual days

Individual days can be run with:

% zig run src/day1.zig < input.txt

And tested with:

% zig test src/day1.zig

Days can also be compiled into seperate executables which read from stdin and
write answers to stdout:

% zig build-exe -O ReleaseFast src/day1.zig
% time ./day1 < ../testdata/01.in
