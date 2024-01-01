const Environment = @import("Environment.zig");
const std = @import("std");

/// Runs the solver on the given input, and verifies that the given answers match.
/// One of `answer1` or `answer2` may be omitted; in that case, the answer for
/// that part is not verified.
pub fn testSolver(
    solve: Environment.SolveFn,
    input: []const u8,
    answer1: ?[]const u8,
    answer2: ?[]const u8,
) !void {
    try std.testing.expect(answer1 != null or answer2 != null);

    const result = try Environment.run(std.testing.allocator, input, solve);
    defer result.deinit();
    if (answer1) |e| {
        if (result.answers.part1) |r| {
            try std.testing.expectEqualStrings(e, r);
        } else {
            std.debug.print("Received no answer for part 1, expected: {s}\n", .{e});
            return error.TestFailure;
        }
    }
    if (answer2) |e| {
        if (result.answers.part2) |r| {
            try std.testing.expectEqualStrings(e, r);
        } else {
            std.debug.print("Received no answer for part 2, expected: {s}\n", .{e});
            return error.TestFailure;
        }
    }
}
