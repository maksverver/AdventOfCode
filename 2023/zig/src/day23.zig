const Environment = @import("framework/Environment.zig");
const grids = @import("parsing/grids.zig");
const Grid = grids.TextGrid;
const Dir = grids.Dir;
const Coords = grids.Coords;
const std = @import("std");

const Vertex = u6;
const VertexMask = u64;
const no_vertex = std.math.maxInt(Vertex);
const Length = u32;
const Edge = struct { w: Vertex, len: Length };

const start: Vertex = 0;
const finish: Vertex = 1;

fn getSlopeDir(ch: u8) ?Dir {
    return switch (ch) {
        '^' => .n,
        '>' => .e,
        'v' => .s,
        '<' => .w,
        else => null,
    };
}

fn countNeighbors(grid: Grid, pos: Coords, respect_slopes: bool) u8 {
    if (respect_slopes) {
        if (getSlopeDir(grid.atPos(pos))) |dir| {
            // Must follow slope dir.
            if (grid.move(pos, dir, 1)) |new_pos| {
                if (grid.atPos(new_pos) != '#') return 1;
            }
            return 0;
        }
    }
    var res: u8 = 0;
    for (std.enums.values(Dir)) |dir| {
        if (grid.move(pos, dir, 1)) |new_pos| {
            if (grid.atPos(new_pos) != '#') res += 1;
        }
    }
    return res;
}

// Gets the neighbor of `pos` that is not `except_pos`, if there is one.
// If there is more than one option, one is arbitrarily returned.
fn getNeighbor(grid: Grid, pos: Coords, except_pos: Coords, respect_slopes: bool) ?Coords {
    if (respect_slopes) {
        if (getSlopeDir(grid.atPos(pos))) |dir| {
            // Must follow slope dir.
            if (grid.move(pos, dir, 1)) |new_pos| {
                if (grid.atPos(new_pos) != '#' and !std.meta.eql(new_pos, except_pos)) return new_pos;
            }
            return null;
        }
    }
    for (std.enums.values(Dir)) |dir| {
        if (grid.move(pos, dir, 1)) |new_pos| {
            if (grid.atPos(new_pos) != '#' and !std.meta.eql(new_pos, except_pos)) return new_pos;
        }
    }
    return null;
}

fn buildGraph(allocator: std.mem.Allocator, grid: Grid, respect_slopes: bool) ![][]Edge {
    // List of vertex coordinates. We create a vertex for the start and finish,
    // and for each junction, where a junction is a cell with more than two
    // neighbors.
    var vertex_coords = std.ArrayList(Coords).init(allocator);
    defer vertex_coords.deinit();

    // The vertex_index maps cell coords to vertex ids, or no_vertex if the
    // coords do not correspond with a junction.
    const VertexIndex = grids.Grid(Vertex, .{ .ownability = .ownable, .mutability = .mutable });
    var vertex_index = try VertexIndex.initAlloc(allocator, grid.height, grid.width, no_vertex);
    defer vertex_index.deinit();

    // Create two special vertices for the start and end positions.
    const start_pos = Coords{ .r = 0, .c = 1 };
    const finish_pos = Coords{ .r = grid.height - 1, .c = grid.width - 2 };
    std.debug.assert(grid.atPos(start_pos) == '.');
    std.debug.assert(grid.atPos(finish_pos) == '.');
    try vertex_coords.append(start_pos);
    try vertex_coords.append(finish_pos);
    vertex_index.ptrAtPos(start_pos).* = start;
    vertex_index.ptrAtPos(finish_pos).* = finish;

    // Now we'll do one pass over the grid to identify junctions.
    for (0..grid.height) |r| {
        for (0..grid.width) |c| {
            if (grid.at(r, c) != '#') {
                const pos = Coords{ .r = r, .c = c };
                if (countNeighbors(grid, pos, respect_slopes) > 2) {
                    const v: Vertex = @intCast(vertex_coords.items.len);
                    try vertex_coords.append(pos);
                    vertex_index.ptrAtPos(pos).* = v;
                }
            }
        }
    }

    // Finally, identify the paths between junctions (up to four per junction).
    var edgesList = std.ArrayList([]Edge).init(allocator);
    defer edgesList.deinit();
    defer for (edgesList.items) |edges| allocator.free(edges);
    for (vertex_coords.items, 0..) |p, v| {
        var edgeList = std.ArrayList(Edge).init(allocator);
        errdefer edgeList.deinit();
        for (std.enums.values(Dir)) |dir| {
            if (grid.move(p, dir, 1)) |q| {
                if (grid.atPos(q) == '#') continue;

                // Follow corridors until we hit the next junction.
                var prev = p;
                var cur = q;
                var len: Length = 1;
                while (vertex_index.atPos(cur) == no_vertex) {
                    if (getNeighbor(grid, cur, prev, respect_slopes)) |next| {
                        prev = cur;
                        cur = next;
                        len += 1;
                    } else break;
                }
                const w = vertex_index.atPos(cur);
                if (w != v and w != no_vertex) {
                    // Neither a loop nor a dead-end.
                    try edgeList.append(.{ .w = w, .len = len });
                }
            }
        }
        const edges = try edgeList.toOwnedSlice();
        errdefer allocator.free(edges);
        try edgesList.append(edges);
    }
    return try edgesList.toOwnedSlice();
}

// Depth-first search for the longest path.
fn findLongestPath(graph: []const []const Edge, v: Vertex, visited_arg: VertexMask) isize {
    if (v == finish) return 0;
    const visited = visited_arg | (@as(VertexMask, 1) << v);
    var res: isize = std.math.minInt(isize);
    for (graph[v]) |e| {
        if ((visited & (@as(VertexMask, 1) << e.w)) == 0) {
            res = @max(res, e.len + findLongestPath(graph, e.w, visited));
        }
    }
    return res;
}

fn solvePart(allocator: std.mem.Allocator, grid: Grid, respect_slopes: bool) !isize {
    const graph: []const []const Edge = try buildGraph(allocator, grid, respect_slopes);
    defer allocator.free(graph);
    defer for (graph) |edges| allocator.free(edges);
    return findLongestPath(graph, start, 0);
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    const grid = try env.parseInput(Grid, Grid.initFromText);
    try env.setAnswer1(try solvePart(allocator, grid, true));
    try env.setAnswer2(try solvePart(allocator, grid, false));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\#.#####################
        \\#.......#########...###
        \\#######.#########.#.###
        \\###.....#.>.>.###.#.###
        \\###v#####.#v#.###.#.###
        \\###.>...#.#.#.....#...#
        \\###v###.#.#.#########.#
        \\###...#.#.#.......#...#
        \\#####.#.#.#######.#.###
        \\#.....#.#.#.......#...#
        \\#.#####.#.#.#########v#
        \\#.#...#...#...###...>.#
        \\#.#.#v#######v###.###v#
        \\#...#.>.#...>.>.#.###.#
        \\#####v#.#.###v#.#.###.#
        \\#.....#...#...#.#.#...#
        \\#.#########.###.#.#.###
        \\#...###...#...#...#.###
        \\###.###.#.###v#####v###
        \\#...#...#.#.>.>.#.>.###
        \\#.###.###.#.###.#.#v###
        \\#.....###...###...#...#
        \\#####################.#
        \\
    , "94", "154");
}
