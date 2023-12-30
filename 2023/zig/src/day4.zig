const Scanner = @import("parsing/scanning.zig").Scanner;
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

pub fn solve(allocator: std.mem.Allocator, input: []const u8) !void {
    const cards = try parseCards(allocator, input);
    defer allocator.free(cards);
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
    std.debug.print("{}\n{}\n", .{ answer1, answer2 });
}
