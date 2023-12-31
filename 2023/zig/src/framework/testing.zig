const Environment = @import("Environment.zig");
const std = @import("std");

/// Runs the solver on the given input, and verifies that the given answers match.
/// One of `answer1` or `answer2` may be omitted; in that case, the answer for
/// that part is not verified.
pub fn testSolver(
    solve: *const fn (*Environment) anyerror!void,
    input: []const u8,
    answer1: ?[]const u8,
    answer2: ?[]const u8,
) !void {
    try std.testing.expect(answer1 != null or answer2 != null);

    var env = try Environment.init(std.testing.allocator, input);
    defer env.deinit();
    try solve(&env);
    const received = env.getAnswers();
    if (answer1) |e| {
        if (received.part1) |r| {
            try std.testing.expectEqualStrings(e, r);
        } else {
            std.debug.print("Received no answer for part 1, expected: {s}\n", .{e});
            return error.TestFailure;
        }
    }
    if (answer2) |e| {
        if (received.part2) |r| {
            try std.testing.expectEqualStrings(e, r);
        } else {
            std.debug.print("Received no answer for part 2, expected: {s}\n", .{e});
            return error.TestFailure;
        }
    }
}
