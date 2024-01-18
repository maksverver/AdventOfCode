// Really optimized version of Day 14, which also runs great on larger inputs.
//
// For a more sensible but slower solution see unused/day14-slow.zig

const Environment = @import("framework/Environment.zig");
const grids = @import("util/grids.zig");
const Dir = grids.Dir;
const Coords = grids.Coords;
const std = @import("std");

const GridElem = enum { empty, boulder, wall };
const Grid = grids.Grid(GridElem, .{});
const OwnedGrid = grids.Grid(GridElem, .{ .ownability = .ownable });

const Stripes = struct {
    start: Coords,
    along: Dir,
    across: Dir,
};

// Returns the four orientations of the grid. Order matters!
//
// Note that east comes first because it represents the orientation that the
// boulders are in *after* tumbling east, which is the last direction after
// tumbling north, west, south, east in that order.
fn getStripes(grid: Grid) [4]Stripes {
    const W = grid.width;
    const H = grid.height;
    // zig fmt: off
    return .{
        .{ .start = Coords{ .r = 0,     .c = W - 1 }, .along = .w, .across = .s }, // East (reverse rows)
        .{ .start = Coords{ .r = 0,     .c = 0 },     .along = .s, .across = .e }, // North (columns)
        .{ .start = Coords{ .r = H - 1, .c = 0 },     .along = .e, .across = .n }, // West (rows)
        .{ .start = Coords{ .r = H - 1, .c = W - 1 }, .along = .n, .across = .w }, // South (reverse columns)
    };
    // zig fmt: on
}

fn parseInput(allocator: std.mem.Allocator, text: []const u8) !OwnedGrid {
    const input = try grids.TextGrid.initFromText(text);
    var grid = try grids.Grid(GridElem, .{ .ownability = .ownable, .mutability = .mutable })
        .initAlloc(allocator, input.height, input.width, undefined);
    errdefer grid.deinit();
    for (0..input.height) |r| {
        for (0..input.width) |c| {
            grid.ptrAt(r, c).* = switch (input.at(r, c)) {
                '.' => .empty,
                'O' => .boulder,
                '#' => .wall,
                else => return error.InvalidInput,
            };
        }
    }
    return grid.asReadonly();
}

fn solvePart1(grid: Grid) usize {
    var total_load: usize = 0;
    for (0..grid.width) |c| {
        var load = grid.height;
        for (0..grid.height) |r| {
            switch (grid.at(r, c)) {
                .empty => {},
                .boulder => {
                    total_load += load;
                    load -= 1;
                },
                .wall => {
                    load = grid.height - 1 - r;
                },
            }
        }
    }
    return total_load;
}

// Space are all cells that are not walls (i.e. both boulders and empty cells)
fn countSpace(grid: Grid) usize {
    var res: usize = 0;
    for (0..grid.height) |r| {
        for (0..grid.width) |c| {
            if (grid.at(r, c) != .wall) res += 1;
        }
    }
    return res;
}

// Represents a stack of boulders starting at `pos` and extending in the given
// direction. To calculate boulder positions, we also need to know the count
// of boulders per stack, which is tracked separately (in the `counts` array).
const BoulderStack = struct {
    pos: Coords,
    dir: Dir,
};

