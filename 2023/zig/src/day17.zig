const Environment = @import("framework/Environment.zig");
const Grid = @import("parsing/Grid.zig");
const Coords = Grid.Coords;
const Dir = Grid.Dir;
const std = @import("std");

const State = struct {
    dist: usize,
    pos: Coords,
    last_dir: Dir,

    fn compareDist(_: void, a: State, b: State) std.math.Order {
        return std.math.order(a.dist, b.dist);
    }
};

fn getDist(dist: []usize, grid: Grid, state: State) *usize {
    return &dist[(state.pos.r * grid.width + state.pos.c) * 2 + state.last_dir.axis()];
}

fn solvePart(allocator: std.mem.Allocator, grid: Grid, min_repeat: usize, max_repeat: usize) !usize {
    var todo = std.PriorityQueue(State, void, State.compareDist).init(allocator, {});
    defer todo.deinit();

    var dist = try allocator.alloc(usize, grid.width * grid.height * 2);
    defer allocator.free(dist);
    @memset(dist, std.math.maxInt(usize));

    // Use Dijkstra's algorithm to find shortest path.
    try todo.add(State{ .dist = 0, .pos = .{ .r = 0, .c = 0 }, .last_dir = .e });
    try todo.add(State{ .dist = 0, .pos = .{ .r = 0, .c = 0 }, .last_dir = .s });
    dist[0] = 0;
    dist[1] = 0;
    while (todo.len > 0) {
        const state = todo.remove();
        const dist_p = getDist(dist, grid, state);
        if (dist_p.* < state.dist) continue;
        if (state.pos.r == grid.height - 1 and state.pos.c == grid.width - 1) return state.dist;
        const dirs = [2]Dir{ state.last_dir.prev(), state.last_dir.next() };
        for (dirs) |dir| {
            var new_pos = state.pos;
            var new_dist = state.dist;
            for (1..max_repeat + 1) |steps| {
                new_pos = grid.move(new_pos, dir, 1) orelse break;
                std.debug.assert(std.ascii.isDigit(grid.charAtPos(new_pos)));
                new_dist += grid.charAtPos(new_pos) - '0';
                if (steps >= min_repeat) {
                    const new_state = State{ .dist = new_dist, .pos = new_pos, .last_dir = dir };
                    const new_dist_p = getDist(dist, grid, new_state);
                    if (new_state.dist < new_dist_p.*) {
                        new_dist_p.* = new_state.dist;
                        try todo.add(new_state);
                    }
                }
            }
        }
    }
    @panic("no solution found");
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    const grid = try env.parseInput(Grid, Grid.init);
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
