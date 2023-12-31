//! Environment used by solvers to obtain resources like the heap allocator
//! (getAllocator()) and the input data (getInput()).
//!
//! A solver function receives an Environment pointer and should do two things:
//!
//!  1. Parse the input. Either by calling getInput() followed by parsingDone(),
//!     or using one of the convenience methods parseInput(), or
//!     parseInputArena().
//!
//!  2. Solve the problem, and report the answers either by calling setAnswer1()
//!     and setAnswer2(), or by calling only setAnswers() to report both answers
//!     in one step.
//!
//! The environment will take care of recording the total solution time, as well
//! as the time spent on parsing and solving the separate parts, if they are
//! reported separately.
//!

const std = @import("std");

const Environment = @This();

/// Answers to both parts, converted to strings.
pub const Answers = struct {
    part1: ?[]const u8 = null,
    part2: ?[]const u8 = null,
};

/// Times taken by the solver, in nanoseconds.
///
/// If `solving` is set, then `solving1` and `solving2` are unset.
pub const Times = struct {
    parsing: ?u64 = null,
    solving: ?u64 = null,
    solving1: ?u64 = null,
    solving2: ?u64 = null,

    /// Returns the total solving time, by summing the non-null fields.
    fn total(self: *const Times) u64 {
        return (self.parsing orelse 0) + (self.solving orelse ((self.solving1 orelse 0) + (self.solving2 orelse 0)));
    }
};

// Member fields. These should not be accessed directly even though Zig allows it.
_input: []const u8,
_allocator: std.mem.Allocator,
_arena: ?std.heap.ArenaAllocator = null,
_answers: Answers = .{},
_timer: std.time.Timer,
_times: Times = .{},

pub fn init(allocator: std.mem.Allocator, input: []const u8) !Environment {
    return Environment{
        ._allocator = allocator,
        ._input = input,
        ._timer = try std.time.Timer.start(),
    };
}

pub fn deinit(self: *Environment) void {
    if (self._arena) |a| a.deinit();
    if (self._answers.part1) |p| self._allocator.free(p);
    if (self._answers.part2) |p| self._allocator.free(p);
}

pub fn getHeapAllocator(self: *Environment) std.mem.Allocator {
    return self._allocator;
}

pub fn getArenaAllocator(self: *Environment) std.mem.Allocator {
    if (self._arena == null) {
        self._arena = std.heap.ArenaAllocator.init(self.getHeapAllocator());
    }
    return self._arena.?.allocator();
}

pub fn getInput(self: *Environment) []const u8 {
    return self._input;
}

pub fn getAnswers(self: *const Environment) *const Answers {
    return &self._answers;
}

pub fn getTimes(self: *Environment) *const Times {
    return &self._times;
}

/// Total time in nanoseconds, since calling init().
pub fn getTotalTime(self: *Environment) u64 {
    return self._times.total() + self._timer.read();
}

/// Solver calls this method to notify the environment that parsing is done,
/// which causes the parse time to be recorded.
///
/// Calling this is optional. If it is called, it should be called only once,
/// before reporting any answers.
pub fn parsingDone(self: *Environment) !void {
    if (self._times.parsing != null) @panic("parsing already done");
    self._times.parsing = self._timer.lap();
}

/// Convenience method that wraps getInput() and parsingDone(). This may be
/// called instead of parsingDone().
pub fn parseInput(self: *Environment, comptime T: type, parse: *const fn ([]const u8) anyerror!T) !T {
    const res = try parse(self.getInput());
    try self.parsingDone();
    return res;
}

/// Convenience method that wraps getInput(), getArenaAllocator() and
/// parsingDone(). This may be called instead of parsingDone().
pub fn parseInputArena(self: *Environment, comptime T: type, parse: *const fn (std.mem.Allocator, []const u8) anyerror!T) !T {
    const res = try parse(self.getArenaAllocator(), self._input);
    try self.parsingDone();
    return res;
}

fn storeAnswer(self: *Environment, answer: *?[]const u8, value: anytype) !void {
    if (answer.* != null) @panic("answer already set");
    var list = std.ArrayList(u8).init(self.getHeapAllocator());
    // FIXME: "{}"" only works for ints, not slices of strings etc.
    try std.fmt.format(list.writer(), "{}", .{value});
    answer.* = try list.toOwnedSlice();
}

/// Records the answer to part 1. This should be called only once.
pub fn setAnswer1(self: *Environment, value: anytype) !void {
    try self.storeAnswer(&self._answers.part1, value);
    self._times.solving1 = self._timer.lap();
}

/// Records the answer to part 2. This should be called only once.
pub fn setAnswer2(self: *Environment, value: anytype) !void {
    try self.storeAnswer(&self._answers.part2, value);
    self._times.solving2 = self._timer.lap();
}

/// Records the answers to part 1 and part 2. This may be called only once,
/// instead of calling setAnswer1() and setAnswer2() separately.
///
/// This method is meant for solvers that solve both parts together, so
/// recording solving times for part 1 and 2 separately does not make sense.
pub fn setAnswers(self: *Environment, value1: anytype, value2: anytype) !void {
    try self.storeAnswer(&self._answers.part1, value1);
    try self.storeAnswer(&self._answers.part2, value2);
    self._times.solving = self._timer.lap();
}

/// Prints the answers to stderr for debugging.
pub fn debugPrintAnswers(self: *const Environment) void {
    std.debug.print("{?s}\n{?s}\n", .{ self._answers.part1, self._answers.part2 });
}
