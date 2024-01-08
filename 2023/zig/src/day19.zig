const Environment = @import("framework/Environment.zig");
const Scanner = @import("parsing/Scanner.zig");
const std = @import("std");

const Field = enum { x, m, a, s };

const State = u32;
const Val = usize;

const Part = std.EnumArray(Field, Val);

const Bounds = std.EnumArray(Field, struct { Val, Val });

// Special state values.
const accepted = 0;
const rejected = 1;
const no_state = std.math.maxInt(State);

// Optimization: pre-allocate elements to reduce allocation overhead.
const rules_capacity = 1000;
const parts_capacity = 1000;

// Each state transition is a quadruple (field, val, lt, ge), which is evaluated
// by comparing the value of `field` to `val`. If it is less, go to state `lt`.
// If it is greater or equal, go to `ge`.
const Transition = struct {
    field: Field = .x,
    val: Val = 0,
    lt: State = no_state,
    ge: State = no_state,

    fn setOtherBranch(self: *Transition, next: State) void {
        if (self.lt == no_state) {
            std.debug.assert(self.ge != no_state);
            self.lt = next;
        } else {
            std.debug.assert(self.ge == no_state);
            self.ge = next;
        }
    }
};

const Input = struct {
    transitions: []Transition,
    start: State,
    parts: []Part,
    allocator: std.mem.Allocator,

    fn deinit(self: Input) void {
        self.allocator.free(self.parts);
        self.allocator.free(self.transitions);
    }
};

// This parses the input into the normalized state transition table, flattening
// rules into a single conditional per state, introducing new dummy states if a
// rule has more than one conditional. For example:
//
//  a{x<10:b,m>20:c,a<30:d,e}
//
// Flattens into:
//
//  a{x<10:b,s}
//  s{m<21:t,c}
//  t{a<30:d,e}
//
// where `s` and `t` are dummy states. Rules without a conditional (e.g., "a{A}")
// are not supported. This is checked in setOtherBranch().
//
const Parser = struct {
    statesByName: std.StringHashMap(State),
    transitions: std.ArrayList(Transition),
    last_state: ?State = null,
    first_branch: bool = false,

    fn init(allocator: std.mem.Allocator) !Parser {
        var statesByName = std.StringHashMap(State).init(allocator);
        errdefer statesByName.deinit();
        try statesByName.ensureTotalCapacity(rules_capacity);
        var transitions = std.ArrayList(Transition).init(allocator);
        errdefer transitions.deinit();
        try transitions.ensureTotalCapacity(rules_capacity);
        try transitions.append(Transition{});
        try transitions.append(Transition{});
        try statesByName.put("A", accepted);
        try statesByName.put("R", rejected);
        return .{
            .statesByName = statesByName,
            .transitions = transitions,
        };
    }

    fn beginRule(self: *Parser, name: []const u8) !void {
        self.last_state = try self.getNamedState(name);
        self.first_branch = true;
    }

    fn addTransition(self: *Parser, transition: Transition) !void {
        if (self.first_branch) {
            self.first_branch = false;
        } else {
            const dst = try self.createState();
            self.transitions.items[self.last_state.?].setOtherBranch(dst);
            self.last_state = dst;
        }
        self.transitions.items[self.last_state.?] = transition;
    }

    fn ifLessThan(self: *Parser, field: Field, val: Val, dest: []const u8) !void {
        try self.addTransition(.{
            .field = field,
            .val = val,
            .lt = try self.getNamedState(dest),
            .ge = no_state,
        });
    }

    fn ifGreaterThan(self: *Parser, field: Field, val: Val, dest: []const u8) !void {
        try self.addTransition(.{
            .field = field,
            .val = val + 1,
            .lt = no_state,
            .ge = try self.getNamedState(dest),
        });
    }

    fn endRule(self: *Parser, dest_name: []const u8) !void {
        const dst = try self.getNamedState(dest_name);
        self.transitions.items[self.last_state.?].setOtherBranch(dst);
        self.last_state = null;
    }

    fn getNamedState(self: *Parser, name: []const u8) !State {
        const entry = try self.statesByName.getOrPut(name);
        if (!entry.found_existing) {
            errdefer _ = self.statesByName.remove(name);
            entry.value_ptr.* = try self.createState();
        }
        return entry.value_ptr.*;
    }

    fn createState(self: *Parser) !State {
        const state: State = @intCast(self.transitions.items.len);
        try self.transitions.append(Transition{});
        return state;
    }

    fn deinit(self: *Parser) void {
        self.transitions.deinit();
        self.statesByName.deinit();
    }
};

fn ok(val: anytype) bool {
    return if (val) |_| true else |_| false;
}

