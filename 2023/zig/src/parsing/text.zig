const std = @import("std");

const testing = @import("./testing.zig");
const expectEqual = testing.expectEqual;
const expectEqualString = testing.expectEqualString;
const expectEqualStringSlice = testing.expectEqualStringSlice;

/// Detects a newline sequence (either CR, LF, CR LF, or LF CR) in `data` and
/// returns a pair {nl, end} indicating where the newline sequence begins and
/// ends, or returns null if no newlines are found.
pub fn findNewline(data: []const u8) ?struct { nl: usize, end: usize } {
    var pos: usize = 0;
    while (pos < data.len) : (pos += 1) {
        if (data[pos] == '\r') {
            var end = pos + 1;
            if (end < data.len and data[end] == '\n') end += 1;
            return .{ .nl = pos, .end = end };
        }
        if (data[pos] == '\n') {
            var end = pos + 1;
            if (end < data.len and data[end] == '\r') end += 1;
            return .{ .nl = pos, .end = end };
        }
    }
    return null;
}

test "findNewline() not found" {
    try expectEqual(findNewline("foobar"), null);
}

test "findNewline() at end of line" {
    const sep1 = findNewline("foo\n").?;
    try expectEqual(sep1.nl, 3);
    try expectEqual(sep1.end, 4);

    const sep2 = findNewline("foo\r\n");
    try expectEqual(sep2.?.nl, 3);
    try expectEqual(sep2.?.end, 5);
}

test "findNewline() finds first newline" {
    try expectEqual(findNewline("foo\rbar\n").?.nl, 3);
    try expectEqual(findNewline("foo\nbar\r").?.end, 4);

    try expectEqual(findNewline("foo\rbar\n").?.nl, 3);
    try expectEqual(findNewline("foo\nbar\r").?.end, 4);
}

test "findNewline() multiple newline characters in a row" {
    try expectEqual(findNewline("\r\r").?.end, 1);
    try expectEqual(findNewline("\n\n").?.end, 1);
    try expectEqual(findNewline("\r\n\r\n").?.end, 2);
    try expectEqual(findNewline("\n\r\n\r").?.end, 2);
}

/// Returns the next line in `remaining` (excluding the newline sequence), and
/// updates `remaining` to contain the remaining text (starting right after
/// the newline sequence).
pub fn splitLine(remaining: *[]const u8) ?[]const u8 {
    const text = remaining.*;
    if (findNewline(text)) |sep| {
        remaining.* = text[sep.end..];
        return text[0..sep.nl];
    } else {
        return null;
    }
}

/// Splits the data into lines, stripping newline characters.
///
/// Returns error.EndOfInput if `data` doesn't end with a newline character,
/// or error.OutOfMemory if allocation fails. Otherwise, runs a slice of lines
/// that must be freed by the caller.
pub fn splitLinesAlloc(allocator: std.mem.Allocator, data: []const u8) error{ OutOfMemory, EndOfInput }![][]const u8 {
    var lines = std.ArrayList([]const u8).init(allocator);
    errdefer lines.deinit();
    var remaining = data;
    while (remaining.len > 0) {
        if (splitLine(&remaining)) |line| {
            try lines.append(line);
        } else {
            return error.EndOfInput;
        }
    }
    return lines.toOwnedSlice();
}

test "splitLinesAlloc() basic" {
    const lines = try splitLinesAlloc(std.testing.allocator, "foo\nbar\nquux\n");
    defer std.testing.allocator.free(lines);

    try expectEqualStringSlice(lines, &[_][]const u8{ "foo", "bar", "quux" });
}

test "splitLinesAlloc() crlf" {
    const lines = try splitLinesAlloc(std.testing.allocator, "foo\r\nbar\r\nquux\r\n");
    defer std.testing.allocator.free(lines);

    try expectEqualStringSlice(lines, &[_][]const u8{ "foo", "bar", "quux" });
}

test "splitLinesAlloc() empty input" {
    const lines = try splitLinesAlloc(std.testing.allocator, "");
    try expectEqual(lines.len, 0);
}

test "splitLinesAlloc() missing newline" {
    const result = splitLinesAlloc(std.testing.allocator, "foo\nbar");
    try expectEqual(result, error.EndOfInput);
}

// Iterates over the words in the given string, where a word is a maximal
// substring that does not contain whitespace, as defined by
// std.ascii.isWhitespace().
const WordIterator = struct {
    remaining: []const u8,

    fn init(text: []const u8) WordIterator {
        return WordIterator{ .remaining = text };
    }

    fn next(self: *WordIterator) ?[]const u8 {
        const text = self.remaining;
        var begin: usize = 0;
        while (begin < text.len and std.ascii.isWhitespace(text[begin])) begin += 1;
        var end = begin;
        while (end < text.len and !std.ascii.isWhitespace(text[end])) end += 1;
        self.remaining = text[end..];
        return if (begin < end) text[begin..end] else null;
    }
};

// Splits a string into words seperated by whitespace.
pub fn splitWords(allocator: std.mem.Allocator, text: []const u8) ![][]const u8 {
    var words = std.ArrayList([]const u8).init(allocator);
    errdefer words.deinit();
    var it = WordIterator.init(text);
    while (it.next()) |word| try words.append(word);
    return words.toOwnedSlice();
}

test "splitWords() basic" {
    const received = try splitWords(std.testing.allocator, "foo bar baz");
    defer std.testing.allocator.free(received);
    try expectEqualStringSlice(received, &[_][]const u8{ "foo", "bar", "baz" });
}

test "splitWords() extra spaces" {
    const received = try splitWords(std.testing.allocator, "   foo\r\n\tbar   baz   ");
    defer std.testing.allocator.free(received);
    try expectEqualStringSlice(received, &[_][]const u8{ "foo", "bar", "baz" });
}

pub fn joinWith(allocator: std.mem.Allocator, separator: []const u8, pieces: []const []const u8) ![]const u8 {
    var buf = std.ArrayList(u8).init(allocator);
    if (pieces.len > 0) {
        try buf.appendSlice(pieces[0]);
        var pos: usize = 1;
        while (pos < pieces.len) : (pos += 1) {
            try buf.appendSlice(separator);
            try buf.appendSlice(pieces[pos]);
        }
    }
    return try buf.toOwnedSlice();
}

test "joinWith() basic" {
    const received = try joinWith(std.testing.allocator, ",", &[_][]const u8{ "foo", "bar", "baz" });
    defer std.testing.allocator.free(received);
    try expectEqualString(received, "foo,bar,baz");
}

test "joinWith() empty seperator" {
    const received = try joinWith(std.testing.allocator, "", &[_][]const u8{ "foo", "bar", "baz" });
    defer std.testing.allocator.free(received);
    try expectEqualString(received, "foobarbaz");
}

test "joinWith() empty input" {
    const received = try joinWith(std.testing.allocator, ",", &[0][]const u8{});
    defer std.testing.allocator.free(received);
    try expectEqualString(received, "");
}

/// Parses the given text as a list of numbers in decimal notation.
pub fn parseNumbers(comptime T: type, allocator: std.mem.Allocator, text: []const u8) ![]T {
    var numbers = std.ArrayList(T).init(allocator);
    errdefer numbers.deinit();
    var it = WordIterator.init(text);
    while (it.next()) |word| try numbers.append(try std.fmt.parseInt(T, word, 10));
    return numbers.toOwnedSlice();
}

pub fn removePrefix(data: []const u8, prefix: []const u8) ?[]const u8 {
    return if (std.mem.startsWith(u8, data, prefix)) data[prefix.len..] else null;
}
