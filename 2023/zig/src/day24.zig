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

fn solvePart1(rays: []const Ray) !u64 {
    var answer: u64 = 0;
    for (rays, 0..) |r, i| {
        for (rays[i + 1 ..]) |s| {
            const min = 200_000_000_000_000;
            const max = 400_000_000_000_000;
            if (intersectInRange(r.x, r.y, r.vx, r.vy, s.x, s.y, s.vx, s.vy, min, max)) answer += 1;
        }
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getHeapAllocator();
    const rays = try env.parseInputAlloc([]Ray, parseInput, allocator);
    defer allocator.free(rays);

    try env.setAnswer1(try solvePart1(rays));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}
