const Environment = @import("framework/Environment.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

const words = .{ "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };

fn findFirstDigit(s_in: []const u8, comptime allowWords: bool) !usize {
    var s = s_in;
    while (s.len > 0) : (s = s[1..]) {
        const first = s[0];
        if (first >= '1' and first <= '9') {
            return first - '0';
        }

        if (allowWords) {
            inline for (words, 1..) |word, i| {
                if (std.mem.startsWith(u8, s, word)) {
                    return i;
                }
            }
        }
    }
    return error.EndOfInput;
}

fn findLastDigit(s_in: []const u8, comptime allowWords: bool) !usize {
    var s = s_in;
    while (s.len > 0) : (s = s[0 .. s.len - 1]) {
        const last = s[s.len - 1];
        if (last >= '1' and last <= '9') {
            return last - '0';
        }
        if (allowWords) {
            inline for (words, 1..) |word, i| {
                if (std.mem.endsWith(u8, s, word)) {
                    return i;
                }
            }
        }
    }
    return error.EndOfInput;
}

fn solvePart(lines: []const []const u8, comptime part2: bool) !u64 {
    var answer: u64 = 0;
    for (lines) |line| {
        answer += 10 * try findFirstDigit(line, part2) + try findLastDigit(line, part2);
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const lines = try env.parseInputArena([]const []const u8, text.splitLinesAlloc);
    try env.setAnswer1(try solvePart(lines, false));
    try env.setAnswer2(try solvePart(lines, true));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example 1" {
    const lines = try text.splitLinesAlloc(std.testing.allocator,
        \\1abc2
        \\pqr3stu8vwx
        \\a1b2c3d4e5f
        \\treb7uchet
        \\
    );
    defer std.testing.allocator.free(lines);
    try std.testing.expectEqual(try solvePart(lines, false), 142);
}

test "example 2" {
    const lines = try text.splitLinesAlloc(std.testing.allocator,
        \\two1nine
        \\eightwothree
        \\abcone2threexyz
        \\xtwone3four
        \\4nineeightseven2
        \\zoneight234
        \\7pqrstsixteen
        \\
    );
    defer std.testing.allocator.free(lines);
    try std.testing.expectEqual(try solvePart(lines, true), 281);
}
