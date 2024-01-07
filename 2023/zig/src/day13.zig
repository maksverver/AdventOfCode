const Environment = @import("framework/Environment.zig");
const grids = @import("parsing/grids.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

const Grid = grids.ReorientableGrid(u8, false);

pub fn findReflectionRow(grid: Grid, comptime want_errors: usize) ?usize {
    loop: for (1..grid.height) |rr| {
        var errors: usize = 0;
        for (0..@min(rr, grid.height - rr)) |r| {
            for (0..grid.width) |c| {
                if (grid.charAt(rr + r, c) != grid.charAt(rr - 1 - r, c)) {
                    errors += 1;
                    if (errors > want_errors) continue :loop;
                }
            }
        }
        if (errors == want_errors) return rr;
    }
    return null;
}

pub fn solvePart(grid: Grid, comptime errors: usize) !usize {
    if (findReflectionRow(grid, errors)) |r| return r * 100;
    if (findReflectionRow(grid.transposed(), errors)) |c| return c;
    return error.InvalidInput;
}

pub fn solve(env: *Environment) !void {
    var it = try text.ParagraphIterator.init(env.getInput());
    var answer1: usize = 0;
    var answer2: usize = 0;
    while (it.next()) |p| {
        const grid = try Grid.init(p);
        answer1 += try solvePart(grid, 0);
        answer2 += try solvePart(grid, 1);
    }
    try env.setAnswers(answer1, answer2);
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\#.##..##.
        \\..#.##.#.
        \\##......#
        \\##......#
        \\..#.##.#.
        \\..##..##.
        \\#.#.##.#.
        \\
        \\#...##..#
        \\#....#..#
        \\..##..###
        \\#####.##.
        \\#####.##.
        \\..##..###
        \\#....#..#
        \\
    , "405", "400");
}
