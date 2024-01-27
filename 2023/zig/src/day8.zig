const Environment = @import("framework/Environment.zig");
const Scanner = @import("util/Scanner.zig");
const scanning = @import("util/scanning.zig");
const std = @import("std");

const Instruction = enum(u8) { L, R };

const Part = enum { Part1, Part2 };

// Integer large enough to store the length of all cycles and their LCM.
const Answer = u64;

// Special value that means “no vertex” (used to detect uninitialized edges).
const no_vertex = std.math.maxInt(usize);

const Vertex = struct {
    name: []const u8, // unowned (and not actually used except for debugging)
    edges: [2]usize, // left, right
    start2: bool,
    finish2: bool,

    fn fromName(name: []const u8) Vertex {
        return Vertex{
            .name = name,
            .edges = [2]usize{ no_vertex, no_vertex },
            .start2 = name[name.len - 1] == 'A',
            .finish2 = name[name.len - 1] == 'Z',
        };
    }

    fn setEdges(self: *Vertex, l: usize, r: usize) void {
        std.debug.assert(self.edges[0] == no_vertex);
        std.debug.assert(self.edges[1] == no_vertex);
        self.edges = [2]usize{ l, r };
    }
};

const Input = struct {
    instructions: []const Instruction,
    vertices: []const Vertex,
    start1: ?usize,
    finish1: ?usize,
    allocator: std.mem.Allocator,

    fn deinit(self: Input) void {
        self.allocator.free(self.instructions);
        self.allocator.free(self.vertices);
    }
};

const GraphBuilder = struct {
    vertex_ids: std.StringHashMap(usize), // name -> index in vertices.items
    vertices: std.ArrayList(Vertex),

    fn init(allocator: std.mem.Allocator) GraphBuilder {
        return .{
            .vertex_ids = std.StringHashMap(usize).init(allocator),
            .vertices = std.ArrayList(Vertex).init(allocator),
        };
    }

    fn getVertexId(self: *GraphBuilder, name: []const u8) !usize {
        const result = try self.vertex_ids.getOrPut(name);
        if (result.found_existing) return result.value_ptr.*;
        errdefer _ = self.vertex_ids.remove(name);
        const id = self.vertices.items.len;
        try self.vertices.append(Vertex.fromName(name));
        result.value_ptr.* = id;
        return id;
    }

    fn addVertex(self: *GraphBuilder, name: []const u8, left: []const u8, right: []const u8) !void {
        const v = try self.getVertexId(name);
        const l = try self.getVertexId(left);
        const r = try self.getVertexId(right);
        self.vertices.items[v].setEdges(l, r);
    }

    fn deinit(self: *GraphBuilder) void {
        self.vertex_ids.deinit();
        self.vertices.deinit();
    }
};

fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Input {
    var scanner = Scanner.init(input);

    // Parse first line: a sequence of instructions ('L' or 'R')
    const firstLine = try scanner.scan(scanning.alphabetic);
    try scanner.skipNewline();
    const instructions = try allocator.alloc(Instruction, firstLine.len);
    errdefer allocator.free(instructions);
    for (instructions, firstLine) |*i, ch| {
        switch (ch) {
            'L' => i.* = .L,
            'R' => i.* = .R,
            else => return error.InvalidInput,
        }
    }

    // Skip blank line seperator
    try scanner.skipNewline();

    // Parse graph description.
    //
    // Each line describes a vertex and is formatted like "ABC = (DEF, GHI)\n",
    // which describes vertex ABC with edges to DEF (left) and GHI (right).
    var builder = GraphBuilder.init(allocator);
    defer builder.deinit();
    while (!scanner.isEmpty()) {
        const name = try scanner.scan(scanning.alphanumeric);
        try scanner.skipText(" = (");
        const left = try scanner.scan(scanning.alphanumeric);
        try scanner.skipText(", ");
        const right = try scanner.scan(scanning.alphanumeric);
        try scanner.skipText(")\n");
        try builder.addVertex(name, left, right);
    }
    return Input{
        .instructions = instructions,
        .vertices = try builder.vertices.toOwnedSlice(),
        .start1 = builder.vertex_ids.get("AAA"),
        .finish1 = builder.vertex_ids.get("ZZZ"),
        .allocator = allocator,
    };
}

