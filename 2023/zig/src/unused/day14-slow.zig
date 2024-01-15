// Solution to day 14 that explicitly simulates all moves. This is pretty short
// and a cool application of the orientable grid, but it is much slower than
// the optimized version in day14.zig.

const Environment = @import("framework/Environment.zig");
const grids = @import("parsing/grids.zig");
const std = @import("std");

const InputGrid = grids.Grid(u8, .{
    .orientability = .orientable,
});
const OwnedGrid = grids.Grid(u8, .{
    .orientability = .orientable,
    .ownability = .ownable,
    .mutability = .mutable,
});

// For debugging (currently unused)
fn debugPrint(grid: OwnedGrid) !void {
    std.debug.print("\n", .{});
    for (0..grid.height) |r| {
        for (0..grid.width) |c| {
            std.debug.print("{c}", .{grid.at(r, c)});
        }
        std.debug.print("\n", .{});
    }
}

fn moveUp(grid: *OwnedGrid) void {
    for (0..grid.width) |c| {
        var r_dst: usize = 0;
        for (0..grid.height) |r_src| {
            switch (grid.at(r_src, c)) {
                '#' => {
                    r_dst = r_src + 1;
                },
                'O' => {
                    grid.ptrAt(r_src, c).* = '.';
                    grid.ptrAt(r_dst, c).* = 'O';
                    r_dst += 1;
                },
                else => {},
            }
        }
    }
}

fn computeSupport(grid: OwnedGrid) usize {
    var answer: usize = 0;
    for (0..grid.height) |r| {
        for (0..grid.width) |c| {
            if (grid.at(r, c) == 'O') answer += grid.height - r;
        }
    }
    return answer;
}

fn solvePart1(allocator: std.mem.Allocator, input: InputGrid) !usize {
    var grid = try input.duplicate(.mutable, allocator);
    defer grid.deinit();
    moveUp(&grid);
    return computeSupport(grid);
}

pub fn step(grid: *OwnedGrid) void {
    for (0..4) |_| {
        moveUp(grid);
        grid.* = grid.rotatedAnticlockwise();
    }
}

// Number of steps to execute for part 2.
const target2: usize = 1000_000_000;

// Cycle finding.
// https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare
fn solvePart2(allocator: std.mem.Allocator, input: InputGrid) !usize {
    var grid1 = try input.duplicate(.mutable, allocator);
    defer grid1.deinit();
    var grid2 = try input.duplicate(.mutable, allocator);
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
    const input = try env.parseInput(InputGrid, InputGrid.initFromText);

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
