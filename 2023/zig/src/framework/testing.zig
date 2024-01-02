const Environment = @import("Environment.zig");
const std = @import("std");

fn verify(expected: ?[]const u8, received: ?[]const u8) bool {
    if (expected) |e| {
        if (received) |r| {
            return std.mem.eql(u8, e, r);
        } else {
            return false;
        }
    } else {
        return true;
    }
}

fn printVerdict(comptime part: usize, expected: ?[]const u8, received: ?[]const u8) void {
    if (expected) |e| {
        if (received) |r| {
            if (std.mem.eql(u8, e, r)) {
                std.debug.print("Part {} OK\n", .{part});
            } else {
                std.debug.print("Wrong answer for part {}!\n\tExpected: \"{s}\"\n\tReceived: \"{s}\"\n", .{ part, e, r });
            }
        } else {
            std.debug.print("No answer for part {}!\n\tExpected: \"{s}\"\n", .{ part, e });
        }
    }
}

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

    if (verify(answer1, result.answers.part1) and
        verify(answer2, result.answers.part2)) return;

    // Something was wrong! Print some details.
    printVerdict(1, answer1, result.answers.part1);
    printVerdict(2, answer2, result.answers.part2);
    return error.TestFailure;
}
