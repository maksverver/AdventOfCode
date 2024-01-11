const Environment = @import("framework/Environment.zig");
const text = @import("parsing/text.zig");
const std = @import("std");

const Signal = enum { low, high };

// For conjunctions, the remembered state is represented as a bitmask where
// 1 represents low and 0 represents hi, so that it emits a low pulse when the
// bitmask is 0.
const max_inputs = 16;
const ConjunctionType = std.meta.Int(.unsigned, max_inputs);

fn initConjunction(num_inputs: usize) ConjunctionType {
    std.debug.assert(num_inputs <= max_inputs);
    // Is there a better way to do this?
    if (num_inputs < max_inputs) {
        return (@as(ConjunctionType, 1) << @intCast(num_inputs)) - 1;
    } else {
        return ~@as(ConjunctionType, 0);
    }
}

const ModuleType = enum { sink, broadcaster, flipflop, conjunction };

const ModuleState = union(ModuleType) {
    sink: void,
    broadcaster: void,
    flipflop: bool,
    conjunction: ConjunctionType,
};

const Module = struct {
    name: []const u8, // unused; remove?
    inputs: []const usize,
    outputs: []const usize,
    state: ModuleState = .sink,

    fn init(name: []const u8, inputs: []const usize, outputs: []const usize, typ_: ModuleType) Module {
        return .{
            .name = name,
            .inputs = inputs,
            .outputs = outputs,
            .state = switch (typ_) {
                .sink => .{ .sink = {} },
                .broadcaster => .{ .broadcaster = {} },
                .flipflop => .{ .flipflop = false },
                .conjunction => .{ .conjunction = initConjunction(inputs.len) },
            },
        };
    }

    // unused; remove?
    fn reset(self: *Module) void {
        self.* = Module.init(self.inputs, self.outputs, self.state);
    }

    fn process(self: *Module, source: usize, signal: Signal) ?Signal {
        switch (self.state) {
            .sink => return null,
            .broadcaster => return signal,
            .flipflop => |*state| switch (signal) {
                .high => return null,
                .low => {
                    state.* = !state.*;
                    return if (state.* == false) .low else .high;
                },
            },
            .conjunction => |*state| {
                const idx = std.mem.indexOfScalar(usize, self.inputs, source).?;
                const bit = @as(ConjunctionType, 1) << @intCast(idx);
                switch (signal) {
                    .low => state.* |= bit,
                    .high => state.* &= ~bit,
                }
                return if (state.* == 0) .low else .high;
            },
        }
    }
};

const Graph = struct {
    modules: []Module,
    broadcaster: usize,
    rx: ?usize,

    // unused; remove?
    fn reset(self: *Graph) void {
        for (self.modules) |m| m.reset();
    }
};

// Builds the graph. Note that this assumes we are using the arena allocator,
// so it contains no logic for freeing memory at all!
const GraphBuilder = struct {
    const ModuleDef = struct {
        name: []const u8, // unused, remove?
        typ_: ?ModuleType = null,
        inputs: std.ArrayListUnmanaged(usize) = .{},
        outputs: std.ArrayListUnmanaged(usize) = .{},
    };

    modules: std.ArrayListUnmanaged(ModuleDef) = .{},
    module_index: std.StringHashMapUnmanaged(usize) = .{},
    allocator: std.mem.Allocator,

    fn getModuleIdByName(self: *GraphBuilder, name: []const u8) !usize {
        const res = try self.module_index.getOrPut(self.allocator, name);
        if (!res.found_existing) {
            errdefer _ = self.module_index.remove(name);
            res.value_ptr.* = self.modules.items.len;
            try self.modules.append(self.allocator, ModuleDef{ .name = name });
        }
        return res.value_ptr.*;
    }

    fn createSource(self: *GraphBuilder, label: []const u8) !usize {
        var name: []const u8 = undefined;
        var typ_: ModuleType = undefined;
        if (label[0] == '&') {
            name = label[1..];
            typ_ = .conjunction;
        } else if (label[0] == '%') {
            name = label[1..];
            typ_ = .flipflop;
        } else if (std.mem.eql(u8, label, "broadcaster")) {
            name = label;
            typ_ = ModuleType.broadcaster;
        } else {
            name = label;
            typ_ = ModuleType.sink;
        }
        const id = try self.getModuleIdByName(name);
        var module = &self.modules.items[id];
        std.debug.assert(module.typ_ == null);
        module.typ_ = typ_;
        return id;
    }

    fn addDestination(self: *GraphBuilder, source_id: usize, dest_name: []const u8) !void {
        const dest_id = try self.getModuleIdByName(dest_name);
        var source = &self.modules.items[source_id];
        var dest = &self.modules.items[dest_id];
        try source.outputs.append(self.allocator, dest_id);
        try dest.inputs.append(self.allocator, source_id);
    }

    // Can be called only once!
    fn build(self: *GraphBuilder) !Graph {
        const broadcaster = self.module_index.get("broadcaster") orelse return error.InvalidInput;
        const rx = self.module_index.get("rx"); // missing in examples
        var modules = try self.allocator.alloc(Module, self.modules.items.len);
        for (self.modules.items, modules) |def, *module| {
            module.* = Module.init(def.name, def.inputs.items, def.outputs.items, def.typ_ orelse .sink);
        }
        return Graph{
            .modules = modules,
            .broadcaster = broadcaster,
            .rx = rx,
        };
    }
};

