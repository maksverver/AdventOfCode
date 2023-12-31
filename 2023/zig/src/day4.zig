const Environment = @import("framework/Environment.zig");
const Scanner = @import("parsing/Scanner.zig");
const std = @import("std");

const numbers = 100;
const Numbers = std.bit_set.IntegerBitSet(numbers);

fn scanNumbers(scanner: *Scanner) !Numbers {
    var result: Numbers = Numbers.initEmpty();
    while (scanner.scanInt(usize) catch null) |number| {
        std.debug.assert(0 <= number and number < numbers);
        result.set(number);
        scanner.skipHorizontalSpace();
    }
    return result;
}

const Card = struct {
    num: isize = 0,
    win: Numbers = Numbers.initEmpty(),
    have: Numbers = Numbers.initEmpty(),
    copies: isize = 1,

    fn countWinning(self: *Card) usize {
        return self.win.intersectWith(self.have).count();
    }
};

fn scanCard(scanner: *Scanner) !Card {
    try scanner.skipText("Card");
    scanner.skipHorizontalSpace();
    const num = try scanner.scanInt(isize);
    try scanner.skipText(":");
    scanner.skipHorizontalSpace();
    const win = try scanNumbers(scanner);
    try scanner.skipText("|");
    scanner.skipHorizontalSpace();
    const have = try scanNumbers(scanner);
    try scanner.skipNewline();
    return Card{ .num = num, .win = win, .have = have, .copies = 1 };
}

fn parseCards(allocator: std.mem.Allocator, input: []const u8) ![]Card {
    var cardsList = std.ArrayList(Card).init(allocator);
    errdefer cardsList.deinit();
    var scanner = Scanner{ .text = input };
    errdefer scanner.debugPrintRemainingInput(); // useful for debugging parse errors
    while (!scanner.isEmpty()) {
        try cardsList.append(try scanCard(&scanner));
    }
    return cardsList.toOwnedSlice();
}

pub fn solve(env: *Environment) !void {
    const cards = try env.parseInputArena([]Card, parseCards);
    var answer1: isize = 0;
    var answer2: isize = 0;
    for (cards, 0..) |*card, i| {
        var n = card.countWinning();
        if (n > 0) {
            answer1 += @as(isize, 1) << @intCast(n - 1);
            for (i + 1..i + 1 + n) |j| {
                std.debug.assert(j < cards.len);
                cards[j].copies += card.copies;
            }
        }
        answer2 += card.copies;
    }
    return env.setAnswers(answer1, answer2);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        \\Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        \\Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        \\Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        \\Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        \\Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
        \\
    , "13", "30");
}
