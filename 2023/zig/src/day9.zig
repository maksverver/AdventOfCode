const Environment = @import("framework/Environment.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

fn extrapolate(data: []i64) i64 {
    if (std.mem.allEqual(i64, data, 0)) return 0;
    const n = data.len - 1;
    for (0..n) |i| data[i] = data[i + 1] - data[i];
    return data[n] + extrapolate(data[0..n]);
}

pub fn solve(env: *Environment) !void {
    var numbers1 = std.ArrayList(i64).init(env.getHeapAllocator());
    var numbers2 = std.ArrayList(i64).init(env.getHeapAllocator());
    defer numbers1.deinit();
    defer numbers2.deinit();
    var answer1: i64 = 0;
    var answer2: i64 = 0;
    var line_it = try text.LineIterator.init(env.getInput());
    while (line_it.next()) |line| {
        // Parse line of numbers into numbers1
        numbers1.clearRetainingCapacity();
        try text.parseNumbersToList(i64, &numbers1, line);

        // Assign the reverse of numbers1 to numbers2 (we can't reverse
        // in-place because extrapolate() modifies the data during execution).
        const n = numbers1.items.len;
        try numbers2.resize(n);
        for (0..n) |i| numbers2.items[i] = numbers1.items[n - 1 - i];

        answer1 += extrapolate(numbers1.items);
        answer2 += extrapolate(numbers2.items);
    }
    try env.setAnswers(answer1, answer2);
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\0 3 6 9 12 15
        \\1 3 6 10 15 21
        \\10 13 16 21 30 45
        \\
    , "114", "2");
}
