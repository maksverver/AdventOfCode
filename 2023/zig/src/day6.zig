const Environment = @import("framework/Environment.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

// Type used for numbers in the input. Must be large enough to store the
// concatenation of input numbers! 64 bit is sufficient for the official input.
const Number = u64;

// Type used for answers. Must be at least as large as Number, but also large
// enough to hold the product of winning counts for part 1.
const Answer = u64;

// Parses the given line as a list of numbers.
fn parseNumbers(allocator: std.mem.Allocator, line: []const u8) ![]Number {
    const words = try text.splitWords(allocator, line);
    defer allocator.free(words);
    return try text.parseNumbers(Number, allocator, words);
}

/// Concatenates the given nonnegative numbers. For example, {1, 0, 23} => 1023.
fn Concatenate(numbers: []const Number) Number {
    var res: Number = 0;
    for (numbers) |n| {
        std.debug.assert(n >= 0);
        var multiplier: Number = 10;
        while (multiplier <= n) multiplier *= 10;
        res = multiplier * res + n;
    }
    return res;
}

const Input = struct {
    records: []Record,
    concatenatedRecord: Record,
    allocator: std.mem.Allocator,

    fn init(allocator: std.mem.Allocator, times: []const Number, dists: []const Number) !Input {
        if (times.len != dists.len) {
            @panic("times and dists must have the same length");
        }
        const records = try allocator.alloc(Record, times.len);
        errdefer allocator.free(records); // technically not necessary...
        for (0.., times, dists) |i, time, dist| {
            records[i] = Record{
                .time = time,
                .dist = dist,
            };
        }
        const concatated = Record{
            .time = Concatenate(times),
            .dist = Concatenate(dists),
        };
        return Input{
            .records = records,
            .concatenatedRecord = concatated,
            .allocator = allocator,
        };
    }

    fn deinit(self: *Input) void {
        self.allocator.free(self.records);
    }
};

fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Input {
    const lines = try text.splitLines(allocator, input);
    defer allocator.free(lines);
    if (lines.len != 2) return error.InvalidInput;
    const times = try parseNumbers(allocator, try text.removePrefix(lines[0], "Time:"));
    defer allocator.free(times);
    const dists = try parseNumbers(allocator, try text.removePrefix(lines[1], "Distance:"));
    defer allocator.free(dists);
    return Input.init(allocator, times, dists);
}

const Record = struct {
    time: Number,
    dist: Number,

    // Determines if holding for `hold` seconds beats the record, which is true
    // iff. (time - hold) * hold > dist.
    fn isWinning(record: *const Record, hold: Number) bool {
        return hold > 0 and (record.time - hold) > @divFloor(record.dist, hold);
    }

    // Binary search for the first value `hold` in range [lo..hi) such that
    // record.isWinning(hold) == target.
    fn findBoundary(record: *const Record, lo_arg: Number, hi_arg: Number, target: bool) Number {
        var lo = lo_arg;
        var hi = hi_arg;
        while (lo < hi) {
            var mid = lo + @divFloor((hi - lo), 2);
            if (record.isWinning(mid) == target) {
                hi = mid;
            } else {
                lo = mid + 1;
            }
        }
        return lo;
    }

    // Determines the number of values of `hold` for which record.isWinning(hold)
    // is true, using the fact that the optimal value to hold is time / 2, then
    // uses binary search to find the boundaries (which are actually symmetric,
    // but we don't use that here).
    fn countWinning(record: *const Record) Number {
        const bestHold = @divFloor(record.time, 2);
        if (!record.isWinning(bestHold)) return 0;

        const lo = record.findBoundary(0, bestHold, true);
        const hi = record.findBoundary(bestHold, record.time, false);

        // Verify we found the exact boundaries so that record.isWinning(hold)
        // is true iff. 0 < lo <= hold < hi < time:
        std.debug.assert(0 < lo and lo < hi and hi < record.time);
        std.debug.assert(!record.isWinning(lo - 1));
        std.debug.assert(record.isWinning(lo));
        std.debug.assert(record.isWinning(hi - 1));
        std.debug.assert(!record.isWinning(hi));

        return hi - lo;
    }
};

fn solvePart1(input: *const Input) Answer {
    var answer: Answer = 1;
    for (input.records) |record| {
        answer *= record.countWinning();
    }
    return answer;
}

fn solvePart2(input: *const Input) Answer {
    return input.concatenatedRecord.countWinning();
}

pub fn solve(env: *Environment) !void {
    var input = try env.parseInputHeap(Input, parseInput);
    defer input.deinit();
    try env.setAnswer1(solvePart1(&input));
    try env.setAnswer2(solvePart2(&input));
}

fn expectEqual(actual: anytype, expected: @TypeOf(actual)) !void {
    return std.testing.expectEqual(expected, actual);
}

test "Record.countWinning()" {
    const record1 = Record{ .time = 7, .dist = 9 };
    try expectEqual(record1.countWinning(), 4);

    const record2 = Record{ .time = 15, .dist = 40 };
    try expectEqual(record2.countWinning(), 8);

    const record3 = Record{ .time = 30, .dist = 200 };
    try expectEqual(record3.countWinning(), 9);

    const concatenated = Record{ .time = 7_15_30, .dist = 9_40_200 };
    try expectEqual(concatenated.countWinning(), 71503);
}

test "example" {
    try (@import("framework/testing.zig").testSolver(solve,
        \\Time:      7  15   30
        \\Distance:  9  40  200
        \\
    , "288", "71503"));
}
