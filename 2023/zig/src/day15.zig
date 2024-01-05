const Environment = @import("framework/Environment.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

const Answer = u64;
const Input = []const u8;

fn parseInput(input_arg: []const u8) !Input {
    var input = input_arg;
    if (text.splitLine(&input)) |line| {
        if (input.len == 0) return line;
    }
    return error.InvalidInput;
}

fn hash(s: []const u8) u8 {
    var h: u8 = 0;
    for (s) |c| {
        h +%= c;
        h *%= 17;
    }
    return h;
}

fn solvePart1(input: []const u8) Answer {
    var res: Answer = 0;
    var it = std.mem.splitScalar(u8, input, ',');
    while (it.next()) |word| res += hash(word);
    return res;
}

fn solvePart2(allocator: std.mem.Allocator, input: []const u8) !Answer {
    const M = std.StringArrayHashMap(Answer);
    var maps = [1]M{M.init(allocator)} ** 256;
    defer for (&maps) |*map| map.deinit();

    var it = std.mem.splitScalar(u8, input, ',');
    while (it.next()) |word| {
        std.debug.assert(word.len > 0);
        if (word[word.len - 1] == '-') {
            const key = word[0 .. word.len - 1];
            _ = maps[hash(key)].orderedRemove(key);
        } else if (std.mem.indexOfScalar(u8, word, '=')) |i| {
            const key = word[0..i];
            const value = try std.fmt.parseInt(Answer, word[i + 1 ..], 10);
            try maps[hash(key)].put(key, value);
        } else {
            return error.InvalidInput;
        }
    }
    var answer: Answer = 0;
    for (maps, 1..) |m, i| {
        for (m.values(), 1..) |v, j| {
            answer += i * j * v;
        }
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const line = try env.parseInput(Input, parseInput);
    try env.setAnswer1(solvePart1(line));
    try env.setAnswer2(try solvePart2(env.getHeapAllocator(), line));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        \\
    , "1320", "145");
}
