const Environment = @import("framework/Environment.zig");
const Scanner = @import("parsing/Scanner.zig");
const std = @import("std");

const Ray = struct {
    x: i64,
    y: i64,
    z: i64,
    vx: i64,
    vy: i64,
    vz: i64,
};

fn parseInput(allocator: std.mem.Allocator, input: []const u8) ![]Ray {
    var list = std.ArrayList(Ray).init(allocator);
    errdefer list.deinit();
    var scanner = Scanner.init(input);
    while (!scanner.isEmpty()) {
        var x = try scanner.scanInt(i64);
        try scanner.skipText(", ");
        var y = try scanner.scanInt(i64);
        try scanner.skipText(", ");
        var z = try scanner.scanInt(i64);
        try scanner.skipText(" @ ");
        var vx = try scanner.scanInt(i64);
        try scanner.skipText(", ");
        var vy = try scanner.scanInt(i64);
        try scanner.skipText(", ");
        var vz = try scanner.scanInt(i64);
        try scanner.skipNewline();
        try list.append(Ray{ .x = x, .y = y, .z = z, .vx = vx, .vy = vy, .vz = vz });
    }
    return list.toOwnedSlice();
}

/// Returns true iff. two 2D lines intersect, with an intersection point (x, y)
/// where min <= x, y <= max, using only integer arithmetic in the calculation.
fn intersectInRange(x1: i64, y1: i64, vx1: i64, vy1: i64, x2: i64, y2: i64, vx2: i64, vy2: i64, min_arg: i64, max_arg: i64) bool {
    var det: i128 = vx2 * vy1 - vx1 * vy2;
    if (det == 0) return false; // lines are parallel

    var dx = x2 - x1;
    var dy = y2 - y1;

    var f1: i128 = vx2 * dy - vy2 * dx; // f1/det = position of intersection on first line
    var f2: i128 = vx1 * dy - vy1 * dx; // f2/det = position of intersection on second line
    std.debug.assert(f1 != 0);
    std.debug.assert(f2 != 0);

    if (std.math.sign(f1) != std.math.sign(det)) return false; // collision happened in the past
    if (std.math.sign(f2) != std.math.sign(det)) return false; // collision happened in the past

    // Calculate (xdet, ydet) so that the intersection point (x, y) = (xdet/det, ydet/y).
    const xdet = x1 * det + vx1 * f1;
    const ydet = y1 * det + vy1 * f1;
    std.debug.assert(xdet == x2 * det + vx2 * f2);
    std.debug.assert(ydet == y2 * det + vy2 * f2);

    // Below, we will calculate (min <= xdet/det and xdet/det <= max) as
    // (min*det <= xdet and xdet <= max*det), but this requires that we swap
    // min and max if det is negative:
    var min = if (det > 0) min_arg else max_arg;
    var max = if (det > 0) max_arg else min_arg;

    // Check if the intersection point's coordinates lie between min and max, inclusive.
    return (min * det <= xdet and xdet <= max * det) and
        (min * det <= ydet and ydet <= max * det);
}

fn solvePart1(rays: []const Ray, min: i64, max: i64) !u64 {
    var answer: u64 = 0;
    for (rays, 0..) |r, i| {
        for (rays[i + 1 ..]) |s| {
            if (intersectInRange(r.x, r.y, r.vx, r.vy, s.x, s.y, s.vx, s.vy, min, max)) answer += 1;
        }
    }
    return answer;
}

// We need at least f80 to have enough precision to solve the official input
// exactly. f128 works too, but is likely to be slower, especially since it's
// rarely supported by hardware.
const FloatT = f80;

