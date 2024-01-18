const Environment = @import("framework/Environment.zig");
const Scanner = @import("util/Scanner.zig");
const std = @import("std");

const Dir = enum { r, d, l, u };

// Answer type. 64 bits is enough for the official input.
const IAnswer = i64;
const UAnswer = u64;

// This solution uses a similar approach as for Day 10; see comments there.
const Solver = struct {
    row: IAnswer = 0,
    area: IAnswer = 0,
    perimeter: UAnswer = 0,

    fn move(self: *Solver, dir: Dir, steps: UAnswer) void {
        const i = @as(isize, @intCast(steps));
        switch (dir) {
            .u => self.row -= i,
            .d => self.row += i,
            .r => self.area += self.row * i,
            .l => self.area -= self.row * i,
        }
        self.perimeter += steps;
    }

    fn getAnswer(self: *const Solver) UAnswer {
        std.debug.assert(self.row == 0);
        return std.math.absCast(self.area) + self.perimeter / 2 + 1;
    }
};

pub fn solve(env: *Environment) !void {
    var scanner = Scanner.init(env.getInput());
    var solver1 = Solver{};
    var solver2 = Solver{};
    while (!scanner.isEmpty()) {
        // Parse input line of the form: "R 6 (#70c710)\n"
        const dirToken = try scanner.scanAlphabetic();
        scanner.skipHorizontalSpace();
        const steps1 = try scanner.scanInt(usize);
        scanner.skipHorizontalSpace();
        try scanner.skipText("(#");
        const rgb = try scanner.scanIntBase(u24, 16);
        try scanner.skipText(")");
        try scanner.skipNewline();

        // Part 1
        if (dirToken.len != 1) return error.InvalidInput;
        const dir1: Dir = switch (dirToken[0]) {
            'R' => .r,
            'D' => .d,
            'L' => .l,
            'U' => .u,
            else => return error.InvalidInput,
        };
        solver1.move(dir1, steps1);

        // Part2
        if (rgb % 16 >= 4) return error.InvalidInput;
        const dir2: Dir = @enumFromInt(rgb % 16);
        const steps2 = rgb / 16;
        solver2.move(dir2, steps2);
    }
    try env.setAnswers(solver1.getAnswer(), solver2.getAnswer());
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\R 6 (#70c710)
        \\D 5 (#0dc571)
        \\L 2 (#5713f0)
        \\D 2 (#d2c081)
        \\R 2 (#59c680)
        \\D 2 (#411b91)
        \\L 5 (#8ceee2)
        \\U 2 (#caa173)
        \\L 1 (#1b58a2)
        \\U 2 (#caa171)
        \\R 2 (#7807d2)
        \\U 3 (#a77fa3)
        \\L 2 (#015232)
        \\U 2 (#7a21e3)
        \\
    , "62", "952408144115");
}