// Parses lines of the form "&hd -> hp, js, hz\n".
fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Graph {
    var builder = GraphBuilder{ .allocator = allocator };
    var line_it = try text.LineIterator.init(input);
    while (line_it.next()) |line| {
        var part_it = std.mem.split(u8, line, " -> ");
        var head = part_it.next() orelse return error.InvalidInput;
        var tail = part_it.next() orelse return error.InvalidInput;
        if (part_it.next()) |_| return error.InvalidInput;
        const source = try builder.createSource(head);
        var dest_it = std.mem.split(u8, tail, ", ");
        while (dest_it.next()) |dest| try builder.addDestination(source, dest);
    }
    return builder.build();
}

const no_module = std.math.maxInt(usize);

const Event = struct {
    source: usize = no_module,
    dest: usize,
    signal: Signal,

    fn debugPrint(elem: @This(), graph: Graph) void {
        std.debug.print("{s} -{s}-> {s}\n", .{
            if (elem.source == no_module) "button" else graph.modules[elem.source].name,
            @tagName(elem.signal),
            graph.modules[elem.dest].name,
        });
    }
};

// Simulates the push of a button (which sends a low signal to the broadcaster),
// then simulates all events until none are left to process.
fn simulate(graph: *Graph, events: *std.ArrayList(Event)) !void {
    events.clearRetainingCapacity();
    var pos: usize = events.items.len;
    try events.append(.{ .signal = .low, .dest = graph.broadcaster });
    while (pos < events.items.len) : (pos += 1) {
        const elem = events.items[pos];
        //elem.debugPrint(graph.*); // uncomment this to show simulation trace
        var module = &graph.modules[elem.dest];
        if (module.process(elem.source, elem.signal)) |s| {
            for (module.outputs) |m| {
                try events.append(.{ .signal = s, .source = elem.dest, .dest = m });
            }
        }
    }
}

// Part 1: count low and high pulses sent in the first 1000 steps.
const Part1Solver = struct {
    low_pulses: u64 = 0,
    high_pulses: u64 = 0,

    fn process(self: *Part1Solver, steps: usize, events: []const Event) ?u64 {
        for (events) |event| switch (event.signal) {
            .low => self.low_pulses += 1,
            .high => self.high_pulses += 1,
        };
        return if (steps == 1000) self.low_pulses * self.high_pulses else null;
    }
};

fn lcm(x: anytype, y: anytype) @TypeOf(x, y) {
    return x * y / std.math.gcd(x, y); // warning: overflow possible!
}

// Part 2: count the number of steps until rx is first called. We need to make
// some assumptions about how the input is constructed and how it behaves (which
// can be inferred from the input drawn as a graph): the `rx` module has a
// single conjunction module as its source, which itself has four sources. Each
// of those sources sends a a high signal periodically with offset 0. Therefore,
// we can calculate the first time all sources send a high signal as the least
// common multiple (LCM) of the invididual periods.
const Part2Solver = struct {
    conjunction_id: usize,
    conjunction_inputs: []const usize,
    unsolved_inputs: ConjunctionType,
    period: u64 = 1,

    fn init(graph: *const Graph) !?Part2Solver {
        if (graph.rx) |rx| {
            const rx_module = &graph.modules[rx];
            if (graph.modules[rx].inputs.len != 1) return error.UnsupportedInput;
            const pre_rx_id = rx_module.inputs[0];
            const pre_rx_module = &graph.modules[pre_rx_id];
            return switch (pre_rx_module.state) {
                .conjunction => |c| .{
                    .conjunction_id = pre_rx_id,
                    .conjunction_inputs = pre_rx_module.inputs,
                    .unsolved_inputs = c,
                },
                else => error.UnsupportedInput,
            };
        } else {
            // Missing rx module (this happens in the example inputs)
            return null;
        }
    }

    fn process(self: *Part2Solver, steps: usize, events: []const Event) ?u64 {
        for (events) |event| if (event.signal == .high and event.dest == self.conjunction_id) {
            const idx = std.mem.indexOfScalar(usize, self.conjunction_inputs, event.source).?;
            const bit = @as(ConjunctionType, 1) << @intCast(idx);
            if ((self.unsolved_inputs & bit) != 0) {
                self.period = self.period * steps / std.math.gcd(self.period, steps);
                self.unsolved_inputs &= ~bit;
                if (self.unsolved_inputs == 0) return self.period;
            }
        };
        return null;
    }
};

pub fn solve(env: *Environment) !void {
    var graph = try env.parseInputArena(Graph, parseInput);

    // Simulate until both answers are solved.
    var solver1: ?Part1Solver = .{};
    var solver2: ?Part2Solver = try Part2Solver.init(&graph);
    var events = std.ArrayList(Event).init(env.getHeapAllocator());
    defer events.deinit();
    var steps: u64 = 0;
    while (solver1 != null or solver2 != null) {
        try simulate(&graph, &events);
        steps += 1;
        if (solver1) |*s| if (s.process(steps, events.items)) |answer| {
            try env.setAnswer1(answer);
            solver1 = null;
        };
        if (solver2) |*s| if (s.process(steps, events.items)) |answer| {
            try env.setAnswer2(answer);
            solver2 = null;
        };
    }
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example 1" {
    try @import("framework/testing.zig").testSolver(solve,
        \\broadcaster -> a, b, c
        \\%a -> b
        \\%b -> c
        \\%c -> inv
        \\&inv -> a
        \\
    , "32000000", null);
}

test "example 2" {
    try @import("framework/testing.zig").testSolver(solve,
        \\broadcaster -> a
        \\%a -> inv, con
        \\&inv -> b
        \\%b -> con
        \\&con -> output
        \\
    , "11687500", null);
}