const Part2Solver = struct {
    const total_steps: usize = 1_000_000_000;
    const no_index: usize = std.math.maxInt(usize);

    grid: Grid,
    stacks: std.ArrayList(BoulderStack),
    next_wall_data: []usize,
    next_wall_start: []usize,
    counts: []u8,
    allocator: std.mem.Allocator,

    fn init(allocator: std.mem.Allocator, grid: Grid) !Part2Solver {
        const stripes = getStripes(grid);

        // Precalculate the nearest wall for grid position and each direction.
        //
        // We assign each side of the wall a separate wall index between 0 and
        // wall_count (so a single # can have 4 wall indices, one for each side).
        // Additionally, the edges of the grid are also assigned wall indices.
        //
        // (See the example below.)
        const WallIndex = grids.Grid(usize, .{ .ownability = .ownable, .mutability = .mutable });
        var wall_index: [4]WallIndex = undefined;
        @memset(&wall_index, WallIndex.initEmpty());
        defer for (wall_index) |elem| elem.deinit();

        // For calculating the final answer, we maintain the start position and
        // direction of each wall.
        var stacks = std.ArrayList(BoulderStack).init(allocator);
        errdefer stacks.deinit();

        // Walls are numbered consecutively across all directions, but we keep track
        // of the range of wall numbers assigned to each direction.
        for (0..4) |dir| {
            wall_index[dir] = try WallIndex.initAlloc(allocator, grid.height, grid.width, no_index);
            const stripe = stripes[dir];
            var start_it = grid.iterateDir(stripe.across, stripe.start);
            while (start_it.next()) |start| {
                var wall = no_index;
                var pos_it = grid.iterateDir(stripe.along, start);
                while (pos_it.next()) |pos| {
                    switch (grid.atPos(pos)) {
                        .wall => wall = no_index,
                        else => {
                            if (wall == no_index) {
                                wall = stacks.items.len;
                                try stacks.append(.{ .pos = pos, .dir = stripe.along });
                            }
                            wall_index[dir].ptrAtPos(pos).* = wall;
                        },
                    }
                }
            }
        }
        const wall_count = stacks.items.len;

        // Now we can calculate for each wall and direction where boulders resting
        // against it end up. For example, given the grid on the left below, we
        // can calculate the wall indices (with walls between square brackets, and
        // numbers indicating the nearest wall in each direction):
        //
        // Grid           East                North             West            South
        //
        //                              [3][4] -
        //          +-----------+      +---------+       +---------+    +-------------+
        //  . . #   | 0  0  [0] |  -   | 3  4 [6]|  [10] | 10 10  - |   |  14  13   - |
        //  . # .   | 2 [2]  1  | [1]  | 3 [5] 6 |   [8] |  8 [9] 9 |   |  14 [13] 11 |
        //  # O O   | -  3   3  | [3]  | -  5  6 |   [7] |  7  7  7 |   | [14] 12  11 |
        //          +-----------+      +---------+       +---------+    +-------------+
        //                                                                  - [12][11]
        //
        // Then if the east wall 3 has two boulders resting against it, then
        // tumbling north next, would move the first boulder up to wall 6, and
        // the second boulder to wall 5, so for wall index 3 we can precompute
        // [5, 6], etc.
        //
        var next_wall_data = try allocator.alloc(usize, countSpace(grid) * 4);
        errdefer allocator.free(next_wall_data);

        // The ranges of walls are encoded by consecutive offsets into next_wall_data.
        // In the above example, we want to record the next walls of 3 as 6 and 4,
        // so next_wall_data[next_wall_start[3]..next_wall_start[4]] = {6, 4}.
        var next_wall_start = try allocator.alloc(usize, wall_count);
        errdefer allocator.free(next_wall_start);
        var wall_number: usize = 0;
        var next_wall_pos: usize = 0;
        for (0..4) |dir| {
            const next_dir = @as(u2, @intCast(dir)) +% 1;
            const stripe = stripes[dir];
            var start_it = grid.iterateDir(stripe.across, stripe.start);
            while (start_it.next()) |start| {
                var current_wall = no_index;
                var pos_it = grid.iterateDir(stripe.along, start);
                while (pos_it.next()) |pos| {
                    switch (grid.atPos(pos)) {
                        .wall => current_wall = no_index,
                        else => {
                            if (current_wall == no_index) {
                                next_wall_start[wall_number] = next_wall_pos;
                                current_wall = wall_number;
                                wall_number += 1;
                            }
                            next_wall_data[next_wall_pos] = wall_index[next_dir].atPos(pos);
                            next_wall_pos += 1;
                        },
                    }
                }
            }
        }
        std.debug.assert(wall_number == wall_count);
        std.debug.assert(next_wall_pos == next_wall_data.len);

        // Calculate counts after initially tilting north, using wall_index[1].
        //
        // counts[i] = the number of boulder resting against the i-th wall
        var counts = try allocator.alloc(u8, wall_count);
        errdefer allocator.free(counts);
        @memset(counts, 0);
        for (0..grid.height) |r| {
            for (0..grid.width) |c| {
                if (grid.at(r, c) == .boulder) {
                    counts[wall_index[1].at(r, c)] += 1;
                }
            }
        }
        var solver = Part2Solver{
            .grid = grid,
            .stacks = stacks,
            .next_wall_data = next_wall_data,
            .next_wall_start = next_wall_start,
            .counts = counts,
            .allocator = allocator,
        };
        return solver;
    }

    fn deinit(self: Part2Solver) void {
        self.allocator.free(self.counts);
        self.allocator.free(self.next_wall_start);
        self.allocator.free(self.next_wall_data);
        self.stacks.deinit();
    }

    fn tumbleAllDirections(self: *Part2Solver) !void {
        for (self.counts, self.next_wall_start) |*c, start| {
            const count = c.*;
            c.* = 0;
            for (self.next_wall_data[start .. start + count]) |i| self.counts[i] += 1;
        }
    }

    fn calculateSupport(self: *const Part2Solver) usize {
        // This works for all directions, even though we only use this in part 2,
        // where all boulders lie against eastern walls. We could use this to speed it
        // up slightly but it probably doesn't matter.
        var answer: usize = 0;
        for (self.counts, self.stacks.items) |count, stack| {
            var it = self.grid.iterateDir(stack.dir, stack.pos);
            for (0..count) |_| answer += self.grid.height - it.next().?.r;
        }
        return answer;
    }

    fn solve(self: *Part2Solver) !usize {
        // Now iterate until we can detect a cycle (using a HashMap).
        var steps: usize = 0;
        var last_seen = std.StringHashMap(u32).init(self.allocator);
        defer {
            var it = last_seen.keyIterator();
            while (it.next()) |key| self.allocator.free(key.*);
            last_seen.deinit();
        }
        while (true) {
            try self.tumbleAllDirections();
            steps += 1;

            var key: ?[]u8 = try self.allocator.dupe(u8, self.counts);
            defer if (key) |p| self.allocator.free(p);
            var res = try last_seen.getOrPut(key.?);
            if (!res.found_existing) {
                key = null; // last_seen owns the key now
                res.value_ptr.* = @intCast(steps);
            } else {
                // Cycle found!
                const cycle_start = res.value_ptr.*;
                const cycle_len = steps - cycle_start;
                const steps_remaining = (total_steps - steps) % cycle_len;
                for (0..steps_remaining) |_| try self.tumbleAllDirections();
                return self.calculateSupport();
            }
        }
    }
};

fn solvePart2(allocator: std.mem.Allocator, grid: Grid) !usize {
    var solver = try Part2Solver.init(allocator, grid);
    defer solver.deinit();
    return solver.solve();
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    const grid = try env.parseInputAlloc(OwnedGrid, parseInput, allocator);
    defer grid.deinit();

    try env.setAnswer1(solvePart1(grid.asUnowned()));
    try env.setAnswer2(try solvePart2(allocator, grid.asUnowned()));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\O....#....
        \\O.OO#....#
        \\.....##...
        \\OO.#O....O
        \\.O.....O#.
        \\O.#..O.#.#
        \\..O..#O..O
        \\.......O..
        \\#....###..
        \\#OO..#....
        \\
    , "136", "64");
}
