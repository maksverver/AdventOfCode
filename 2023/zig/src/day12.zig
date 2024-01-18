// This is an optimized bottom-up dynamic programming solution to day 12.
//
// For a version using recursion with memoization, see unused/day12.zig

const Environment = @import("framework/Environment.zig");
const Scanner = @import("util/Scanner.zig");
const text = @import("util/text.zig");
const std = @import("std");

const Answer = u64;

const Solver = struct {
    capacity: usize = 0,

    /// max_hashes[i] is the maximum number of trailing hashes of pattern[0..j]
    max_hashes: []usize = &[0]usize{},

    /// combis[i][j] is the number ways the pattern[0..j] can be filled to match
    /// runs[0..i]. To save memory, only the last two rows are stored.
    combis1: []Answer = &[0]Answer{},
    combis2: []Answer = &[0]Answer{},

    fn deinit(self: Solver, allocator: std.mem.Allocator) void {
        allocator.free(self.combis2);
        allocator.free(self.combis1);
        allocator.free(self.max_hashes);
    }

    fn solve(self: *Solver, allocator: std.mem.Allocator, pattern: []const u8, runs: []usize) !Answer {
        // Reserve space for pattern.len + 1 memo entries.
        if (self.capacity < pattern.len + 1) {
            self.capacity = @max(self.capacity, 16);
            while (self.capacity < pattern.len + 1) self.capacity *= 2;
            self.max_hashes = try allocator.realloc(self.max_hashes, self.capacity);
            self.combis1 = try allocator.realloc(self.combis1, self.capacity);
            self.combis2 = try allocator.realloc(self.combis2, self.capacity);
        }

        const max_hashes = self.max_hashes;
        var prev_row = self.combis1;
        var next_row = self.combis2;

        max_hashes[0] = 0;
        for (pattern, 0..) |ch, i| max_hashes[i + 1] = if (ch == '.') 0 else max_hashes[i] + 1;

        // First row: using no runs, we can fill any prefix that does not contain a
        // '#' in exactly 1 way: by setting all characters to '.'.
        const first_hash = std.mem.indexOfScalar(u8, pattern, '#') orelse pattern.len;
        @memset(prev_row[0 .. first_hash + 1], 1);
        @memset(prev_row[first_hash + 1 ..], 0);

        // Subsequent rows: if a prefix ends with '#', there is no solution.
        // Otherwise, we either keep the last '.' as filler, or match a run of
        // '#'s followed by a '.'.
        for (runs) |n| {
            next_row[0] = 0;
            for (pattern, 0..) |ch, j| {
                next_row[j + 1] = if (ch == '#') 0 else next_row[j] +
                    if (n <= max_hashes[j]) prev_row[j - n] else 0;
            }
            std.mem.swap([]Answer, &prev_row, &next_row);
        }
        return prev_row[pattern.len];
    }
};

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    var solver = Solver{};
    defer solver.deinit(allocator);
    var patternList = std.ArrayList(u8).init(allocator);
    defer patternList.deinit();
    var runsList = std.ArrayList(usize).init(allocator);
    defer runsList.deinit();
    var scanner = Scanner.init(env.getInput());
    var answer1: Answer = 0;
    var answer2: Answer = 0;
    while (!scanner.isEmpty()) {
        const patternString = try scanner.scanToken();
        scanner.skipHorizontalSpace();
        const runsString = try scanner.scanToken();
        try scanner.skipNewline();

        patternList.clearRetainingCapacity();
        try patternList.appendSlice(patternString);
        try patternList.append('.');

        runsList.clearRetainingCapacity();
        var it = std.mem.splitScalar(u8, runsString, ',');
        while (it.next()) |token| {
            try runsList.append(try std.fmt.parseInt(usize, token, 10));
        }

        answer1 += try solver.solve(allocator, patternList.items, runsList.items);

        // Set pattern to five copies of patternStrings separated by '?'.
        _ = patternList.pop();
        for (1..5) |_| {
            try patternList.append('?');
            try patternList.appendSlice(patternString);
        }
        try patternList.append('.');

        // Set runs to five copies of runs.
        const n = runsList.items.len;
        try runsList.resize(5 * n);
        for (n..5 * n) |i| runsList.items[i] = runsList.items[i - n];

        answer2 += try solver.solve(allocator, patternList.items, runsList.items);
    }
    try env.setAnswers(answer1, answer2);
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\???.### 1,1,3
        \\.??..??...?##. 1,1,3
        \\?#?#?#?#?#?#?#? 1,3,1,6
        \\????.#...#... 4,1,1
        \\????.######..#####. 1,6,5
        \\?###???????? 3,2,1
        \\
    , "21", "525152");
}
