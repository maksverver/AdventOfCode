const Environment = @import("framework/Environment.zig");
const Scanner = @import("parsing/Scanner.zig");
const std = @import("std");

const order = "23456789TJQKA";
const num_values = order.len + 1;

fn cardValue(ch: u8) !u8 {
    if (std.mem.indexOfScalar(u8, order, ch)) |pos| {
        return @as(u8, @intCast(pos)) + 1; // 0 is reserved for Jokers in part 2
    }
    return error.InvalidInput;
}

fn computeRank(values: *const [5]u8) u8 {
    // Find the top two counts, which define the rank of the hand. (There are
    // only 5 cards, so the remaining counts are at most 1.)
    //
    //  5, 0  five of a kind
    //  4, 1  four of a kind
    //  3, 2  full house
    //  3, 1  three of a kind
    //  2, 2  two pair
    //  2, 1  one pair
    //  1, 1  high card
    //
    // If we have any jokers, we will use substitute them for the most-common
    // other card, which is optimal.
    var count = std.mem.zeroes([num_values]u8);
    for (values) |v| count[v] += 1;
    std.mem.swap(u8, &count[1], &count[1 + std.mem.indexOfMax(u8, count[1..])]);
    std.mem.swap(u8, &count[2], &count[2 + std.mem.indexOfMax(u8, count[2..])]);
    return (count[0] + count[1]) * 5 + count[2];
}

const Hand = struct {
    rank: u8,
    values: [5]u8,
    bid: u32,

    fn compare(_: void, a: Hand, b: Hand) bool {
        if (a.rank != b.rank) return a.rank < b.rank;
        return std.mem.lessThan(u8, &a.values, &b.values);
    }
};

pub fn parseInput(allocator: std.mem.Allocator, input: []const u8) ![]Hand {
    var scanner = Scanner.init(input);
    var list = std.ArrayList(Hand).init(allocator);
    errdefer list.deinit();
    while (!scanner.isEmpty()) {
        const chars = try scanner.scanAlphanumeric();
        scanner.skipHorizontalSpace();
        const bid = try scanner.scanInt(u32);
        try scanner.skipNewline();
        var values: [5]u8 = undefined;
        if (chars.len != values.len) return error.InvalidInput;
        for (&values, chars) |*value, char| value.* = try cardValue(char);
        try list.append(Hand{ .rank = 0, .values = values, .bid = bid });
    }
    return try list.toOwnedSlice();
}

pub fn solvePart(hands: []Hand) u64 {
    for (hands) |*hand| hand.rank = computeRank(&hand.values);
    std.mem.sortUnstable(Hand, hands, {}, Hand.compare);
    var result: u64 = 0;
    for (hands, 1..) |hand, rank| result += hand.bid * rank;
    return result;
}

pub fn solve(env: *Environment) !void {
    const hands = try env.parseInputHeap([]Hand, parseInput);
    defer env.getHeapAllocator().free(hands);

    // Part 1.
    try env.setAnswer1(solvePart(hands));

    // Part 2: replace jacks with jokers, which have minimal value, but can
    // substitute for any other card.
    const jack = try cardValue('J');
    for (hands) |*hand| {
        for (&hand.values) |*value| {
            if (value.* == jack) value.* = 0;
        }
    }
    try env.setAnswer2(solvePart(hands));
}

pub fn main() !void {
    try @import("framework/running.zig").runSolutionStdIO(solve);
}

test "example" {
    try @import("framework/testing.zig").testSolver(solve,
        \\32T3K 765
        \\T55J5 684
        \\KK677 28
        \\KTJJT 220
        \\QQQJA 483
        \\
    , "6440", "5905");
}
