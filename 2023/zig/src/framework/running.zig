const Environment = @import("Environment.zig");
const std = @import("std");

fn nanosToMillis(nanos: u64) f64 {
    return @as(f64, @floatFromInt(nanos)) / 1e6;
}

pub fn writeTimes(writer: anytype, times: *const Environment.Times, totalNanos: u64) !void {
    // Report solution times
    try std.fmt.format(writer, "{d:.3} ms", .{nanosToMillis(totalNanos)});
    if (times.parsing) |ns| {
        try std.fmt.format(writer, " (parsing: {d:.3} ms)", .{nanosToMillis(ns)});
    }
    if (times.solving) |ns| {
        try std.fmt.format(writer, " (solving: {d:.3} ms)", .{nanosToMillis(ns)});
    } else {
        if (times.solving1) |ns| {
            try std.fmt.format(writer, " (part 1: {d:.3} ms)", .{nanosToMillis(ns)});
        }
        if (times.solving2) |ns| {
            try std.fmt.format(writer, " (part 2: {d:.3} ms)", .{nanosToMillis(ns)});
        }
    }
    try std.fmt.format(writer, "\n", .{});
}

/// Runs the solver on input read from stdin, and writes the answers to stdout,
/// without verification. This is useful to run solutions individually while
/// testing, e.g. with `zig run src/day1.zig < input.txt`.
pub fn runSolutionStdIO(solve: *const fn (*Environment) anyerror!void) !void {
    var general_purpose_allocator = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(general_purpose_allocator.deinit() == .ok);
    const allocator = general_purpose_allocator.allocator();

    const max_input_size = std.math.maxInt(usize);
    const input = try std.io.getStdIn().readToEndAlloc(allocator, max_input_size);
    defer allocator.free(input);

    var env = try Environment.init(allocator, input);
    defer env.deinit();
    try solve(&env);
    // Important to get the total time immediately after solving, even though
    // we only print the times later.
    const totalNanos = env.getTotalTime();
    const times = env.getTimes();

    var bufferedStdout = std.io.bufferedWriter(std.io.getStdOut().writer());
    var bufferedStderr = std.io.bufferedWriter(std.io.getStdErr().writer());

    // Print answers.
    const answers = env.getAnswers();
    try bufferedStdout.writer().print("{?s}\n{?s}\n", .{ answers.part1, answers.part2 });
    try bufferedStdout.flush();

    // Print solution times.
    try writeTimes(bufferedStderr.writer(), times, totalNanos);
    try bufferedStderr.flush();
}
