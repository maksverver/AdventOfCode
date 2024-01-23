const Environment = @import("framework/Environment.zig");
const grids = @import("util/grids.zig");
const Dir = grids.Dir;
const Coords = grids.Coords;
const Grid = grids.TextGrid;
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

fn detectSymbol(grid: *const Grid, symbols: *std.ArrayList(Symbol), pos: Coords, dr: i2, dc: i2) !void {
    if (grid.moveBy(pos, dr, dc)) |new_pos| {
        const ch = grid.ptrAtPos(new_pos);
        if (isSymbol(ch.*)) try symbols.append(Symbol{ .ch = ch });
    }
}

// Part 1. Identify the sum of all numbers that are adjacent to a symbol, where
// a symbol is any character that is not a '.' or a digit.
//
// This code also builds up a list of symbols adjacent to numbers for part 2.
fn solvePart1(grid: *const Grid, symbols: *std.ArrayList(Symbol)) !isize {
    var answer: isize = 0;
    var pos = Coords{ .r = 0, .c = undefined };
    while (pos.r < grid.height) : (pos.r += 1) {
        pos.c = 0;
        while (pos.c < grid.width) : (pos.c += 1) {
            std.debug.assert(!std.ascii.isWhitespace(grid.atPos(pos)));
            if (std.ascii.isDigit(grid.atPos(pos))) {
                var number: isize = 0;
                const oldSymbolsLen = symbols.items.len;
                try detectSymbol(grid, symbols, pos, -1, -1);
                try detectSymbol(grid, symbols, pos, 0, -1);
                try detectSymbol(grid, symbols, pos, 1, -1);
                while (pos.c < grid.width) : (pos.c += 1) {
                    const ch = grid.atPos(pos);
                    if (!isDigit(ch)) break;
                    number = 10 * number + (ch - '0');
                    try detectSymbol(grid, symbols, pos, -1, 0);
                    try detectSymbol(grid, symbols, pos, 1, 0);
                }
                try detectSymbol(grid, symbols, pos, -1, 0);
                try detectSymbol(grid, symbols, pos, 0, 0);
                try detectSymbol(grid, symbols, pos, 1, 0);
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
    std.mem.sortUnstable(Symbol, symbols, {}, symbolLessThan);
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
    const grid = try env.parseInput(Grid, Grid.initFromText);

    var symbols = std.ArrayList(Symbol).init(env.getHeapAllocator());
    defer symbols.deinit();

    try env.setAnswer1(try solvePart1(&grid, &symbols));
    try env.setAnswer2(solvePart2(symbols.items));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
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
