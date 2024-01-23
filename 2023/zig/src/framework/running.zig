const Environment = @import("Environment.zig");
const builtin = @import("builtin");
const std = @import("std");

pub fn nanosToMillis(nanos: u64) f64 {
    return @as(f64, @floatFromInt(nanos)) / 1e6;
}

pub fn writeTimes(writer: anytype, totalNanos: u64, times: *const Environment.Times) !void {
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

/// Constructs an allocator depending on whether libc is linked.
pub const AllocatorFactory = union(enum) {
    c: void,
    gpa: std.heap.GeneralPurposeAllocator(.{}),

    pub fn init() AllocatorFactory {
        return if (builtin.link_libc) .{ .c = {} } else .{ .gpa = .{} };
    }

    pub fn deinit(self: *AllocatorFactory) void {
        return switch (self.*) {
            .c => {},
            .gpa => |*p| if (p.deinit() != .ok) @panic("Memory leaks detected!"),
        };
    }

    /// Returns raw_c_allocator if libc is linked in, or else the allocator
    /// for the GeneralPurposeAllocator.
    pub fn allocator(self: *AllocatorFactory) std.mem.Allocator {
        return if (builtin.link_libc) std.heap.raw_c_allocator else self.gpa.allocator();
    }
};

/// Runs the solver on input read from stdin, and writes the answers to stdout,
/// without verification. This is useful to run solutions individually while
/// testing, e.g. with `zig run src/day1.zig < input.txt`.
pub fn runSolutionStdIO(solve: *const fn (*Environment) anyerror!void) !void {
    var af = AllocatorFactory.init();
    defer af.deinit();
    const allocator = af.allocator();

    const max_input_size = std.math.maxInt(usize);
    const input = try std.io.getStdIn().readToEndAlloc(af.allocator(), max_input_size);
    defer allocator.free(input);

    const result = try Environment.run(allocator, input, solve);
    defer result.deinit();

    var bufferedStdout = std.io.bufferedWriter(std.io.getStdOut().writer());
    var bufferedStderr = std.io.bufferedWriter(std.io.getStdErr().writer());

    // Print answers.
    try bufferedStdout.writer().print("{[part1]?s}\n{[part2]?s}\n", result.answers);
    try bufferedStdout.flush();

    // Print solution times.
    try writeTimes(bufferedStderr.writer(), result.totalTime, &result.subTimes);
    try bufferedStderr.flush();
}