const State = struct {
    is: []const Instruction,
    vs: []const Vertex,
    i: usize, // current index (0 <= i < instructions.len)
    v: usize, // current vertex (0 <= v < vertices.len)

    fn init(input: Input, v: usize) State {
        return State{
            .is = input.instructions,
            .vs = input.vertices,
            .i = 0,
            .v = v,
        };
    }

    fn step(s: *State) void {
        s.v = s.vs[s.v].edges[@intFromEnum(s.is[s.i])];
        s.i += 1;
        if (s.i == s.is.len) s.i = 0;
    }
};

fn solvePart1(input: Input) ?Answer {
    // Annoyingly, one of the example inputs has no start/finish for part 1,
    // so we have to make the answer optional.
    const start = input.start1 orelse return null;
    const finish = input.finish1 orelse return null;

    // Now just simulate until we reach the end state.
    var state = State.init(input, start);
    var steps: Answer = 0;
    while (state.v != finish) : (steps += 1) state.step();
    return steps;
}

// Fast version. This blatantly assumes that the cycle period is equal to the
// distance from start to finish, which happens to be true for the official
// input.
fn findCycleFast(input: Input, start: usize) Answer {
    var a: State = State.init(input, start);
    var n: Answer = 0;
    while (!input.vertices[a.v].finish2) : (n += 1) a.step();
    return n;
}

// Slower version which properly detects the cycle using a cycle finding
// algorithm, and verifies that the offset is 0.
//
// https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare
fn findCycleRobust(input: Input, start: usize) ?Answer {
    var a: State = State.init(input, start);
    var b = a;
    a.step();
    b.step();
    b.step();
    var n: Answer = 1;
    while (!(a.v == b.v and input.vertices[a.v].finish2)) : (n += 1) {
        a.step();
        b.step();
        b.step();
    }
    // Verify that cycle starts at offset 0.
    a.step();
    b.step();
    b.step();
    var m = n + 1;
    while (!(a.v == b.v and input.vertices[a.v].finish2)) : (m += 1) {
        a.step();
        b.step();
        b.step();
    }
    if (m != 2 * n) return null; // offset is not 0
    return n;
}

fn findCycle(input: Input, start: usize) ?Answer {
    if (std.debug.runtime_safety) {
        return findCycleRobust(input, start);
    } else {
        return findCycleFast(input, start);
    }
}

// For part 2, this solution makes some assumptions about the properties of the
// input data: that each ghost is in an independent cycle with offset 0, so we
// only need to calculate the least common multiple of individual cycle lengths.

fn solvePart2(input: Input) ?Answer {
    var answer: Answer = 1;
    for (input.vertices, 0..) |vertex, id| if (vertex.start2) {
        const period = findCycle(input, id) orelse return null;
        answer = answer * period / std.math.gcd(answer, period);
    };
    return answer;
}

pub fn solve(env: *Environment) !void {
    const input = try env.parseInputHeap(Input, parseInput);
    defer input.deinit();

    if (solvePart1(input)) |answer| try env.setAnswer1(answer);
    if (solvePart2(input)) |answer| try env.setAnswer2(answer);
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example 1" {
    try @import("framework/testing.zig").testSolver(solve,
        \\RL
        \\
        \\AAA = (BBB, CCC)
        \\BBB = (DDD, EEE)
        \\CCC = (ZZZ, GGG)
        \\DDD = (DDD, DDD)
        \\EEE = (EEE, EEE)
        \\GGG = (GGG, GGG)
        \\ZZZ = (ZZZ, ZZZ)
        \\
    , "2", null);
}

test "example 2" {
    try @import("framework/testing.zig").testSolver(solve,
        \\LLR
        \\
        \\AAA = (BBB, BBB)
        \\BBB = (AAA, ZZZ)
        \\ZZZ = (ZZZ, ZZZ)
        \\
    , "6", null);
}

test "example 3" {
    try @import("framework/testing.zig").testSolver(solve,
        \\LR
        \\
        \\11A = (11B, XXX)
        \\11B = (XXX, 11Z)
        \\11Z = (11B, XXX)
        \\22A = (22B, XXX)
        \\22B = (22C, 22C)
        \\22C = (22Z, 22Z)
        \\22Z = (22B, 22B)
        \\XXX = (XXX, XXX)
        \\
    , null, "6");
}
