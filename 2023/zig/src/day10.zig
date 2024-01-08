const Environment = @import("framework/Environment.zig");
const Grid = @import("parsing/Grid.zig");
const Coords = Grid.Coords;
const Dir = Grid.Dir;
const std = @import("std");

const Connections = struct {
    n: bool = false,
    e: bool = false,
    s: bool = false,
    w: bool = false,

    fn count(c: Connections) usize {
        return @as(usize, @intFromBool(c.n)) +
            @as(usize, @intFromBool(c.e)) +
            @as(usize, @intFromBool(c.s)) +
            @as(usize, @intFromBool(c.w));
    }
};

fn getConnections(ch: u8) Connections {
    return switch (ch) {
        '|' => .{ .n = true, .s = true },
        '-' => .{ .e = true, .w = true },
        'L' => .{ .n = true, .e = true },
        'J' => .{ .n = true, .w = true },
        '7' => .{ .s = true, .w = true },
        'F' => .{ .s = true, .e = true },
        else => .{},
    };
}

fn nextDirection(c: Connections, d: Dir) !Dir {
    if (c.n and d != .s) return .n;
    if (c.e and d != .w) return .e;
    if (c.s and d != .n) return .s;
    if (c.w and d != .e) return .w;
    return error.InvalidInput;
}

pub fn solve(env: *Environment) !void {
    const grid = try env.parseInput(Grid, Grid.init);

    // Find the start, and determine the connections from the surrounding tiles.
    const start = try grid.indexOf('S');
    const startConnections = Connections{
        .n = if (grid.move(start, .n, 1)) |q| getConnections(grid.charAtPos(q)).s else false,
        .e = if (grid.move(start, .e, 1)) |q| getConnections(grid.charAtPos(q)).w else false,
        .s = if (grid.move(start, .s, 1)) |q| getConnections(grid.charAtPos(q)).n else false,
        .w = if (grid.move(start, .w, 1)) |q| getConnections(grid.charAtPos(q)).e else false,
    };
    std.debug.assert(startConnections.count() == 2);

    // Now follow the path, which is a simple polygon, and calculate its
    // area and perimeter.
    //
    // The perimeter is simply the number of steps taken along the path.
    //
    // The area is calculated using the shoelace formula, simplified for the
    // special case where we only move 1 step in one of 4 ortogonal directions
    // at a time.
    //
    // For the general case, see: https://en.wikipedia.org/wiki/Shoelace_formula
    var pos = start;
    var area: isize = 0;
    var perimeter: isize = 0;
    var dir = try nextDirection(startConnections, .w);
    while (true) {
        perimeter += 1;
        switch (dir) {
            .n => {
                pos.r -= 1;
            },
            .e => {
                area += @as(isize, @intCast(pos.r));
                pos.c += 1;
            },
            .s => {
                pos.r += 1;
            },
            .w => {
                pos.c -= 1;
                area -= @as(isize, @intCast(pos.r));
            },
        }
        if (pos.r == start.r and pos.c == start.c) break;
        dir = try nextDirection(getConnections(grid.charAtPos(pos)), dir);
    }

    // Part 1: report the maximum distance from the start. This is simply
    // half the perimeter (which is necessarily even).
    const answer1 = @divExact(perimeter, 2);

    // Part 2: report the number of points of the interior.
    //
    // We can calulate this using Pick's theorem, which states:
    //
    //  A = i + b/2 - 1
    //
    // therefore:
    //
    //  i = A - b/2 + 1
    //
    // where A is the area (which we've calculated), i is the number of interior
    // points (which is the answer to part 2), and b is the number of boundary
    // points, so b/2 is simply the semiperimeter (which we've calculated as the
    // answer of part 1, above).
    //
    // See: https://en.wikipedia.org/wiki/Pick%27s_theorem
    const answer2 = try std.math.absInt(area) - answer1 + 1;

    try env.setAnswers(answer1, answer2);
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example 1" {
    try @import("framework/testing.zig").testSolver(solve,
        \\7-F7-
        \\.FJ|7
        \\SJLL7
        \\|F--J
        \\LJ.LJ
        \\
    , "8", null);
}

test "example 2" {
    try @import("framework/testing.zig").testSolver(solve,
        \\FF7FSF7F7F7F7F7F---7
        \\L|LJ||||||||||||F--J
        \\FL-7LJLJ||||||LJL-77
        \\F--JF--7||LJLJIF7FJ-
        \\L---JF-JLJIIIIFJLJJ7
        \\|F|F-JF---7IIIL7L|7|
        \\|FFJF7L7F-JF7IIL---7
        \\7-L-JL7||F7|L7F-7F7|
        \\L.L7LFJ|||||FJL7||LJ
        \\L7JLJL-JLJLJL--JLJ.L
        \\
    , null, "10");
}
