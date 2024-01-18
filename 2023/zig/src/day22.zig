const Environment = @import("framework/Environment.zig");
const Scanner = @import("util/Scanner.zig");
const text = @import("util/text.zig");
const std = @import("std");

const Coord = u32;

const Brick = struct {
    x1: Coord,
    y1: Coord,
    z1: Coord,
    x2: Coord,
    y2: Coord,
    z2: Coord,

    fn compareZ1(_: void, a: Brick, b: Brick) bool {
        return a.z1 < b.z1;
    }
};

// The input is converted from a list of bricks to a directed acyclic graph
// (DAG) that describes which bricks rest on top of other bricks. In this DAG
// the index 0 refers to the floor, and the bricks have indices 1 through
// bricks.len (inclusive).
//
// The DAG is an array `supported_by` of type [][]usize, where supported_by[i]
// is a sorted array of distinct indices, such that supported_by[i] contains j
// iff. block i rests directly on block j.
//
// Both parts of the problem can be solved using only this DAG, without needing
// to reference to original list of bricks.
const Input = []const []const usize;

fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Input {
    var line_count = text.countLines(input) orelse return error.InvalidInput;
    var bricks = try allocator.alloc(Brick, line_count);
    defer allocator.free(bricks);

    var i: usize = 0;
    var scanner = Scanner.init(input);
    while (!scanner.isEmpty()) {
        var x1 = try scanner.scanInt(Coord);
        try scanner.skipText(",");
        var y1 = try scanner.scanInt(Coord);
        try scanner.skipText(",");
        var z1 = try scanner.scanInt(Coord);
        try scanner.skipText("~");
        var x2 = try scanner.scanInt(Coord);
        try scanner.skipText(",");
        var y2 = try scanner.scanInt(Coord);
        try scanner.skipText(",");
        var z2 = try scanner.scanInt(Coord);
        try scanner.skipNewline();

        if (x1 > x2) std.mem.swap(Coord, &x1, &x2);
        if (y1 > y2) std.mem.swap(Coord, &y1, &y2);
        if (z1 > z2) std.mem.swap(Coord, &z1, &z2);

        // Sanity check: blocks should extend in at most one dimension (x, y or z).
        if (@as(u2, @intFromBool(x1 != x2)) +
            @as(u2, @intFromBool(y1 != y2)) +
            @as(u2, @intFromBool(z1 != z2)) > 1)
        {
            return error.InvalidInput;
        }

        bricks[i] = .{ .x1 = x1, .y1 = y1, .z1 = z1, .x2 = x2, .y2 = y2, .z2 = z2 };
        i += 1;
    }
    std.debug.assert(i == bricks.len);
    return calculateSupport(allocator, bricks);
}

fn freeInput(allocator: std.mem.Allocator, supported_by: Input) void {
    for (supported_by) |s| allocator.free(s);
    allocator.free(supported_by);
}

fn sortAndDeduplicate(comptime T: type, list: *std.ArrayList(T)) void {
    std.mem.sortUnstable(T, list.items, {}, std.sort.asc(T));
    var j: usize = 0;
    for (0..list.items.len) |i| {
        if (i == 0 or list.items[i] != list.items[i - 1]) {
            list.items[j] = list.items[i];
            j += 1;
        }
    }
    list.shrinkRetainingCapacity(j);
}

// Provides a top-level view of the bricks, recording for each (x, y) coordinate
// the height of the stack and the index of the topmost brick.
const HeightIndex = struct {
    const Elem = struct { h: Coord, i: usize };

    width: usize,
    data: []Elem,
    allocator: std.mem.Allocator,

    fn init(allocator: std.mem.Allocator, bricks: []const Brick) !HeightIndex {
        var depth: Coord = 1; // limit on y coordinates
        var width: Coord = 1; // limit on x coordinates
        for (bricks) |brick| {
            depth = @max(depth, brick.y2 + 1);
            width = @max(width, brick.x2 + 1);
        }
        const data = try allocator.alloc(Elem, depth * width);
        @memset(data, .{ .h = 0, .i = 0 });
        return HeightIndex{ .width = width, .data = data, .allocator = allocator };
    }

    fn deinit(self: *HeightIndex) void {
        self.allocator.free(self.data);
    }

    fn get(self: *const HeightIndex, x: Coord, y: Coord) Elem {
        return self.data[x + y * self.width];
    }

    fn set(self: *HeightIndex, x: Coord, y: Coord, elem: Elem) !void {
        self.data[x + y * self.width] = elem;
    }
};

