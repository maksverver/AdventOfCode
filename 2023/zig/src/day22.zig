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
// Both parts of the problem can be solved using only this DAG, without needing
// to reference to original list of bricks.
const Input = struct {
    starts: []usize,
    data: []usize,

    fn fromBricks(allocator: std.mem.Allocator, bricks: []Brick) !Input {
        // Sort bricks from bottom to top.
        std.mem.sortUnstable(Brick, bricks, {}, Brick.compareZ1);

        // Alocate `start` array and `data` buffer.
        var starts = try allocator.alloc(usize, bricks.len + 2);
        errdefer allocator.free(starts);
        var buf = std.ArrayList(usize).init(allocator);
        errdefer buf.deinit();

        starts[0] = 0; // floor element

        // For each brick, calculate the set of bricks it is supported by.
        var index = try HeightIndex.init(allocator, bricks);
        //var index = HashHeightIndex.init(allocator);
        defer index.deinit();
        for (bricks, 1..) |brick, i| {
            const start = buf.items.len;
            starts[i] = start;
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
                            buf.shrinkRetainingCapacity(start);
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
            sortAndDeduplicate(usize, &buf, start);
        }
        starts[bricks.len + 1] = buf.items.len;
        return Input{ .starts = starts, .data = try buf.toOwnedSlice() };
    }

    fn deinit(self: Input, allocator: std.mem.Allocator) void {
        allocator.free(self.starts);
        allocator.free(self.data);
    }

    /// Number of bricks, plus 1 for the floor.
    fn brickCount(self: Input) usize {
        return self.starts.len - 1;
    }

    // Returns a slice of distinct block indices j, where i rests directly on j.
    fn supportedBy(self: Input, i: usize) []const usize {
        return self.data[self.starts[i]..self.starts[i + 1]];
    }
};

fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Input {
    const line_count = text.countLines(input) orelse return error.InvalidInput;
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
    return Input.fromBricks(allocator, bricks);
}

