///! Runs all the solvers on the official test data, and reports time taken.
///!
const std = @import("std");
const text = @import("parsing/text.zig");
const running = @import("framework/running.zig");
const nanosToMillis = running.nanosToMillis;
const Environment = @import("framework/Environment.zig");
const SolveFn = Environment.SolveFn;

const solvers = [_]?SolveFn{
    @import("day1.zig").solve,
    @import("day2.zig").solve,
    @import("day3.zig").solve,
    @import("day4.zig").solve,
    @import("day5.zig").solve,
    @import("day6.zig").solve,
    @import("day7.zig").solve,
    @import("day8.zig").solve,
    @import("day9.zig").solve,
    // TODO: days 10-25
    null, // null is allowed to skip days I haven't solved yet
};

// Silly logic to calculate default input and answer paths at compile time.
const defaultInputPathFmt = "../testdata/{d:0>2}.in";
const DefaultInputPathArgs = struct { usize };

const defaultAnswerPathFmt = "../testdata/{d:0>2}.ref";
const DefaultAnswerPathArgs = struct { usize };

var stdout = std.io.bufferedWriter(std.io.getStdOut().writer());
var stdoutWriter = stdout.writer();

inline fn defaultInputPath(comptime day: isize) *const [std.fmt.count(defaultInputPathFmt, DefaultInputPathArgs{@as(usize, day)}):0]u8 {
    comptime return std.fmt.comptimePrint(defaultInputPathFmt, DefaultInputPathArgs{@as(usize, day)});
}

inline fn defaultAnswerPath(comptime day: isize) *const [std.fmt.count(defaultAnswerPathFmt, DefaultAnswerPathArgs{@as(usize, day)}):0]u8 {
    comptime return std.fmt.comptimePrint(defaultAnswerPathFmt, DefaultAnswerPathArgs{@as(usize, day)});
}

fn parseAnswers(data: []const u8) !Environment.Answers {
    var result = Environment.Answers{};
    var remaining = data;
    if (text.splitLine(&remaining)) |part1| {
        result.part1 = part1;
        if (text.splitLine(&remaining)) |part2| {
            result.part2 = part2;
            if (remaining.len != 0) {
                return error.TooManyAnswers;
            }
        }
        return result;
    } else {
        return error.TooFewAnswers;
    }
}

fn compareAnswers(actual: ?[]const u8, expected: ?[]const u8) bool {
    if (actual) |a| {
        if (expected) |e| {
            // Both values are present. Verify contents are the same.
            return std.mem.eql(u8, a, e);
        }
    }
    // Verify both values are absent.
    return (actual == null) and (expected == null);
}

const tableHeader =
    \\╔═════╤════════╤════════╤═════════╤═════════╤═════════╤═════════╤═════════╗
    \\║ Day │ Part 1 │ Part 2 │Time (ms)│ Parsing │ Solve 1 │ Solve 2 │ Solving ║
    \\╟─────┼────────┼────────┼─────────┼─────────┼─────────┼─────────┼─────────╢
    \\
;

const tableFooter =
    \\╚═════╧════════╧════════╧═════════╧═════════╧═════════╧═════════╧═════════╝
    \\
;

fn printTime(opt_nanos: ?u64) !void {
    if (opt_nanos) |nanos| {
        try stdoutWriter.print("│{d: >8.3} ", .{nanosToMillis(nanos)});
    } else {
        try stdoutWriter.print("│{s: >8} ", .{"-"});
    }
}