fn parseInput(allocator: std.mem.Allocator, input: []const u8) !Input {
    var scanner = Scanner.init(input);
    // Scan workflows. Each line is of the form "a{x>1:b,m<2:c,d}\n"
    var parser = try Parser.init(allocator);
    defer parser.deinit();
    while (!ok(scanner.skipNewline())) {
        try parser.beginRule(try scanner.scanAlphanumeric());
        try scanner.skipText("{");
        while (true) {
            const token = try scanner.scanAlphanumeric();
            if (ok(scanner.skipText("}"))) {
                try parser.endRule(token);
                break;
            }
            if (token.len != 1) return error.InvalidInput;
            const field: Field = switch (token[0]) {
                'x' => .x,
                'm' => .m,
                'a' => .a,
                's' => .s,
                else => return error.InvalidInput,
            };
            const lt = if (ok(scanner.skipText("<"))) true else if (ok(scanner.skipText(">"))) false else return error.InvalidInput;
            const val = try scanner.scanInt(Val);
            try scanner.skipText(":");
            const dest = try scanner.scanAlphanumeric();
            try scanner.skipText(",");
            if (lt) {
                try parser.ifLessThan(field, val, dest);
            } else {
                try parser.ifGreaterThan(field, val, dest);
            }
        }
        try scanner.skipNewline();
    }

    // Scan parts. Each line is of the form "{x=1,m=2,a=3,s=4}\n"
    var partsList = std.ArrayList(Part).init(allocator);
    defer partsList.deinit();
    try partsList.ensureTotalCapacity(parts_capacity);
    while (!scanner.isEmpty()) {
        var part = Part.initUndefined();
        try scanner.skipText("{x=");
        part.set(.x, try scanner.scanInt(Val));
        try scanner.skipText(",m=");
        part.set(.m, try scanner.scanInt(Val));
        try scanner.skipText(",a=");
        part.set(.a, try scanner.scanInt(Val));
        try scanner.skipText(",s=");
        part.set(.s, try scanner.scanInt(Val));
        try scanner.skipText("}");
        try scanner.skipNewline();
        try partsList.append(part);
    }

    return .{
        .transitions = try parser.transitions.toOwnedSlice(),
        .start = parser.statesByName.get("in") orelse return error.InvalidInput,
        .parts = try partsList.toOwnedSlice(),
        .allocator = allocator,
    };
}

fn isAccepted(input: *const Input, part: Part) bool {
    var state = input.start;
    while (state != accepted and state != rejected) {
        const t = input.transitions[state];
        state = if (part.get(t.field) < t.val) t.lt else t.ge;
    }
    return state == accepted;
}

fn solvePart1(input: *const Input) u64 {
    var answer: u64 = 0;
    for (input.parts) |part| {
        if (isAccepted(input, part)) {
            for (part.values) |v| answer += v;
        }
    }
    return answer;
}

fn countSolutions(input: *const Input, state: State, bounds: Bounds) u64 {
    if (state == rejected) {
        return 0;
    }
    if (state == accepted) {
        var count: u64 = 1;
        for (bounds.values) |b| count *= b[1] - b[0];
        return count;
    }
    const t = input.transitions[state];
    const lo = bounds.get(t.field)[0];
    const hi = bounds.get(t.field)[1];
    if (t.val >= hi) return countSolutions(input, t.lt, bounds);
    if (t.val <= lo) return countSolutions(input, t.ge, bounds);
    var below = bounds;
    below.getPtr(t.field)[1] = t.val;
    var above = bounds;
    above.getPtr(t.field)[0] = t.val;
    return countSolutions(input, t.lt, below) + countSolutions(input, t.ge, above);
}

fn solvePart2(input: *const Input) u64 {
    return countSolutions(input, input.start, Bounds.initFill(.{ 1, 4001 }));
}

pub fn solve(env: *Environment) !void {
    const input = try env.parseInputArena(Input, parseInput);
    defer input.deinit();
    try env.setAnswer1(solvePart1(&input));
    try env.setAnswer2(solvePart2(&input));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\px{a<2006:qkq,m>2090:A,rfg}
        \\pv{a>1716:R,A}
        \\lnx{m>1548:A,A}
        \\rfg{s<537:gd,x>2440:R,A}
        \\qs{s>3448:A,lnx}
        \\qkq{x<1416:A,crn}
        \\crn{x>2662:A,R}
        \\in{s<1351:px,qqz}
        \\qqz{s>2770:qs,m<1801:hdj,R}
        \\gd{a>3333:R,R}
        \\hdj{m>838:A,pv}
        \\
        \\{x=787,m=2655,a=1222,s=2876}
        \\{x=1679,m=44,a=2067,s=496}
        \\{x=2036,m=264,a=79,s=2244}
        \\{x=2461,m=1339,a=466,s=291}
        \\{x=2127,m=1623,a=2188,s=1013}
        \\
    , "19114", "167409079868000");
}
