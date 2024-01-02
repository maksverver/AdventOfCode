//! A simple example of how to implement the solver for a day.
//!
//! This can be used as a template to implement subsequent days.
//!
//! In this example, the input is a single line of numbers separates by spaces.
//! Part 1 calculates the sum of the numbers.
//! Part 2 calculates the product of the numbers.

const Environment = @import("framework/Environment.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

const Input = []const i64;

fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Input {
    var remaining = input;
    const line = text.splitLine(&remaining) orelse return error.InvalidInput;
    std.debug.assert(remaining.len == 0);
    return text.parseNumbersAlloc(i64, allocator, line);
}

fn solvePart1(input: Input) !i64 {
    var res: i64 = 0;
    for (input) |i| res += i;
    return res;
}

fn solvePart2(input: Input) !i64 {
    var res: i64 = 1;
    for (input) |i| res *= i;
    return res;
}

pub fn solve(env: *Environment) !void {
    const numbers = try env.parseInputArena(Input, parseInput);
    try env.setAnswer1(try solvePart1(numbers));
    try env.setAnswer2(try solvePart2(numbers));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\3 1 4 1 5 9 2 6 5 3 5 8 9 7 9 3
        \\
    , "80", "6613488000");
}
