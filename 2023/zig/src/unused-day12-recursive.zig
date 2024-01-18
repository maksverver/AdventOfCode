const Environment = @import("framework/Environment.zig");
const Scanner = @import("parsing/Scanner.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

const Answer = u64;

const MemoKey = struct {
    patLeft: usize,
    runsLeft: usize,
};

var memo: std.AutoHashMap(MemoKey, Answer) = undefined;

fn noneEqual(comptime T: type, slice: []const T, scalar: T) bool {
    for (slice) |item| {
        if (item == scalar) return false;
    }
    return true;
}

fn calc(pattern: []const u8, runs: []usize) !Answer {
    if (runs.len == 0) {
        return if (noneEqual(u8, pattern, '#')) 1 else 0;
    }
    const n = runs[0];
    if (pattern.len < n + 1) return 0;

    var res: Answer = 0;
    if (pattern[0] != '#') {
        res += try calcMemoized(pattern[1..], runs);
    }
    if (noneEqual(u8, pattern[0..n], '.') and pattern[n] != '#') {
        res += try calcMemoized(pattern[n + 1 ..], runs[1..]);
    }
    return res;
}

fn calcMemoized(pattern: []const u8, runs: []usize) error{OutOfMemory}!Answer {
    const key = MemoKey{ .patLeft = pattern.len, .runsLeft = runs.len };
    if (memo.get(key)) |val| return val;
    const val = try calc(pattern, runs);
    try memo.put(key, val);
    return val;
}

fn solveOneCase(pattern: []const u8, runs: []usize) !Answer {
    memo.clearRetainingCapacity();
    return try calc(pattern, runs);
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    memo = @TypeOf(memo).init(allocator);
    defer memo.deinit();
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

        answer1 += try solveOneCase(patternList.items, runsList.items);

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

        answer2 += try solveOneCase(patternList.items, runsList.items);
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
