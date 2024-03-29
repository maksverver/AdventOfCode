const Environment = @import("framework/Environment.zig");
const grids = @import("util/grids.zig");
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

fn bit(v: Vertex) VertexMask {
    return @as(VertexMask, 1) << v;
}

// Depth-first search for the longest path.
//
// We could memoize this based on (v, visited) pairs, but for the official test
// input, this method is called around 30 million times with around 11 million
// unique pairs of (v, visited), so memoization has little effect.
fn findLongestPath(graph: []const []const Edge, end: Vertex, v: Vertex, visited_arg: VertexMask) isize {
    if (v == end) return 0;
    const visited = visited_arg | bit(v);
    var res: isize = std.math.minInt(isize);
    for (graph[v]) |e| {
        if ((visited & bit(e.w)) == 0) {
            res = @max(res, e.len + findLongestPath(graph, end, e.w, visited));
        }
    }
    return res;
}

fn solvePart(allocator: std.mem.Allocator, grid: Grid, respect_slopes: bool) !isize {
    // The hardest part is building the graph from the input:
    const graph: []const []const Edge = try buildGraph(allocator, grid, respect_slopes);
    defer allocator.free(graph);
    defer for (graph) |edges| allocator.free(edges);

    // At this point, we could calculate the longest path with:
    //
    //  return findLongestPath(graph, finish, start, 0);
    //
    // However, the search can be sped up by searching for the longest path from
    // start to a predecessor of `finish` instead. The logic is that the longest
    // path has to go through one of the predecessors of `finish` just before
    // reaching `finish`, so we can prune solutions that have visited all
    // predecessors without continuing to `finish`.
    //
    // In the official test data, `finish` has only one predecessor, and this
    // optimization cuts the runtime approximately in half.
    var answer: isize = std.math.minInt(isize);
    for (graph, 0..) |edges, i| {
        for (edges) |e| {
            if (e.w == finish) {
                const v: Vertex = @intCast(i);
                answer = @max(answer, findLongestPath(graph, v, start, bit(finish)) + e.len);
            }
        }
    }
    return answer;
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
