const Environment = @import("framework/Environment.zig");
const grids = @import("util/grids.zig");
const Grid = grids.TextGrid;
const Dir = grids.Dir;
const std = @import("std");

fn entranceCount(grid: Grid) usize {
    return grid.height * 2 + grid.width * 2;
}

const StateOrEntrance = union(enum) {
    state: State,
    entrance: usize,
};

const State = struct {
    r: usize,
    c: usize,
    dir: Dir,

    fn step(state: State, grid: Grid, dir: Dir) StateOrEntrance {
        const height = grid.height;
        const width = grid.width;
        const r = state.r;
        const c = state.c;
        return switch (dir) {
            .e => if (c + 1 < width)
                .{ .state = .{ .r = r, .c = c + 1, .dir = .e } }
            else
                .{ .entrance = r + height },

            .w => return if (c > 0)
                .{ .state = .{ .r = r, .c = c - 1, .dir = .w } }
            else
                .{ .entrance = r },

            .n => return if (r > 0)
                .{ .state = .{ .r = r - 1, .c = c, .dir = .n } }
            else
                .{ .entrance = c + 2 * height },

            .s => if (r + 1 < height)
                .{ .state = .{ .r = r + 1, .c = c, .dir = .s } }
            else
                .{ .entrance = c + 2 * height + width },
        };
    }

    fn fromEntrance(grid: Grid, index: usize) State {
        const height = grid.height;
        const width = grid.width;
        if (index < 2 * height) {
            // Horizontal entrance.
            if (index < height) {
                return .{ .r = index, .c = 0, .dir = .e };
            } else {
                return .{ .r = index - height, .c = width - 1, .dir = .w };
            }
        } else {
            // Vertical entrance.
            if (index < 2 * height + width) {
                return .{ .r = 0, .c = index - 2 * height, .dir = .s };
            } else {
                std.debug.assert(index < 2 * height + 2 * width);
                return .{ .r = height - 1, .c = index - (2 * height + width), .dir = .n };
            }
        }
    }
};

test "State entrance indices" {
    const expectEqual = @import("util/testing.zig").expectEqual;

    const grid = try Grid.initFromText(
        \\....
        \\....
        \\....
        \\
    );

    // The 4 x 3 grid has 14 entrances with the following indices:
    //
    //      6 7 8 9
    //      v v v v
    //  0-> . . . . <-3
    //  1-> . . . . <-4
    //  2-> . . . . <-5
    //      ^ ^ ^ ^
    //    10 11 12 13
    //
    try expectEqual(entranceCount(grid), 14);

    try expectEqual(State.fromEntrance(grid, 0), State{ .r = 0, .c = 0, .dir = .e });
    try expectEqual(State.fromEntrance(grid, 2), State{ .r = 2, .c = 0, .dir = .e });
    try expectEqual(State.fromEntrance(grid, 3), State{ .r = 0, .c = 3, .dir = .w });
    try expectEqual(State.fromEntrance(grid, 5), State{ .r = 2, .c = 3, .dir = .w });
    try expectEqual(State.fromEntrance(grid, 6), State{ .r = 0, .c = 0, .dir = .s });
    try expectEqual(State.fromEntrance(grid, 9), State{ .r = 0, .c = 3, .dir = .s });
    try expectEqual(State.fromEntrance(grid, 10), State{ .r = 2, .c = 0, .dir = .n });
    try expectEqual(State.fromEntrance(grid, 13), State{ .r = 2, .c = 3, .dir = .n });

    for (0..entranceCount(grid)) |i| {
        const state = State.fromEntrance(grid, i);
        try expectEqual(state.step(grid, state.dir.reverse()), StateOrEntrance{ .entrance = i });
    }
}