fn sortAndDeduplicate(comptime T: type, list: *std.ArrayList(T), pos: usize) void {
    if (pos == list.items.len) return;
    std.mem.sortUnstable(T, list.items[pos..], {}, std.sort.asc(T));
    var i = pos + 1;
    var j = i;
    while (j < list.items.len) : (j += 1) {
        if (list.items[j] != list.items[j - 1]) {
            list.items[i] = list.items[j];
            i += 1;
        }
    }
    list.shrinkRetainingCapacity(i);
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

fn solvePart1(allocator: std.mem.Allocator, input: Input) !usize {
    const safe_to_remove = try allocator.alloc(bool, input.brickCount());
    @memset(safe_to_remove, true);
    defer allocator.free(safe_to_remove);
    for (1..input.brickCount()) |i| {
        const s = input.supportedBy(i);
        if (s.len == 1) safe_to_remove[s[0]] = false;
    }
    var answer: usize = 0;
    for (safe_to_remove[1..]) |s| answer += @intFromBool(s);
    return answer;
}

// Slow implementation of the lowest common ancestor algorithm.
//
// This just stores the parent and depth of each vertex in the tree, and moves
// up one level at a time until a common ancestor is found.
//
// Every call to lca() takes O(V) time worst-case.
const SlowLCA = struct {
    parents: []usize,
    depths: []usize,

    fn init(allocator: std.mem.Allocator, n: usize) !SlowLCA {
        var parents = try allocator.alloc(usize, n);
        errdefer allocator.free(parents);
        var depths = try allocator.alloc(usize, n);
        errdefer allocator.free(depths);
        parents[0] = 0; // floor
        depths[0] = 0; // floor
        return .{ .depths = depths, .parents = parents };
    }

    fn deinit(self: SlowLCA, allocator: std.mem.Allocator) void {
        defer allocator.free(self.depths);
        defer allocator.free(self.parents);
    }

    // Add vertex v with the given parent, and return the depth of v.
    fn addVertex(self: SlowLCA, v: usize, parent: usize) usize {
        self.parents[v] = parent;
        self.depths[v] = self.depths[parent] + 1;
        return self.depths[v];
    }

    fn lca(self: SlowLCA, v_in: usize, w_in: usize) usize {
        var v = v_in;
        var w = w_in;
        while (v != w) {
            if (self.depths[v] > self.depths[w]) {
                v = self.parents[v];
            } else if (self.depths[w] > self.depths[v]) {
                w = self.parents[w];
            } else {
                v = self.parents[v];
                w = self.parents[w];
            }
        }
        return v;
    }
};

// Asymptotically faster implementation of the lowest common ancestor algorithm.
//
// This uses exponential search to find the lowest common ancestor, so that
// each call to lca() takes O(log V) amortized time. It requires allocating
// O(V log V) memory up front.
const FastLCA = struct {
    const no_vertex = std.math.maxInt(usize);

    // ceil(log2(n)) where n is the number of vertices, passed to init().
    log2size: usize,

    // ancestors[v × log2size + k] is the 2^k-th ancestor of v, or 0 if
    // depth[v] ≤ 2^k, or no_vertex if the value has not been computed yet.
    //
    // Specifically, ancestors[v × log2size] is the parent vertex of v.
    //
    // The parent value is assigned by addVertex(). Other values are initialized
    // to no_vertex and computed on-demand by getAncestorPowerOf2().
    ancestors: []usize,

    // depths[v] = the the depth of vertex v in the tree, with the floor
    // (vertex 0) having depth 0.
    depths: []usize,

    fn init(allocator: std.mem.Allocator, n: usize) !FastLCA {
        var log2size = std.math.log2_int(usize, n) + 1;
        var ancestors = try allocator.alloc(usize, log2size * n);
        errdefer allocator.free(ancestors);
        @memset(ancestors, no_vertex);
        var depths = try allocator.alloc(usize, n);
        errdefer allocator.free(depths);
        ancestors[0] = 0; // floor
        depths[0] = 0; // floor
        return .{ .log2size = log2size, .depths = depths, .ancestors = ancestors };
    }

    fn deinit(self: FastLCA, allocator: std.mem.Allocator) void {
        defer allocator.free(self.depths);
        defer allocator.free(self.ancestors);
    }

    // Add vertex v with the given parent, and return the depth of v.
    fn addVertex(self: FastLCA, v: usize, parent: usize) usize {
        self.ancestors[self.log2size * v] = parent;
        self.depths[v] = self.depths[parent] + 1;
        return self.depths[v];
    }

    fn getParent(self: FastLCA, v: usize) usize {
        return self.ancestors[self.log2size * v];
    }

    fn getAncestorPowerOf2(self: FastLCA, v: usize, k: usize) usize {
        std.debug.assert(k < self.log2size);
        var j = k;
        while (self.ancestors[self.log2size * v + j] == no_vertex) j -= 1;
        var a = self.ancestors[self.log2size * v + j];
        while (j < k) : (j += 1) {
            a = self.getAncestorPowerOf2(a, j);
            self.ancestors[self.log2size * v + (j + 1)] = a;
        }
        return a;
    }

    fn getNthAncestor(self: FastLCA, v_in: usize, n: usize) usize {
        var v = v_in;
        var k: usize = 0;
        var bit: usize = 1;
        while (bit <= n) {
            if ((n & bit) != 0) v = self.getAncestorPowerOf2(v, k);
            k += 1;
            bit += bit;
        }
        return v;
    }

    fn lca(self: FastLCA, v_in: usize, w_in: usize) usize {
        var v = v_in;
        var w = w_in;

        var n = self.depths[v];
        var m = self.depths[w];
        if (n > m) v = self.getNthAncestor(v, n - m);
        if (m > n) w = self.getNthAncestor(w, m - n);
        if (v == w) return v;

        var k: usize = 0;
        while (self.getAncestorPowerOf2(v, k) != self.getAncestorPowerOf2(w, k)) {
            k += 1;
        }
        while (k > 0) {
            k -= 1;
            const a = self.getAncestorPowerOf2(v, k);
            const b = self.getAncestorPowerOf2(w, k);
            if (a != b) {
                v = a;
                w = b;
            }
        }
        std.debug.assert(v != w and self.getParent(v) == self.getParent(w));
        return self.getParent(v);
    }
};

// For each block i, we define parent[i] as the highest single block whose
// removal would cause i to fall (0 if it rests on the floor), and depth[i]
// as the total number of single blocks that would cause block i to fall (i.e.,
// depth[i] = depth[parent[i]] + 1 if parent[i] != 0). Then we can calculate the
// answer as the sum of depths[i] for all i.
//
// This algorithm calls the lca method |E| - |V| times, where |V| is the number
// of bricks, and |E| is the number of edges in the graph implied by the
// supported-by relation.
//
// The overall complexity depends on the LCA implementation chosen: O(EV) for
// SlowLCA, or O(E log V) for FastLCA.
fn solvePart2(comptime LCA: type, allocator: std.mem.Allocator, input: Input) !u64 {
    var lca = try LCA.init(allocator, input.brickCount());
    defer lca.deinit(allocator);
    var answer: u64 = 0;
    for (1..input.brickCount()) |i| {
        const s = input.supportedBy(i);
        std.debug.assert(s.len >= 1); // floor is always included
        var p = s[0];
        for (s[1..]) |q| p = lca.lca(p, q);
        answer += lca.addVertex(i, p) - 1; // minus 1 for the floor
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getArenaAllocator();
    const input = try env.parseInputAlloc(Input, parseInput, allocator);
    defer input.deinit(allocator);

    try env.setAnswer1(try solvePart1(allocator, input));

    // For part 2, we can choose between two LCA implementations. FastLCA is
    // asymptotically faster, but slower for the official test data.
    try env.setAnswer2(try solvePart2(SlowLCA, allocator, input));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    const expectEqual = @import("util/testing.zig").expectEqual;
    const allocator = std.testing.allocator;
    const input = try parseInput(allocator,
        \\1,0,1~1,2,1
        \\0,0,2~2,0,2
        \\0,2,3~2,2,3
        \\0,0,4~0,2,4
        \\2,0,5~2,2,5
        \\0,1,6~2,1,6
        \\1,1,8~1,1,9
        \\
    );
    defer input.deinit(allocator);
    try expectEqual(try solvePart1(allocator, input), 5);
    try expectEqual(try solvePart2(SlowLCA, allocator, input), 7);
    try expectEqual(try solvePart2(FastLCA, allocator, input), 7);
}
