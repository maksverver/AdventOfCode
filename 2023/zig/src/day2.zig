const Scanner = @import("parsing/scanning.zig").Scanner;
const std = @import("std");

pub fn solve(_: std.mem.Allocator, input: []const u8) !void {
    var scanner = Scanner{ .text = input };
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
                var count = try scanner.scanInt(isize);
                std.debug.assert(count >= 0);
                scanner.skipHorizontalSpace();
                var color = try scanner.scanAlphabetic();
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
    std.debug.print("{}\n{}\n", .{ answer1, answer2 });
}
