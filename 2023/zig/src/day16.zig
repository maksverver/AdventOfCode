//! A simple example of how to implement the solver for a day.
//!
//! This can be used as a template to implement subsequent days.
//!
//! In this example, the input is a single line of numbers separates by spaces.
//! Part 1 calculates the sum of the numbers.
//! Part 2 calculates the product of the numbers.

const Environment = @import("framework/Environment.zig");
const Grid = @import("parsing/Grid.zig");
const std = @import("std");

const Dir = enum { n, e, s, w };

const State = struct {
    r: isize,
    c: isize,
    dir: Dir,

    pub fn step(state: State, dir: Dir) State {
        return switch (dir) {
            .n => .{ .r = state.r - 1, .c = state.c, .dir = .n },
            .e => .{ .r = state.r, .c = state.c + 1, .dir = .e },
            .s => .{ .r = state.r + 1, .c = state.c, .dir = .s },
            .w => .{ .r = state.r, .c = state.c - 1, .dir = .w },
        };
    }
};

const Solver = struct {
    grid: Grid,
    allocator: std.mem.Allocator,

    // Slice of size height × width, indicating which tiles are illuminated.
    _illuminated: []bool,

    // _todo and _seen are used to implement a breadth-first search in solve()).
    // _seen is a slice of size height × width × 4 that tracks whether a state
    // is already in todo, and todo contains the reachable states.
    _seen: []bool,
    _todo: std.ArrayList(State),

    fn init(allocator: std.mem.Allocator, grid: Grid) !Solver {
        var illuminated = try allocator.alloc(bool, grid.height * grid.width);
        errdefer allocator.free(illuminated);
        @memset(illuminated, false);
        var seen = try allocator.alloc(bool, grid.height * grid.width * 4);
        errdefer allocator.free(seen);
        @memset(seen, false);
        var todo = std.ArrayList(State).init(allocator);
        errdefer todo.deinit();
        return Solver{ .grid = grid, ._illuminated = illuminated, ._todo = todo, ._seen = seen, .allocator = allocator };
    }

    fn deinit(self: Solver) void {
        self._todo.deinit();
        self.allocator.free(self._seen);
        self.allocator.free(self._illuminated);
    }

    pub fn _getIlluminated(self: *Solver, state: State) *bool {
        const r = @as(usize, @intCast(state.r));
        const c = @as(usize, @intCast(state.c));
        return &self._illuminated[r * self.grid.width + c];
    }

    pub fn _getSeen(self: *Solver, state: State) *bool {
        const r = @as(usize, @intCast(state.r));
        const c = @as(usize, @intCast(state.c));
        const d = @intFromEnum(state.dir);
        return &self._seen[(r * self.grid.width + c) * 4 + d];
    }

    // Adds `state` to `self.todo` if it is in bounds and not yet in `self.seen`.
    fn _maybeAdd(self: *Solver, state: State) !void {
        if (!self.grid.inBounds(state.r, state.c)) return;
        const v = self._getSeen(state);
        if (v.*) return;
        v.* = true;
        return self._todo.append(state);
    }

    // Calculates how many tiles would be illuminated if the light beam starts
    // from row r, column c and direction dir. Runs in O(answer) time.
    fn solve(self: *Solver, r: isize, c: isize, dir: Dir) !usize {
        // Add initial state.
        std.debug.assert(self._todo.items.len == 0);
        try self._maybeAdd(State{ .r = r, .c = c, .dir = dir });
        std.debug.assert(self._todo.items.len == 1);

        // Breadth-first search for reachable states. (Depth-first search would
        // also work. This is just convenient.)
        var answer: usize = 0;
        var pos: usize = 0;
        while (pos < self._todo.items.len) : (pos += 1) {
            const state = self._todo.items[pos];
            const ptr = self._getIlluminated(state);
            if (!ptr.*) {
                answer += 1;
                ptr.* = true;
            }
            switch (self.grid.charAt(state.r, state.c)) {
                '.' => {
                    try self._maybeAdd(state.step(state.dir));
                },
                '|' => {
                    if (state.dir != .s) try self._maybeAdd(state.step(.n));
                    if (state.dir != .n) try self._maybeAdd(state.step(.s));
                },
                '-' => {
                    if (state.dir != .w) try self._maybeAdd(state.step(.e));
                    if (state.dir != .e) try self._maybeAdd(state.step(.w));
                },
                '/' => {
                    switch (state.dir) {
                        .n => try self._maybeAdd(state.step(.e)),
                        .e => try self._maybeAdd(state.step(.n)),
                        .s => try self._maybeAdd(state.step(.w)),
                        .w => try self._maybeAdd(state.step(.s)),
                    }
                },
                '\\' => {
                    switch (state.dir) {
                        .n => try self._maybeAdd(state.step(.w)),
                        .e => try self._maybeAdd(state.step(.s)),
                        .s => try self._maybeAdd(state.step(.e)),
                        .w => try self._maybeAdd(state.step(.n)),
                    }
                },
                else => return error.InvalidInput,
            }
        }

        // Cleanup. We want to clear _todo, and reset _illuminated and _seen to
        // all false values for the next call to solve(). The optimal method
        // depends on how many states we visited.
        if (pos < self._seen.len / 16) {
            // Relatively few states visited. Erase only the visited states.
            for (self._todo.items) |state| {
                self._getIlluminated(state).* = false;
                self._getSeen(state).* = false;
            }
        } else {
            // Many states visited. Zero out everything at once.
            @memset(self._illuminated, false);
            @memset(self._seen, false);
        }
        self._todo.clearRetainingCapacity();

        return answer;
    }
};

fn solvePart1(solver: *Solver) !usize {
    return solver.solve(0, 0, .e);
}

fn solvePart2(solver: *Solver) !usize {
    std.debug.assert(solver.grid.width > 0 and solver.grid.height > 0);
    var answer: usize = 0;
    const last_c = @as(isize, @intCast(solver.grid.width - 1));
    var r: isize = 0;
    while (r < solver.grid.height) : (r += 1) {
        answer = @max(answer, try solver.solve(r, 0, .e));
        answer = @max(answer, try solver.solve(r, last_c, .w));
    }
    const last_r = @as(isize, @intCast(solver.grid.height - 1));
    var c: isize = 0;
    while (c < solver.grid.width) : (c += 1) {
        answer = @max(answer, try solver.solve(0, c, .s));
        answer = @max(answer, try solver.solve(last_r, c, .n));
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const grid = try env.parseInput(Grid, Grid.init);
    var solver = try Solver.init(env.getHeapAllocator(), grid);
    defer solver.deinit();

    try env.setAnswer1(try solvePart1(&solver));
    try env.setAnswer2(try solvePart2(&solver));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\.|...\....
        \\|.-.\.....
        \\.....|-...
        \\........|.
        \\..........
        \\.........\
        \\..../.\\..
        \\.-.-/..|..
        \\.|....-|.\
        \\..//.|....
        \\
    , "46", "51");
}
