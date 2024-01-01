///! Runs all the solvers on the official test data, and reports time taken.
///!
const std = @import("std");
const running = @import("framework/running.zig");
const Environment = @import("framework/Environment.zig");

const SolveFunction = *const fn (*Environment) anyerror!void;

// Silly logic to calculate default input paths at compile time.
const defaultInputPathFmt = "../testdata/{d:0>2}.in";
const DefaultInputPathArgs = struct { usize };

inline fn defaultInputPath(comptime day: isize) *const [std.fmt.count(defaultInputPathFmt, DefaultInputPathArgs{@as(usize, day)}):0]u8 {
    comptime return std.fmt.comptimePrint(defaultInputPathFmt, DefaultInputPathArgs{@as(usize, day)});
}

}

fn solveDay(input_path: []const u8, solveFunction: SolveFunction) !void {
    // Set up memory allocator, which detects leaks and other errors in debug mode.
    var general_purpose_allocator = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(general_purpose_allocator.deinit() == .ok);
    const allocator = general_purpose_allocator.allocator();

    // Read input file.
    const max_input_size = std.math.maxInt(usize);
    const input = try std.fs.cwd().readFileAlloc(allocator, input_path, max_input_size);
    // To read from stdin instead:
    // const input = try std.io.getStdIn().readToEndAlloc(allocator, max_input_size);
    defer allocator.free(input);

    var env = try Environment.init(allocator, input);
    defer env.deinit();
    try solveFunction(&env);
    const times = env.getTimes();
    const totalNanos = env.getTotalTime();

    // TODO: verify output!
    env.debugPrintAnswers();

    try running.writeTimes(std.io.getStdOut().writer(), times, totalNanos);
}

const DayConfig = struct { input: []const u8, solve: SolveFunction };

const solvers = [_]?SolveFunction{
    @import("day1.zig").solve,
    @import("day2.zig").solve,
    @import("day3.zig").solve,
    @import("day4.zig").solve,
    null, // TODO: day 5
    @import("day6.zig").solve,
    // TODO: days 7-25
    null, // null is allowed to skip days I haven't solved yet
};

pub fn main() !void {
    inline for (solvers, 1..) |opt_solve, day| {
        if (opt_solve) |solve| {
            const input_path = defaultInputPath(day);
            std.debug.print("Solving day {d} (input: {s})\n", .{ day, input_path });
            try solveDay(input_path, solve);
        } else {
            std.debug.print("Skipping day {d}\n", .{day});
        }
    }
}

test {
    // This causes tests in all packages this package depends on to run:
    std.testing.refAllDecls(@This());
}
