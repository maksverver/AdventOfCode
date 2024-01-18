const Environment = @import("framework/Environment.zig");
const grids = @import("util/grids.zig");
const TextGrid = grids.TextGrid;
const Coords = grids.Coords;
const Dir = grids.Dir;
const std = @import("std");

const inf = std.math.maxInt(Dist);
const Answer = u64;

const Dist = u32;
const DistGrid = grids.Grid(Dist, .{ .ownability = .ownable, .mutability = .mutable });

fn calculateReachability(allocator: std.mem.Allocator, grid: TextGrid) !DistGrid {
    const dist = try DistGrid.initAlloc(allocator, grid.height, grid.width, inf);
    errdefer dist.deinit();

    // For the breadth-first search, allocate a queue buffer equal to the size
    // of the grid, because we expect to cover most of the grid anyway.
    var buf = try allocator.alloc(Coords, grid.width * grid.height);
    defer allocator.free(buf);

    // Breadth-first search.
    const start = try grid.indexOf('S');
    buf[0] = start;
    dist.ptrAtPos(start).* = 0;
    var idx: usize = 0;
    var len: usize = 1;
    while (idx < len) : (idx += 1) {
        const p = buf[idx];
        for (std.enums.values(Dir)) |dir| {
            if (grid.move(p, dir, 1)) |q| {
                const dist_p = dist.ptrAtPos(q);
                if (grid.atPos(q) != '#' and dist_p.* == inf) {
                    dist_p.* = dist.atPos(p) + 1;
                    buf[len] = q;
                    len += 1;
                }
            }
        }
    }
    return dist;
}

// Since we can move back and forth between cells in 2 steps, that means a
// cell that is reachable in x steps is also reachable in x + 2k steps (for any
// nonnegative integer k). To calculate the number of cells reachable in a given
// total number of `steps`, we count all cells that are have a distance from the
// start less than or equal to `steps` and with the same parity as `steps`.
fn solvePart1(dist: DistGrid, steps: usize) Answer {
    var answer: Answer = 0;
    for (0..dist.height) |r| {
        for (0..dist.width) |c| {
            const d = dist.at(r, c);
            if (d <= steps and d % 2 == steps % 2) answer += 1;
        }
    }
    return answer;
}

// This is a lame solution to a pretty lame problem. It exploits the fact that
// the input is a square grid of size 131 with S in the center, and empty lanes
// as drawn:
//
//     + - - / | \ - - +
//     | . / . | . \ . |
//     | / . . | . . \ |
//     / . . . | . . . \
//     - - - - S - - - -
//     \ . . . | . . . /
//     | \ . . | . . / |
//     | . \ . | . / . |
//     + - - \ | / - - +
//
// It turns out that the grid is sparse enough so that all cells within the
// inner diamond that are reachable, are reachable within 65 steps, and the
// cells outside within 131 steps.
//
// The number of steps we need to move is exactly 202300 × 131 + 65 (note that
// 65 = 131 / 2 rounded up) so we can extrapolate the number of visitable cells
// from the number of reachable cells in the total grid and the inner diamond.
//
// Let's figure out how many copies of the original grid are reachable when we
// take k × 131 + 65 steps. We can infer this by extrapolating from the small
// value of k:
//
//
//                                  +--+
//                                  |  |
//               +---+           +--+  +--+
//               |   |           |        |
//    +--+    +--+   +--+     +--+  +  +  +--+
//    | 1|    |    5    |     |      13      |
//    +--+    +--+   +--+     +--+  +  +  +--+
//               |   |           |        |
//               +---+           +--+  +--+
//                                  |  |
//                                  +--+
//     k=0        k=1                k=2       etc.
//
//
// In general, the number of reachable copies is 2k(k + 1) + 1. But this number
// is only approximately correct, since we can move diagonally too, so the true
// pattern looks more like below:
//
//         (a)
//           +---+
//           |/ \|
//     (b)  /|   |\
//       +-+ +   +--+
//       |/        \|
//       |\        /|
//       +---+   +--+
//          \|   |/
//           |\ /| (c)
//           +---+
//
// If you compare this to the previous pattern for k=1, then you can see that
// e.g. the topleft triangle is missing in two places, labeled (a) and (b), and
// appears extra in a third place (c), and in general each of these corner
// triangles appears one less time than expected. This pattern continues for
// higher values of k.
//
// This means for the original grid, partitioned like this:
//
//      +-+-+
//      |/ \|
//      +   +
//      |\ /|
//      +-+-+
//
// The reachable cells in the inner diamond occur exactly 2k(k + 1) + 1 times,
// but the cells in the outer triangles only 2k(k + 1) times.
//
// Finally, we need to account for parity. Since the grid has odd size, the
// distances alternate between even and odd in copies of the grid. Let's assume
// k is even. Then for example the parity of the repeating grids is as follows:
//
//        0
//      0 1 0
//    0 1 0 1 0
//      0 1 0
//        0
//
// If the total number of steps is even, then cells at an even distance are
// only reachable at the (k + 1)×(k + 1) even subgrids, and the cells at an odd
// distance are only reachable at the k×k odd subgrids. If the total number of
// steps is odd, it's the other way around.

fn solvePart2(dist: DistGrid, steps: usize) Answer {
    std.debug.assert(dist.height == dist.width);
    const size = dist.width; // official input: 131
    const mid = size / 2; // official input: 65
    std.debug.assert(dist.at(mid, mid) == 0); // start at center
    std.debug.assert(steps % size == mid);
    const k = steps / size; // official input: 202300
    var answer: Answer = 0;
    for (0..dist.height) |r| {
        for (0..dist.width) |c| {
            const d = dist.at(r, c);
            if (d < inf) {
                if (d % 2 == steps % 2) {
                    answer += (k + 1) * (k + 1);
                } else {
                    answer += k * k;
                }
                if (d > mid) {
                    if (d % 2 == steps % 2) {
                        answer -= k + 1;
                    } else {
                        answer += k;
                    }
                }
            }
        }
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const grid = try env.parseInput(TextGrid, TextGrid.initFromText);
    const dist = try calculateReachability(env.getHeapAllocator(), grid);
    defer dist.deinit();
    try env.setAnswer1(solvePart1(dist, 64));
    try env.setAnswer2(solvePart2(dist, 26501365));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example 1" {
    const grid = try TextGrid.initFromText(
        \\...........
        \\.....###.#.
        \\.###.##..#.
        \\..#.#...#..
        \\....#.#....
        \\.##..S####.
        \\.##..#...#.
        \\.......##..
        \\.##.#.####.
        \\.##..##.##.
        \\...........
        \\
    );
    const dist = try calculateReachability(std.testing.allocator, grid);
    defer dist.deinit();
    try std.testing.expectEqual(@as(Answer, 16), solvePart1(dist, 6));
}
