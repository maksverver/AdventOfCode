const Environment = @import("framework/Environment.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

const MapEntry = struct {
    begin: isize,
    end: isize,
    delta: isize,

    fn compareBegin(_: void, a: MapEntry, b: MapEntry) bool {
        return a.begin < b.begin;
    }
};

// The input consists of a list of seeds, and a list of maps, where each map
// is a list of non-overlapping map entries, sorted by `begin`.
const Input = struct {
    seeds: []isize,
    maps: []const []const MapEntry,
    allocator: std.mem.Allocator,

    fn deinit(self: *const Input) void {
        for (self.maps) |map| self.allocator.free(map);
        self.allocator.free(self.maps);
        self.allocator.free(self.seeds);
    }
};

// Parses the input. The implementation is somewhat tricky due to memory
// management. (Using the arena allocator would be a lot simpler!)
fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Input {
    var it = try text.LineIterator.init(input);

    // Parse seeds line.
    const seedsLine = it.next() orelse return error.InvalidInput;
    const seedsText = text.removePrefix(seedsLine, "seeds:") orelse return error.InvalidInput;
    const seeds = try text.parseNumbersAlloc(isize, allocator, seedsText);
    errdefer allocator.free(seeds);

    // Skip blank separator line.
    const separate = it.next() orelse return error.InvalidInput;

    // Parse maps.
    std.debug.assert(separate.len == 0);
    var mapsList = std.ArrayList([]const MapEntry).init(allocator);
    errdefer mapsList.deinit();
    errdefer for (mapsList.items) |item| allocator.free(item);
    while (it.next()) |header| {
        // Each map starts with a header line (e.g. "seed-to-soil map:")
        std.debug.assert(std.mem.endsWith(u8, header, " map:"));

        // Parse map entries: three numbers per line
        var entries = std.ArrayList(MapEntry).init(allocator);
        errdefer entries.deinit();
        while (it.next()) |line| {
            if (line.len == 0) break;
            var nums: [3]isize = undefined;
            try text.parseNumbersSlice(isize, &nums, line);
            const dst = nums[0];
            const src = nums[1];
            const size = nums[2];
            try entries.append(MapEntry{
                .begin = src,
                .end = src + size,
                .delta = dst - src,
            });
        }

        // Sort entries (this is required by translateRangeToMin()).
        std.mem.sortUnstable(MapEntry, entries.items, {}, MapEntry.compareBegin);

        // Move the entries to the list of map. The order matters here, we must
        // call addOne() before toOwnedSlice() to avoid memory leaks!
        const p = try mapsList.addOne();
        p.* = try entries.toOwnedSlice();
    }
    return Input{
        .seeds = seeds,
        .maps = try mapsList.toOwnedSlice(),
        .allocator = allocator,
    };
}

fn translateSingleValue(maps: []const []const MapEntry, value: isize) isize {
    var result = value;
    for (maps) |entries| {
        for (entries) |entry| {
            if (entry.begin <= result and result < entry.end) {
                result += entry.delta;
                break;
            }
        }
    }
    return result;
}

fn solvePart1(input: *const Input) !i64 {
    var result: i64 = std.math.maxInt(i64);
    for (input.seeds) |seed| result = @min(result, translateSingleValue(input.maps, seed));
    return result;
}

// Translates the range of numbers between begin and end (exclusive) using the
// given maps, and returns the minimum of the final numbers.
fn translateRangeToMin(maps: []const []const MapEntry, begin: isize, end: isize) i64 {
    std.debug.assert(begin < end);
    if (maps.len == 0) return begin;
    var b = begin;
    var e = end;
    var result: i64 = std.math.maxInt(i64);
    for (maps[0]) |entry| {
        if (entry.end <= b) continue;
        if (entry.begin >= e) break;
        if (b < entry.begin) {
            result = @min(result, translateRangeToMin(maps[1..], b, entry.begin));
            b = entry.begin;
        }
        if (e <= entry.end) {
            return @min(result, translateRangeToMin(maps[1..], b + entry.delta, e + entry.delta));
        }
        result = @min(result, translateRangeToMin(maps[1..], b + entry.delta, entry.end + entry.delta));
        b = entry.end;
    }
    return @min(result, translateRangeToMin(maps[1..], b, e));
}

fn solvePart2(input: *const Input) !i64 {
    std.debug.assert(input.seeds.len % 2 == 0);
    var result: i64 = std.math.maxInt(i64);
    var i: usize = 0;
    while (i < input.seeds.len) : (i += 2) {
        const begin = input.seeds[i];
        const end = begin + input.seeds[i + 1];
        if (begin < end) {
            result = @min(result, translateRangeToMin(input.maps, begin, end));
        }
    }
    return result;
}

pub fn solve(env: *Environment) !void {
    const input = try env.parseInputHeap(Input, parseInput);
    defer input.deinit();

    try env.setAnswer1(try solvePart1(&input));
    try env.setAnswer2(try solvePart2(&input));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\seeds: 79 14 55 13
        \\
        \\seed-to-soil map:
        \\50 98 2
        \\52 50 48
        \\
        \\soil-to-fertilizer map:
        \\0 15 37
        \\37 52 2
        \\39 0 15
        \\
        \\fertilizer-to-water map:
        \\49 53 8
        \\0 11 42
        \\42 0 7
        \\57 7 4
        \\
        \\water-to-light map:
        \\88 18 7
        \\18 25 70
        \\
        \\light-to-temperature map:
        \\45 77 23
        \\81 45 19
        \\68 64 13
        \\
        \\temperature-to-humidity map:
        \\0 69 1
        \\1 0 69
        \\
        \\humidity-to-location map:
        \\60 56 37
        \\56 93 4
        \\
    , "35", "46");
}