// Similar functionality ot HeightIndex defined above, but backed by a hash
// table instead. This is more memory efficient for large inputs with sparse
// coordinates, but it is much slower in practice, including for the official
// test data.
const HashHeightIndex = struct {
    const Key = struct { Coord, Coord };
    const Elem = struct { h: Coord, i: usize };
    const floor = Elem{ .h = 0, .i = 0 };

    data: std.AutoHashMap(Key, Elem),

    fn init(allocator: std.mem.Allocator) HashHeightIndex {
        return .{ .data = std.AutoHashMap(Key, Elem).init(allocator) };
    }

    fn deinit(self: *HashHeightIndex) void {
        self.data.deinit();
    }

    fn get(self: *const HashHeightIndex, x: Coord, y: Coord) Elem {
        return self.data.get(.{ x, y }) orelse floor;
    }

    fn set(self: *HashHeightIndex, x: Coord, y: Coord, elem: Elem) !void {
        try self.data.put(.{ x, y }, elem);
    }
};

fn calculateSupport(allocator: std.mem.Allocator, bricks: []Brick) !Input {
    var supported_by = try allocator.alloc([]usize, bricks.len + 1);
    errdefer freeInput(allocator, supported_by);
    supported_by[0] = try allocator.alloc(usize, 0); // floor element

    // Sort bricks from bottom to top.
    std.mem.sortUnstable(Brick, bricks, {}, Brick.compareZ1);

    // For each brick, calculate the set of bricks it is supported by.
    var index = try HeightIndex.init(allocator, bricks);
    //var index = HashHeightIndex.init(allocator);
    defer index.deinit();
    var buf = std.ArrayList(usize).init(allocator);
    defer buf.deinit();
    for (bricks, 1..) |brick, i| {
        buf.clearRetainingCapacity();
        try buf.append(0);
        // Calculate top height for this brick, as the maximum of the heights
        // of the cells on which it rests, plus the brick's own height.
        const new_h = calc: {
            var max_h: Coord = 0;
            var x = brick.x1;
            while (x <= brick.x2) : (x += 1) {
                var y = brick.y1;
                while (y <= brick.y2) : (y += 1) {
                    const elem = index.get(x, y);
                    if (elem.h > max_h) {
                        buf.clearRetainingCapacity();
                        max_h = elem.h;
                    }
                    if (elem.h == max_h) {
                        try buf.append(elem.i);
                    }
                }
            }
            break :calc max_h + (brick.z2 - brick.z1 + 1);
        };
        // Update brick height index
        var x = brick.x1;
        while (x <= brick.x2) : (x += 1) {
            var y = brick.y1;
            while (y <= brick.y2) : (y += 1) {
                try index.set(x, y, .{ .h = new_h, .i = i });
            }
        }
        sortAndDeduplicate(usize, &buf);
        supported_by[i] = try allocator.dupe(usize, buf.items);
    }
    return supported_by;
}

fn solvePart1(allocator: std.mem.Allocator, supported_by: []const []const usize) !usize {
    const safe_to_remove = try allocator.alloc(bool, supported_by.len);
    @memset(safe_to_remove, true);
    defer allocator.free(safe_to_remove);
    for (supported_by[1..]) |s| {
        if (s.len == 1) safe_to_remove[s[0]] = false;
    }
    var answer: usize = 0;
    for (safe_to_remove[1..]) |s| answer += @intFromBool(s);
    return answer;
}

// For each block i, we define parent[i] as the highest single block whose
// removal would cause i to fall (0 if it rests on the floor), and depth[i]
// as the total number of single blocks that would cause block i to fall (i.e.,
// depth[i] = depth[parent[i]] + 1 if parent[i] != 0). Then we can calculate the
// answer as the sum of depths[i] for all i.
fn solvePart2(allocator: std.mem.Allocator, supported_by: []const []const usize) !u64 {
    var depth = try allocator.alloc(usize, supported_by.len);
    defer allocator.free(depth);
    var parent = try allocator.alloc(usize, supported_by.len);
    defer allocator.free(parent);
    depth[0] = 0;
    parent[0] = 0;
    var answer: u64 = 0;
    for (supported_by[1..], 1..) |s, i| {
        // Find the least common ancestor of the blocks that block i rests on.
        // This algorithm runs in O(N) per element of s, but could be optimized
        // to O(log N) using exponential search. For the official test data this
        // isn't necessary.
        std.debug.assert(s.len >= 1);
        var p = s[0];
        for (s[1..]) |j| {
            var q = j;
            while (p != q) {
                if (depth[p] > depth[q]) {
                    p = parent[p];
                } else if (depth[q] > depth[p]) {
                    q = parent[q];
                } else {
                    p = parent[p];
                    q = parent[q];
                }
            }
        }
        parent[i] = p;
        depth[i] = depth[p] + 1;
        answer += depth[i] - 1; // minus 1 to not count the floor
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getArenaAllocator();
    var supported_by = try env.parseInputAlloc(Input, parseInput, allocator);
    defer freeInput(allocator, supported_by);

    try env.setAnswer1(try solvePart1(allocator, supported_by));
    try env.setAnswer2(try solvePart2(allocator, supported_by));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\1,0,1~1,2,1
        \\0,0,2~2,0,2
        \\0,2,3~2,2,3
        \\0,0,4~0,2,4
        \\2,0,5~2,2,5
        \\0,1,6~2,1,6
        \\1,1,8~1,1,9
        \\
    , "5", "7");
}
