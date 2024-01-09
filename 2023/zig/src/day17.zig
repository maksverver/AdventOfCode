const Environment = @import("framework/Environment.zig");
const grids = @import("parsing/grids.zig");
const Grid = grids.TextGrid;
const Coords = grids.Coords;
const Dir = grids.Dir;
const std = @import("std");

const State = struct {
    pos: Coords,
    last_dir: Dir,
};

fn getDist(dist: []usize, grid: Grid, state: State) *usize {
    return &dist[(state.pos.r * grid.width + state.pos.c) * 2 + state.last_dir.axis()];
}

const QueueT = std.ArrayListUnmanaged(std.ArrayListUnmanaged(State));

fn addState(allocator: std.mem.Allocator, todo: *QueueT, dist: usize, state: State) !void {
    while (dist >= todo.items.len) try todo.append(allocator, .{});
    return todo.items[dist].append(allocator, state);
}

fn solvePart(allocator: std.mem.Allocator, grid: Grid, min_repeat: usize, max_repeat: usize) !usize {
    var todo = QueueT{};
    defer todo.deinit(allocator);
    defer for (todo.items) |*list| list.deinit(allocator);

    var dists = try allocator.alloc(usize, grid.width * grid.height * 2);
    defer allocator.free(dists);
    @memset(dists, std.math.maxInt(usize));

    // Use Dijkstra's algorithm to find shortest path.
    dists[0] = 0;
    dists[1] = 0;
    try addState(allocator, &todo, 0, State{ .pos = .{ .r = 0, .c = 0 }, .last_dir = .e });
    try addState(allocator, &todo, 0, State{ .pos = .{ .r = 0, .c = 0 }, .last_dir = .s });
    var old_dist: usize = 0;
    while (old_dist < todo.items.len) {
        if (todo.items[old_dist].popOrNull()) |old_state| {
            if (getDist(dists, grid, old_state).* < old_dist) continue;
            if (old_state.pos.r == grid.height - 1 and old_state.pos.c == grid.width - 1) return old_dist;
            const dirs = [2]Dir{ old_state.last_dir.prev(), old_state.last_dir.next() };
            for (dirs) |dir| {
                var new_dist = old_dist;
                var new_pos = old_state.pos;
                for (1..max_repeat + 1) |steps| {
                    new_pos = grid.move(new_pos, dir, 1) orelse break;
                    std.debug.assert(std.ascii.isDigit(grid.atPos(new_pos)));
                    new_dist += grid.atPos(new_pos) - '0';
                    if (steps >= min_repeat) {
                        const new_state = State{ .pos = new_pos, .last_dir = dir };
                        const p = getDist(dists, grid, new_state);
                        if (new_dist < p.*) {
                            p.* = new_dist;
                            try addState(allocator, &todo, new_dist, new_state);
                        }
                    }
                }
            }
        } else {
            old_dist += 1;
        }
    }
    return error.NoSolutionFound;
}

pub fn solve(env: *Environment) !void {
    // For this problem, the arena allocator is a 2x as fast as the heap allocator,
    // at least when using Zig's general purpose allocator instead of the native
    // libc allocator.
    const allocator = env.getArenaAllocator();
    const grid = try env.parseInput(Grid, Grid.initFromText);
    try env.setAnswer1(try solvePart(allocator, grid, 1, 3));
    try env.setAnswer2(try solvePart(allocator, grid, 4, 10));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\2413432311323
        \\3215453535623
        \\3255245654254
        \\3446585845452
        \\4546657867536
        \\1438598798454
        \\4457876987766
        \\3637877979653
        \\4654967986887
        \\4564679986453
        \\1224686865563
        \\2546548887735
        \\4322674655533
        \\
    , "102", "94");
}
