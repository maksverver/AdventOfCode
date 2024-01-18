const Environment = @import("framework/Environment.zig");
const Scanner = @import("util/Scanner.zig");
const std = @import("std");

/// An edge in the graph. Edges are undirected, but in the Ford-Fulkerson
/// algorithm, they can only be used in one direction or the other at a time.
const Edge = struct {
    v: usize,
    w: usize,

    /// `used` is +1 if the edge is used in the forward direction v->w, or -1 if
    /// the edge is used in the backward direction w->v, or 0 if it is unused.
    used: i2 = 0,

    /// Returns the endpoint of the edge other than `u`.
    fn other(edge: Edge, u: usize) usize {
        std.debug.assert(u == edge.v or u == edge.w);
        return if (u == edge.v) edge.w else edge.v;
    }

    /// Returns how often this edge is used in the direction v->w.
    fn getUsed(edge: Edge, v: usize, w: usize) i2 {
        std.debug.assert((v == edge.v and w == edge.w) or (v == edge.w and w == edge.v));
        return if (v == edge.v) edge.used else -edge.used;
    }

    /// Increases the usage of the edge in direction v->w.
    fn incUsed(edge: *Edge, v: usize, w: usize) void {
        std.debug.assert((v == edge.v and w == edge.w) or (v == edge.w and w == edge.v));
        edge.used += if (v == edge.v) 1 else -1;
    }
};

const Graph = struct {
    /// List of edges in the graph.
    edges: []Edge,

    /// For each vertex v, adj[v] is a slice of pointers to edges adjacent to v.
    adj: [][]*Edge,

    fn deinit(graph: Graph, allocator: std.mem.Allocator) void {
        for (graph.adj) |a| allocator.free(a);
        allocator.free(graph.adj);
        allocator.free(graph.edges);
    }
};

const GraphBuilder = struct {
    vertex_count: usize = 0,
    _edges_list: std.ArrayListUnmanaged(Edge) = .{},
    _vertex_by_name: std.StringHashMapUnmanaged(usize) = .{},
    allocator: std.mem.Allocator,

    fn init(allocator: std.mem.Allocator) GraphBuilder {
        return GraphBuilder{ .allocator = allocator };
    }

    fn deinit(self: *GraphBuilder) void {
        self._vertex_by_name.deinit(self.allocator);
        self._edges_list.deinit(self.allocator);
    }

    fn getVertexId(self: *GraphBuilder, name: []const u8) !usize {
        var res = try self._vertex_by_name.getOrPut(self.allocator, name);
        if (!res.found_existing) {
            res.value_ptr.* = self.vertex_count;
            self.vertex_count += 1;
        }
        return res.value_ptr.*;
    }

    fn addEdge(self: *GraphBuilder, v: usize, w: usize) !void {
        return self._edges_list.append(self.allocator, Edge{ .v = v, .w = w });
    }

    // Should be called at most once!
    fn build(self: *GraphBuilder) !Graph {
        // Convert to adjacency lists. This is a lot more complicated than it
        // would be when using the arena allocator!
        const allocator = self.allocator;
        var adj_lists = try self.allocator.alloc(std.ArrayListUnmanaged(*Edge), self.vertex_count);
        defer self.allocator.free(adj_lists);
        @memset(adj_lists, std.ArrayListUnmanaged(*Edge){});
        defer for (adj_lists) |*list| list.deinit(allocator);
        for (self._edges_list.items) |*e| {
            try adj_lists[e.v].append(allocator, e);
            try adj_lists[e.w].append(allocator, e);
        }
        var adj_list = try std.ArrayListUnmanaged([]*Edge).initCapacity(allocator, self.vertex_count);
        defer adj_list.deinit(allocator);
        defer for (adj_list.items) |slice| allocator.free(slice);
        for (adj_lists) |*list| {
            const slice = try list.toOwnedSlice(allocator);
            errdefer allocator.free(slice);
            try adj_list.append(allocator, slice);
        }
        return Graph{
            .edges = try self._edges_list.toOwnedSlice(allocator),
            .adj = try adj_list.toOwnedSlice(allocator),
        };
    }
};

fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Graph {
    var graph_builder = GraphBuilder.init(allocator);
    defer graph_builder.deinit();
    var scanner = Scanner.init(input);
    while (!scanner.isEmpty()) {
        const src = try scanner.scanAlphabetic();
        try scanner.skipText(": ");
        const v = try graph_builder.getVertexId(src);
        while (scanner.peekNewline().len == 0) {
            var dst = try scanner.scanAlphabetic();
            scanner.skipHorizontalSpace();
            const w = try graph_builder.getVertexId(dst);
            std.debug.assert(v != w);
            try graph_builder.addEdge(v, w);
        }
        try scanner.skipNewline();
    }
    if (graph_builder.vertex_count == 0) return error.InvalidInput;
    return graph_builder.build();
}

// Uses depth-first search to find an augmenting path from `v` to `finish`, and
// returns true if a path was found (in which case the graph is updated to mark
// the edges that were used), or false if no path remains in the residual graph.
fn augment(adj: []const []*Edge, v: usize, finish: usize, visited: []bool) bool {
    if (v == finish) return true;
    visited[v] = true;
    for (adj[v]) |edge| {
        const w = edge.other(v);
        if (!visited[w] and edge.getUsed(v, w) < 1 and augment(adj, w, finish, visited)) {
            edge.incUsed(v, w);
            return true;
        }
    }
    return false;
}

// Uses depth-first search to count the number of vertices reachable in the
// residual graph, which is the size of the component on one side of the cut.
fn countReachable(adj: []const []*Edge, v: usize, visited: []bool) usize {
    var res: usize = 1;
    visited[v] = true;
    for (adj[v]) |edge| {
        const w = edge.other(v);
        if (!visited[w] and edge.getUsed(v, w) < 1) {
            res += countReachable(adj, w, visited);
        }
    }
    return res;
}

pub fn solve(env: *Environment) !void {
    const allocator = env.getArenaAllocator();
    const graph = try env.parseInputAlloc(Graph, parseInput, allocator);
    defer graph.deinit(allocator);
    const vertices = graph.adj.len;

    const visited = try allocator.alloc(bool, vertices);
    defer allocator.free(visited);

    // We will use the Ford-Fulkerson method to find the minimum cut in the
    // graph. Since the graph is undirected, we need to know two vertices (start
    // and finish) on opposite sides of the cut. We will use vertex 0 as the
    // start, and iterate over the remaining vertices in pseudo-random order.
    //
    // The overall algorithm takes time O(VE), but if we assume the components
    // on both sides of the cut have approximately equal size, the expected
    // runtime is O(E) instead. See ../25.py for a detailed complexity analysis.
    const random_prime = 31337;
    std.debug.assert(std.math.gcd(vertices, random_prime) == 1);
    const start: usize = 0;
    for (1..vertices) |i| {
        const finish = random_prime * i % vertices; // pseudo-randomization

        // Determine the minimum cut between start and finish, using the
        // Ford-Fulkerson method of finding augmenting paths.
        var min_cut: usize = 0;
        while (min_cut <= 3) : (min_cut += 1) {
            @memset(visited, false);
            if (!augment(graph.adj, start, finish, visited)) break;
        }
        if (min_cut < 3) {
            // Cut with fewer than 3 edges found. This should be impossible.
            return error.InvalidInput;
        }
        if (min_cut > 3) {
            // Cut with more than 3 edges found. This means we didn't pick the
            // right (start, finish) pair. Reset the edges before trying again.
            for (graph.edges) |*e| e.used = 0;
        } else {
            // Solution found! Calculate the sizes of the components.
            @memset(visited, false);
            const a = countReachable(graph.adj, start, visited);
            const b = vertices - a;
            return env.setAnswer1(a * b);
        }
    }
    // No cut of size 3 found. This should be impossible.
    return error.InvalidInput;
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\jqt: rhn xhk nvd
        \\rsh: frs pzl lsr
        \\xhk: hfx
        \\cmg: qnr nvd lhk bvb
        \\rhn: xhk bvb hfx
        \\bvb: xhk hfx
        \\pzl: lsr hfx nvd
        \\qnr: nvd
        \\ntq: jqt hfx bvb xhk
        \\nvd: lhk
        \\lsr: lhk
        \\rzs: qnr cmg lsr rsh
        \\frs: qnr lhk lsr
        \\
    , "54", null);
}
