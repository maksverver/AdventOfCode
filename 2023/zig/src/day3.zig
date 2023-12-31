const Environment = @import("framework/Environment.zig");
const Scanner = @import("parsing/Scanner.zig");
const Grid = @import("parsing/Grid.zig");
const std = @import("std");

// Represents a symbol adjacent to a number. (row, col) is the location of
// the symbol in the grid, and `number` is the adjacent number. If a symbol
// is adjacent to multiple numbers, then we store a Symbol entry for each
// number.
const Symbol = struct {
    ch: *const u8,
    number: isize = 0,
};

fn symbolLessThan(_: void, a: Symbol, b: Symbol) bool {
    return @intFromPtr(a.ch) < @intFromPtr(b.ch);
}

const isDigit = std.ascii.isDigit;

fn isSymbol(c: u8) bool {
    return c != '.' and !isDigit(c);
}

fn detectSymbol(grid: *const Grid, symbols: *std.ArrayList(Symbol), r: isize, c: isize) !void {
    if (grid.inBounds(r, c)) {
        var ch = grid.charPtrAt(r, c);
        if (isSymbol(ch.*)) try symbols.append(Symbol{ .ch = ch });
    }
}

// Part 1. Identify the sum of all numbers that are adjacent to a symbol, where
// a symbol is any character that is not a '.' or a digit.
//
// This code also builds up a list of symbols adjacent to numbers for part 2.
fn solvePart1(grid: *const Grid, symbols: *std.ArrayList(Symbol)) !isize {
    var answer: isize = 0;
    var r: isize = 0;
    while (r < grid.height) : (r += 1) {
        var c: isize = 0;
        while (c < grid.width) : (c += 1) {
            std.debug.assert(!std.ascii.isWhitespace(grid.charAt(r, c)));
            if (std.ascii.isDigit(grid.charAt(r, c))) {
                var number: isize = 0;
                const oldSymbolsLen = symbols.items.len;
                try detectSymbol(grid, symbols, r - 1, c - 1);
                try detectSymbol(grid, symbols, r + 0, c - 1);
                try detectSymbol(grid, symbols, r + 1, c - 1);
                while (c < grid.width) : (c += 1) {
                    const ch = grid.charAt(r, c);
                    if (!isDigit(ch)) break;
                    number = 10 * number + (ch - '0');
                    try detectSymbol(grid, symbols, r - 1, c);
                    try detectSymbol(grid, symbols, r + 1, c);
                }
                try detectSymbol(grid, symbols, r - 1, c);
                try detectSymbol(grid, symbols, r + 0, c);
                try detectSymbol(grid, symbols, r + 1, c);
                if (oldSymbolsLen < symbols.items.len) {
                    // This number is adjacent to one or more symbols
                    answer += number;

                    // Record the number for the adjacent symbols
                    for (oldSymbolsLen..symbols.items.len) |i| {
                        symbols.items[i].number = number;
                    }
                }
            }
        }
    }
    return answer;
}

// Part 2: for all '*' symbols that are adjacent to exactly 2 numbers, calculate
// the product of those 2 numbers, and finally the sum of those products.
fn solvePart2(symbols: []Symbol) isize {
    std.mem.sort(Symbol, symbols, {}, symbolLessThan);
    var answer: isize = 0;
    var i: usize = 0;
    while (i < symbols.len) {
        var j = i + 1;
        while (j < symbols.len and symbols[i].ch == symbols[j].ch) j += 1;
        if (symbols[i].ch.* == '*' and j - i == 2) {
            answer += symbols[i].number * symbols[i + 1].number;
        }
        i = j;
    }
    return answer;
}

pub fn solve(env: *Environment) !void {
    const grid = try env.parseInput(Grid, Grid.init);

    var symbols = std.ArrayList(Symbol).init(env.getHeapAllocator());
    defer symbols.deinit();

    try env.setAnswer1(try solvePart1(&grid, &symbols));
    try env.setAnswer2(solvePart2(symbols.items));
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\467..114..
        \\...*......
        \\..35..633.
        \\......#...
        \\617*......
        \\.....+.58.
        \\..592.....
        \\......755.
        \\...$.*....
        \\.664.598..
        \\
    , "4361", "467835");
}
