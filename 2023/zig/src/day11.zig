const Environment = @import("framework/Environment.zig");
const Grid = @import("parsing/Grid.zig");
const std = @import("std");

const Answer = u64;

fn countGalaxies(grid: Grid) usize {
    var res: usize = 0;
    for (0..grid.height) |r| {
        for (0..grid.width) |c| {
            if (grid.charAtU(r, c) == '#') res += 1;
        }
    }
    return res;
}

fn countGalaxiesInRow(grid: Grid, r: usize) usize {
    var res: usize = 0;
    for (0..grid.width) |c| {
        if (grid.charAtU(r, c) == '#') res += 1;
    }
    return res;
}

fn countGalaxiesInCol(grid: Grid, c: usize) usize {
    var res: usize = 0;
    for (0..grid.height) |r| {
        if (grid.charAtU(r, c) == '#') res += 1;
    }
    return res;
}

const expand1 = 2;
const expand2 = 1_000_000;

pub fn solve(env: *Environment) !void {
    const grid = try env.parseInput(Grid, Grid.init);
    const total = countGalaxies(grid);
    var answer1: Answer = 0;
    var answer2: Answer = 0;
    var n: usize = 0;
    for (0..grid.width) |c| {
        const pop = countGalaxiesInCol(grid, c);
        if (pop == 0) {
            answer1 += expand1 * n * (total - n);
            answer2 += expand2 * n * (total - n);
        } else {
            answer1 += n * (total - n);
            answer2 += n * (total - n);
            n += pop;
        }
    }
    var m: usize = 0;
    for (0..grid.height) |r| {
        const pop = countGalaxiesInRow(grid, r);
        if (pop == 0) {
            answer1 += expand1 * m * (total - m);
            answer2 += expand2 * m * (total - m);
        } else {
            answer1 += m * (total - m);
            answer2 += m * (total - m);
            m += pop;
        }
    }
    try env.setAnswers(answer1, answer2);
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\...#......
        \\.......#..
        \\#.........
        \\..........
        \\......#...
        \\.#........
        \\.........#
        \\..........
        \\.......#..
        \\#...#.....
        \\
    , "374", "82000210");
}