// Solves a system of linear equations in augmented matrix form using
// Gauss-Jordan elimination.
fn solveMatrix(comptime N: usize, matrix: *[N][N + 1]FloatT) ![N]FloatT {
    for (0..N) |i| {
        // Find a row that's nonzero in column i, and swap it with row i.
        {
            var j = i;
            while (j < N and matrix[j][i] == 0) j += 1;
            if (j == N) return error.MultipleSolutions;
            if (i != j) std.mem.swap([N + 1]FloatT, &matrix[i], &matrix[j]);
        }

        // Normalize row i so it is matrix[i][i] = 1.
        {
            var x = matrix[i][i];
            matrix[i][i] = 1;
            // Note: instead of dividing by x, we could also precalculate 1/x
            // and then multiply by that, which is faster but less precise.
            for (i + 1..N + 1) |c| matrix[i][c] /= x;
        }

        // Subtract row i from other rows until matrix[r][i] = 0 for all r ≠ i.
        for (0..N) |r| if (r != i) {
            var x = matrix[r][i];
            if (x == 0) continue;
            for (i..N + 1) |c| matrix[r][c] -= x * matrix[i][c];
        };
    }

    // The values for the variables are in the last column of the matrix.
    var values: [N]FloatT = undefined;
    for (&values, matrix) |*v, m| v.* = m[N];
    return values;
}

// Since my integer-only Python solution is too much work to port to Zig,
// I just stole this approach from:
// https://github.com/bakkerjangert/AoC_2023/blob/fcc44a084d6b433049fcd6359681703d5abc1674/Day%2024/Day%2024.py#L72-L126
//
// Note it's not needed to shift the coordinates to increase precision when
// using a sufficiently wide floating point format.
fn solvePart2(rays: []const Ray) !i64 {
    var matrix_xy: [4][5]FloatT = undefined;
    var matrix_xz: [4][5]FloatT = undefined;
    for (&matrix_xy, &matrix_xz, 0..) |*row_xy, *row_xz, i| {
        const j = i + 1;
        row_xy[0] = @floatFromInt(rays[j].vy - rays[i].vy);
        row_xz[0] = @floatFromInt(rays[j].vz - rays[i].vz);
        row_xy[1] = @floatFromInt(rays[i].vx - rays[j].vx);
        row_xz[1] = @floatFromInt(rays[i].vx - rays[j].vx);
        row_xy[2] = @floatFromInt(rays[i].y - rays[j].y);
        row_xz[2] = @floatFromInt(rays[i].z - rays[j].z);
        row_xy[3] = @floatFromInt(rays[j].x - rays[i].x);
        row_xz[3] = @floatFromInt(rays[j].x - rays[i].x);
        row_xy[4] = @floatFromInt(rays[i].y * rays[i].vx - rays[i].x * rays[i].vy - rays[j].y * rays[j].vx + rays[j].x * rays[j].vy);
        row_xz[4] = @floatFromInt(rays[i].z * rays[i].vx - rays[i].x * rays[i].vz - rays[j].z * rays[j].vx + rays[j].x * rays[j].vz);
    }
    const x_y_vx_vy = try solveMatrix(4, &matrix_xy);
    const x_z_vx_vz = try solveMatrix(4, &matrix_xz);
    const x = x_y_vx_vy[0];
    const y = x_y_vx_vy[1];
    const z = x_z_vx_vz[1];
    return @intFromFloat(@round(x + y + z));
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    const rays = try env.parseInputAlloc([]Ray, parseInput, allocator);
    defer allocator.free(rays);

    const min = 200_000_000_000_000;
    const max = 400_000_000_000_000;
    try env.setAnswer1(try solvePart1(rays, min, max));
    try env.setAnswer2(try solvePart2(rays));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    const expectEqual = @import("parsing/testing.zig").expectEqual;

    const rays = try parseInput(std.testing.allocator,
        \\19, 13, 30 @ -2, 1, -2
        \\18, 19, 22 @ -1, -1, -2
        \\20, 25, 34 @ -2, -2, -4
        \\12, 31, 28 @ -1, -2, -1
        \\20, 19, 15 @ 1, -5, -3
        \\
    );
    defer std.testing.allocator.free(rays);

    try expectEqual(rays.len, 5);
    try expectEqual(rays[0], Ray{ .x = 19, .y = 13, .z = 30, .vx = -2, .vy = 1, .vz = -2 });
    try expectEqual(rays[4], Ray{ .x = 20, .y = 19, .z = 15, .vx = 1, .vy = -5, .vz = -3 });

    try expectEqual(try solvePart1(rays, 7, 27), 2);

    try expectEqual(try solvePart2(rays), 47);
}
