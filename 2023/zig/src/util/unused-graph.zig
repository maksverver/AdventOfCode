const std = @import("std");
const Scanner = @import("./Scanner.zig");

// Compact graph representation using adjacency lists.
const Graph = struct {
    starts: []usize,
    dests: []usize,

    fn deinit(graph: Graph, allocator: std.mem.Allocator) void {
        allocator.free(graph.dests);
        allocator.free(graph.starts);
    }

    fn vertexCount(graph: Graph) usize {
        return graph.starts.len - 1;
    }

    fn edgeCount(graph: Graph) usize {
        return graph.starts[graph.starts.len - 1];
    }

    // Returns slice of vertices adjacent to v.
    fn adj(graph: Graph, v: usize) []const usize {
        return graph.dests[graph.starts[v]..graph.starts[v + 1]];
    }
};

fn getVertexId(vertex_by_name: *std.StringHashMap(usize), vertex_count: *usize, name: []const u8) !usize {
    var res = try vertex_by_name.getOrPut(name);
    if (!res.found_existing) {
        res.value_ptr.* = vertex_count.*;
        vertex_count.* += 1;
    }
    return res.value_ptr.*;
}

// Note: this parses an undirected graph, but expects each edge to occur in the
// input only once! So a single line "a: b c\n" represents a graph with 3
// vertices and 4 edges: (a, b), (a, c), (b, a), (c, a).
fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Graph {
    var vertex_count: usize = 0;

    // Maps strings to vertex ids between 0 and vertex_count.
    var vertex_by_name = std.StringHashMap(usize).init(allocator);
    defer vertex_by_name.deinit();

    // List of edges as vertex pairs.
    var edges = std.ArrayList(struct { usize, usize }).init(allocator);
    defer edges.deinit();

    // Identify all the edges.
    var scanner = Scanner.init(input);
    while (!scanner.isEmpty()) {
        const src = try scanner.scanAlphabetic();
        try scanner.skipText(": ");
        const v = try getVertexId(&vertex_by_name, &vertex_count, src);
        while (scanner.peekNewline().len == 0) {
            var dst = try scanner.scanAlphabetic();
            scanner.skipHorizontalSpace();
            const w = try getVertexId(&vertex_by_name, &vertex_count, dst);
            try edges.append(.{ w, v });
        }
        try scanner.skipNewline();
    }
    if (vertex_count == 0) return error.InvalidInput;

    // Convert edges to adjacency lists.
    var starts = try allocator.alloc(usize, vertex_count + 1);
    errdefer allocator.free(starts);
    @memset(starts, 0);
    var ends = starts[1..];
    for (edges.items) |edge| {
        ends[edge[0]] += 1;
        ends[edge[1]] += 1;
    }
    var edge_count: usize = 0;
    for (0..vertex_count) |v| {
        const start = edge_count;
        edge_count += ends[v];
        ends[v] = start;
    }

    var dests = try allocator.alloc(usize, edge_count);
    errdefer allocator.free(dests);
    for (edges.items) |edge| {
        const v = edge[0];
        const w = edge[1];
        dests[ends[v]] = w;
        dests[ends[w]] = v;
        ends[v] += 1;
        ends[w] += 1;
    }
    return Graph{ .starts = starts, .dests = dests };
}

test {
    const graph = try parseInput(std.testing.allocator,
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
    );
    defer graph.deinit(std.testing.allocator);

    const expectEqual = @import("./testing.zig").expectEqual;

    try expectEqual(graph.vertexCount(), 15);
    try expectEqual(graph.edgeCount(), 66);
    try expectEqual(graph.adj(0).len, 4);
    try expectEqual(graph.adj(0)[0], 1);
    try expectEqual(graph.adj(0)[1], 2);
    try expectEqual(graph.adj(0)[2], 3);
    try expectEqual(graph.adj(0)[3], 13);
}
