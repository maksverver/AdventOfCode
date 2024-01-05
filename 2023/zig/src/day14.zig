const Environment = @import("framework/Environment.zig");
const grids = @import("parsing/grids.zig");
const std = @import("std");

const Input = grids.ReorientableGrid(u8, false);
const Grid = grids.ReorientableGrid(u8, true);

// For debugging (currently unused)
fn debugPrint(grid: Grid) !void {
    std.debug.print("\n", .{});
    for (0..grid.height) |r| {
        for (0..grid.width) |c| {
            std.debug.print("{c}", .{grid.charAtU(r, c)});
        }
        std.debug.print("\n", .{});
    }
}

fn moveUp(grid: *Grid) void {
    for (0..grid.width) |c| {
        var r_dst: usize = 0;
        for (0..grid.height) |r_src| {
            switch (grid.charAtU(r_src, c)) {
                '#' => {
                    r_dst = r_src + 1;
                },
                'O' => {
                    grid.charPtrAtU(r_src, c).* = '.';
                    grid.charPtrAtU(r_dst, c).* = 'O';
                    r_dst += 1;
                },
                else => {},
            }
        }
    }
}

fn computeSupport(grid: Grid) usize {
    var answer: usize = 0;
    for (0..grid.height) |r| {
        for (0..grid.width) |c| {
            if (grid.charAtU(r, c) == 'O') answer += grid.height - r;
        }
    }
    return answer;
}

fn solvePart1(allocator: std.mem.Allocator, input: Input) !usize {
    var grid = try input.mutableCopy(allocator);
    defer grid.deinit();
    moveUp(&grid);
    return computeSupport(grid);
}

pub fn step(grid: *Grid) void {
    for (0..4) |_| {
        moveUp(grid);
        grid.* = grid.rotatedAnticlockwise();
    }
}

// Number of steps to execute for part 2.
const target2: usize = 1000_000_000;

// Cycle finding.
// https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare
fn solvePart2(allocator: std.mem.Allocator, input: Input) !usize {
    var grid1 = try input.mutableCopy(allocator);
    defer grid1.deinit();
    var grid2 = try input.mutableCopy(allocator);
    defer grid2.deinit();
    step(&grid1);
    step(&grid2);
    step(&grid2);
    var steps1: usize = 1;
    while (!grid1.isEqualTo(grid2)) : (steps1 += 1) {
        step(&grid1);
        step(&grid2);
        step(&grid2);
    }
    step(&grid1);
    step(&grid2);
    step(&grid2);
    var steps2: usize = steps1 + 1;
    while (!grid1.isEqualTo(grid2)) : (steps2 += 1) {
        step(&grid1);
        step(&grid2);
        step(&grid2);
    }
    std.debug.assert(steps2 <= target2);
    const period = steps2 - steps1;
    for (0..target2 % period) |_| step(&grid1);
    return computeSupport(grid1);
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    const input = try env.parseInput(Input, Input.init);

    try env.setAnswer1(try solvePart1(allocator, input));
    try env.setAnswer2(try solvePart2(allocator, input));
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