const Solver = struct {
    grid: Grid,
    allocator: std.mem.Allocator,

    // These members are used to implement a breadth-first search in solve()).
    // _todo contains the reachable states.
    // _seen is a slice of size height × width that tracks whether a state is
    // present in todo.
    // _illuminated counts the number of distinct coordinate pairs in todo,
    // ignoring directions.
    _todo: std.ArrayList(State),
    _seen: []u4,
    _illuminated: usize,

    // `exits` records which entrances have been used as exits, which is used to
    // speed up part 2.
    exits: []bool,

    fn init(allocator: std.mem.Allocator, grid: Grid) !Solver {
        var todo = std.ArrayList(State).init(allocator);
        errdefer todo.deinit();
        const seen = try allocator.alloc(u4, grid.height * grid.width);
        errdefer allocator.free(seen);
        @memset(seen, 0);
        const exits = try allocator.alloc(bool, entranceCount(grid));
        errdefer allocator.free(exits);
        @memset(exits, false);
        return Solver{
            .grid = grid,
            ._todo = todo,
            ._seen = seen,
            ._illuminated = 0,
            .exits = exits,
            .allocator = allocator,
        };
    }

    fn deinit(self: Solver) void {
        self.allocator.free(self.exits);
        self.allocator.free(self._seen);
        self._todo.deinit();
    }

    pub fn _getSeen(self: *Solver, state: State) *u4 {
        const r = @as(usize, @intCast(state.r));
        const c = @as(usize, @intCast(state.c));
        return &self._seen[r * self.grid.width + c];
    }

    // Adds `state` to `self.todo` if it is in bounds and not yet in `self.seen`.
    fn _maybeAdd(self: *Solver, state: State) !void {
        const p = self._getSeen(state);
        if (p.* == 0) self._illuminated += 1;
        const bit = state.dir.asBit();
        if ((p.* & bit) != 0) return;
        p.* |= bit;
        return self._todo.append(state);
    }

    fn _step(self: *Solver, state: State, dir: Dir) !void {
        switch (state.step(self.grid, dir)) {
            .entrance => |e| self.exits[e] = true,
            .state => |s| try self._maybeAdd(s),
        }
    }

    // Calculates how many tiles would be illuminated if the light beam starts
    // from row r, column c and direction dir. Runs in O(answer) time.
    fn solve(self: *Solver, entrance: usize) !usize {
        // Add initial state.
        std.debug.assert(self._illuminated == 0);
        std.debug.assert(self._todo.items.len == 0);
        try self._maybeAdd(State.fromEntrance(self.grid, entrance));
        std.debug.assert(self._illuminated == 1);
        std.debug.assert(self._todo.items.len == 1);

        // Breadth-first search for reachable states. (Depth-first search would
        // also work. This is just convenient.)
        var pos: usize = 0;
        while (pos < self._todo.items.len) : (pos += 1) {
            const state = self._todo.items[pos];
            switch (self.grid.at(state.r, state.c)) {
                '.' => {
                    try self._step(state, state.dir);
                },
                '|' => {
                    if (state.dir != .s) try self._step(state, .n);
                    if (state.dir != .n) try self._step(state, .s);
                },
                '-' => {
                    if (state.dir != .w) try self._step(state, .e);
                    if (state.dir != .e) try self._step(state, .w);
                },
                '/' => {
                    switch (state.dir) {
                        .n => try self._step(state, .e),
                        .e => try self._step(state, .n),
                        .s => try self._step(state, .w),
                        .w => try self._step(state, .s),
                    }
                },
                '\\' => {
                    switch (state.dir) {
                        .n => try self._step(state, .w),
                        .e => try self._step(state, .s),
                        .s => try self._step(state, .e),
                        .w => try self._step(state, .n),
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
            for (self._todo.items) |state| self._getSeen(state).* = 0;
        } else {
            // Many states visited. Zero out everything at once.
            @memset(self._seen, 0);
        }
        self._todo.clearRetainingCapacity();

        const answer = self._illuminated;
        self._illuminated = 0;
        return answer;
    }
};

pub fn solve(env: *Environment) !void {
    const grid = try env.parseInput(Grid, Grid.initFromText);
    std.debug.assert(grid.width > 0 and grid.height > 0);

    var solver = try Solver.init(env.getHeapAllocator(), grid);
    defer solver.deinit();

    // Part 1: try only the first entrance at (0, 0) going east:
    var answer = try solver.solve(0);
    try env.setAnswer1(answer);

    // Part 2: try every other entrance too.
    for (1..entranceCount(grid)) |entrance| {
        // As an optimization, skip entrances which have been used as an exit
        // before. Entering there would cause only a subset of the previous set
        // of tiles to be visited, so we can disregard them for the purpose of
        // computing the maximum.
        if (solver.exits[entrance]) continue;
        answer = @max(answer, try solver.solve(entrance));
    }
    try env.setAnswer2(answer);
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