fn solveDay(
    solve: SolveFn,
    input_path: []const u8,
    answer_path: []const u8,
) !bool {
    // Set up memory allocator, which detects leaks and other errors in debug mode.
    var general_purpose_allocator = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(general_purpose_allocator.deinit() == .ok);
    const allocator = general_purpose_allocator.allocator();

    // Read input file.
    const max_input_size = std.math.maxInt(usize);
    const inputData = std.fs.cwd().readFileAlloc(allocator, input_path, max_input_size) catch {
        // try stdoutWriter.print("Failed to read input from file: \"{s}\"\n", .{input_path});
        return false;
    };
    defer allocator.free(inputData);

    // Read answers file.
    const answerData = std.fs.cwd().readFileAlloc(allocator, answer_path, max_input_size) catch {
        // try stdoutWriter.print("Failed to read answers from file: \"{s}\"\n", .{answer_path});
        return false;
    };
    defer allocator.free(answerData);
    const expectedAnswers = try parseAnswers(answerData);

    const result = try Environment.run(allocator, inputData, solve);
    // Solver finished succesfully!
    defer result.deinit();
    const correct1 = compareAnswers(result.answers.part1, expectedAnswers.part1);
    const correct2 = compareAnswers(result.answers.part2, expectedAnswers.part2);

    try stdoutWriter.print("│ {s: <6} ", .{if (correct1) "OK" else "WRONG"});
    try stdoutWriter.print("│ {s: <6} ", .{if (correct2) "OK" else "WRONG"});

    try printTime(result.totalTime);
    try printTime(result.subTimes.parsing);
    try printTime(result.subTimes.solving1);
    try printTime(result.subTimes.solving2);
    try printTime(result.subTimes.solving);

    return correct1 and correct2;
}

const DayConfig = struct {
    day: usize,
    solve: ?SolveFn,
    input_path: []const u8,
    answer_path: []const u8,
};

const day_configs: []const DayConfig = getDayConfigs();

fn getDayConfig(day: usize) DayConfig {
    if (1 <= day and day <= day_configs.len) {
        return day_configs[day - 1];
    } else {
        return DayConfig{
            .day = day,
            .solve = null,
            .input_path = "",
            .answer_path = "",
        };
    }
}

fn getDayConfigs() []const DayConfig {
    comptime var res: []const DayConfig = &[0]DayConfig{};
    inline for (solvers, 1..) |solve, day| {
        const config = DayConfig{
            .day = day,
            .solve = solve,
            .input_path = defaultInputPath(day),
            .answer_path = defaultAnswerPath(day),
        };
        res = res ++ [1]DayConfig{config};
    }
    return res;
}

fn solveDays(configs: []const DayConfig) !void {
    var timer = try std.time.Timer.start();
    var failures: isize = 0;
    try stdoutWriter.writeAll(tableHeader);
    for (configs) |config| {
        try stdoutWriter.print("║{d: >4} ", .{config.day});
        if (config.solve) |solve| {
            if (solveDay(solve, config.input_path, config.answer_path)) |ok| {
                if (!ok) failures += 1;
                try stdoutWriter.writeAll("║\n");
            } else |err| {
                std.debug.print("Solver for day {} failed! {}\n", .{ config.day, err });
            }
        } else {
            try stdoutWriter.print("│ Missing solver for day {}\n", .{config.day});
        }
    }
    const totalNanos = timer.read();
    try stdoutWriter.writeAll(tableFooter);
    try stdout.flush();
    std.debug.print("Total time: {d:.3} ms\n", .{nanosToMillis(totalNanos)});
    if (failures > 0) {
        std.debug.print("{} solution(s) failed!\n", .{failures});
        std.process.exit(1);
    }
}

const usage = "Usage: aoc [<days>]\n\n";

pub fn main() !void {
    var general_purpose_allocator = std.heap.GeneralPurposeAllocator(.{}){};
    defer std.debug.assert(general_purpose_allocator.deinit() == .ok);
    const allocator = general_purpose_allocator.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);
    var config_list = std.ArrayList(DayConfig).init(allocator);
    defer config_list.deinit();
    for (args[1..]) |arg| {
        const day = std.fmt.parseInt(usize, arg, 10) catch {
            try stdoutWriter.print("Invalid argument: \"{s}\"\n\n", .{arg});
            try stdoutWriter.writeAll(usage);
            try stdout.flush();
            std.process.exit(1);
        };
        try config_list.append(getDayConfig(day));
    }

    const solve_configs = if (config_list.items.len > 0) config_list.items else day_configs;
    try solveDays(solve_configs);
}

test {
    // This causes tests in all packages this package depends on to run:
    std.testing.refAllDeclsRecursive(@This());

    // And also some stuff nothing depends on:
    std.testing.refAllDeclsRecursive(@import("day_example.zig"));
}