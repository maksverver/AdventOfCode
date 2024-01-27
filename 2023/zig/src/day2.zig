const Environment = @import("framework/Environment.zig");
const Scanner = @import("util/Scanner.zig");
const scanning = @import("util/scanning.zig");
const std = @import("std");

pub fn solve(env: *Environment) !void {
    var scanner = Scanner.init(env.getInput());
    var answer1: isize = 0;
    var answer2: isize = 0;
    while (!scanner.isEmpty()) {
        try scanner.skipText("Game ");
        const gameNumber = try scanner.scanInt(isize);
        var max_r: isize = 0;
        var max_g: isize = 0;
        var max_b: isize = 0;
        try scanner.skipText(": ");
        while (true) {
            var r: isize = 0;
            var g: isize = 0;
            var b: isize = 0;
            while (true) {
                const count = try scanner.scanInt(isize);
                std.debug.assert(count >= 0);
                scanner.skipHorizontalSpace();
                const color = try scanner.scan(scanning.alphabetic);
                if (std.mem.eql(u8, color, "red")) {
                    std.debug.assert(r == 0);
                    r = count;
                } else if (std.mem.eql(u8, color, "green")) {
                    std.debug.assert(g == 0);
                    g = count;
                } else if (std.mem.eql(u8, color, "blue")) {
                    std.debug.assert(b == 0);
                    b = count;
                } else {
                    return error.InvalidInput;
                }
                scanner.skipText(", ") catch break;
            }
            max_r = @max(max_r, r);
            max_g = @max(max_g, g);
            max_b = @max(max_b, b);
            scanner.skipText("; ") catch break;
        }
        try scanner.skipNewline();
        if (max_r <= 12 and max_g <= 13 and max_b <= 14) answer1 += gameNumber;
        answer2 += max_r * max_g * max_b;
    }
    return env.setAnswers(answer1, answer2);
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try (@import("framework/testing.zig").testSolver(solve,
        \\Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        \\Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        \\Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        \\Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        \\Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        \\
    , "8", "2286"));
}
