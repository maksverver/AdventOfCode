const Environment = @import("framework/Environment.zig");
const splitLines = @import("parsing/lines.zig").splitLines;
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
    const lines = try env.parseInputArena([]const []const u8, splitLines);
    try env.setAnswer1(try solvePart(lines, false));
    try env.setAnswer2(try solvePart(lines, true));
}
