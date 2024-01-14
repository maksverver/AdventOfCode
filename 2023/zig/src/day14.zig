// Really optimized version of Day 14, which also runs great on larger inputs.
//
// For a more sensible but slower solution see unused/day14-slow.zig

const Environment = @import("framework/Environment.zig");
const grids = @import("parsing/grids.zig");
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

fn getStripes(grid: Grid) [4]Stripes {
    const W = grid.width;
    const H = grid.height;
    // zig fmt: off
    return .{
        .{ .start = Coords{ .r = 0,     .c = 0 },     .along = .s, .across = .e }, // North (columns)
        .{ .start = Coords{ .r = H - 1, .c = 0 },     .along = .e, .across = .n }, // West (rows)
        .{ .start = Coords{ .r = H - 1, .c = W - 1 }, .along = .n, .across = .w }, // South (reverse columns)
        .{ .start = Coords{ .r = 0,     .c = W - 1 }, .along = .w, .across = .s }, // East (reverse rows)
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

const Hash = u64;

fn hashState(counts: []usize, changed: []usize, random_keys: []Hash) Hash {
    var hash: Hash = 0;
    for (changed) |i| hash ^= random_keys[i] *% counts[i];
    return hash;
}

const HashContext = struct {
    pub fn hash(_: HashContext, h: Hash) u64 {
        return @intCast(h);
    }

    pub fn eql(_: HashContext, a: Hash, b: Hash) bool {
        return a == b;
    }
};

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
    random_keys: []Hash,
    changed: std.ArrayList(usize),
    new_changed: std.ArrayList(usize),
    counts: []usize,
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
        // Grid         North             West            South         East
        //
        //           [0][1] -
        //          +---------+       +---------+   +-------------+   +--------------+
        //  . . #   | 0  1 [3]|   [7] | 7  7  - |   |  11  10   - |   | 12  12  [12] |  -
        //  . # O   | 0 [2] 3 |   [5] | 5 [6] 6 |   |  11 [10]  8 |   | 14 [14]  13  | [13]
        //  # . O   | -  2  3 |   [4] | 4  4  4 |   | [11]  9   8 |   | -   15   15  | [15]
        //          +---------+       +---------+   +-------------+   +--------------+
        //                                            -   [9]  [8]
        //
        // Then we start with two boulders resting against the south side of north
        // wall 3, the first of which will roll west against the east side of west
        // wall 6, and the second will roll against wall 4, so for wall index 3
        // we can precompute [6, 4], etc.
        //
        const space_count = countSpace(grid);
        var next_wall_data = try allocator.alloc(usize, space_count * 4);
        errdefer allocator.free(next_wall_data);

        // The ranges of walls are encoded by consecutive offsets into next_wall_data.
        // In the above example, we want to record the next walls of 3 as 6 and 4,
        // so next_wall_data[next_wall_start[3]..next_wall_start[4]] = {6, 4}.
        var next_wall_start = try allocator.alloc(usize, wall_count);
        errdefer allocator.free(next_wall_start);
        var wall_number: usize = 0;
        var buf_pos: usize = 0;
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
                                next_wall_start[wall_number] = buf_pos;
                                current_wall = wall_number;
                                wall_number += 1;
                            }
                            next_wall_data[buf_pos] = wall_index[next_dir].atPos(pos);
                            buf_pos += 1;
                        },
                    }
                }
            }
        }
        std.debug.assert(wall_number == wall_count);
        std.debug.assert(buf_pos == space_count * 4);

        // Generate random keys for walls.
        var random_keys = try allocator.alloc(Hash, wall_count);
        errdefer allocator.free(random_keys);
        {
            var prng = std.rand.DefaultPrng.init(31337);
            var rand = prng.random();
            for (random_keys) |*p| p.* = rand.int(Hash);
        }

        // Calculate initial counts.
        //
        // `changed` contains the indices of walls that have some boulders resting
        // against them, i.e. `changed` contains i iff. count[i] != 0.
        // `new_changed` is scratch space used to calculate changed.
        var changed = std.ArrayList(usize).init(allocator);
        errdefer changed.deinit();
        var new_changed = std.ArrayList(usize).init(allocator);
        errdefer new_changed.deinit();

        // counts[i] = the number of boulder resting against the i-th wall
        var counts = try allocator.alloc(usize, wall_count);
        errdefer allocator.free(counts);
        @memset(counts, 0);

        // Calculate initial counts after tilting north.
        for (0..grid.height) |r| {
            for (0..grid.width) |c| {
                if (grid.at(r, c) == .boulder) {
                    const i = wall_index[0].at(r, c);
                    if (counts[i] == 0) try changed.append(i);
                    counts[i] += 1;
                }
            }
        }
        var solver = Part2Solver{
            .grid = grid,
            .stacks = stacks,
            .next_wall_data = next_wall_data,
            .next_wall_start = next_wall_start,
            .random_keys = random_keys,
            .changed = changed,
            .new_changed = new_changed,
            .counts = counts,
            .allocator = allocator,
        };
        // Finish initial cyle by tilting in the other 3 directions too.
        for (1..4) |_| try solver.tumbleQuarterTurn();
        return solver;
    }

    fn deinit(self: Part2Solver) void {
        self.allocator.free(self.counts);
        self.new_changed.deinit();
        self.changed.deinit();
        self.allocator.free(self.random_keys);
        self.allocator.free(self.next_wall_start);
        self.allocator.free(self.next_wall_data);
        self.stacks.deinit();
    }

    fn tumbleQuarterTurn(self: *Part2Solver) !void {
        self.new_changed.clearRetainingCapacity();
        for (self.changed.items) |i| {
            std.debug.assert(self.counts[i] > 0);
            const start = self.next_wall_start[i];
            for (self.next_wall_data[start .. start + self.counts[i]]) |j| {
                if (self.counts[j] == 0) try self.new_changed.append(j);
                self.counts[j] += 1;
            }
            self.counts[i] = 0;
        }
        std.mem.swap(std.ArrayList(usize), &self.changed, &self.new_changed);
    }

    fn tumbleFullTurn(self: *Part2Solver) !void {
        for (0..4) |_| try self.tumbleQuarterTurn();
    }

    fn calculateSupport(self: *const Part2Solver) usize {
        // This works for all directions, even though we only use this in part 2,
        // where all boulders lie against eastern walls. We could use this to speed it
        // up slightly but it probably doesn't matter.
        const stacks = self.stacks.items;
        var answer: usize = 0;
        for (self.changed.items) |i| {
            var it = self.grid.iterateDir(stacks[i].dir, stacks[i].pos);
            for (0..self.counts[i]) |_| answer += self.grid.height - it.next().?.r;
        }
        return answer;
    }

    fn solve(self: *Part2Solver) !usize {
        // Now iterate until we can detect a cycle.
        var steps: usize = 1;
        var last_seen = std.HashMap(Hash, u32, HashContext, std.hash_map.default_max_load_percentage).init(self.allocator);
        defer last_seen.deinit();
        while (true) {
            try self.tumbleFullTurn();
            steps += 1;
            var res = try last_seen.getOrPut(hashState(self.counts, self.changed.items, self.random_keys));
            if (!res.found_existing) {
                res.value_ptr.* = @intCast(steps);
            } else {
                const cycle_start = res.value_ptr.*;
                const cycle_len = steps - cycle_start;
                for (0..(total_steps - steps) % cycle_len) |_| try self.tumbleFullTurn();
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
