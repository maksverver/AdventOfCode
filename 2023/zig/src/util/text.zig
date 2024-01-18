const std = @import("std");

const testing = @import("./testing.zig");
const expectEqual = testing.expectEqual;
const expectEqualString = testing.expectEqualString;
const expectEqualStringSlice = testing.expectEqualStringSlice;
const expectEqualOptionalString = testing.expectEqualOptionalString;

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

pub fn removeNewline(text: []const u8) ?[]const u8 {
    const n = text.len;
    if (n > 0 and text[n - 1] == '\n') {
        if (n > 1 and text[n - 2] == '\r') return text[0 .. n - 2];
        return text[0 .. n - 1];
    }
    if (n > 0 and text[n - 1] == '\r') {
        if (n > 1 and text[n - 2] == '\n') return text[0 .. n - 2];
        return text[0 .. n - 1];
    }
    return null;
}

pub fn countLines(text: []const u8) ?usize {
    var remaining = text;
    var lines: usize = 0;
    while (remaining.len > 0) {
        if (findNewline(remaining)) |sep| {
            remaining = remaining[sep.end..];
            lines += 1;
        } else {
            return null;
        }
    }
    return lines;
}

test "removeNewline" {
    try expectEqualOptionalString(removeNewline(""), null);
    try expectEqualOptionalString(removeNewline("foo\nbar"), null);
    try expectEqualOptionalString(removeNewline("foo\nbar\n").?, "foo\nbar");
    try expectEqualOptionalString(removeNewline("foo\rbar\r").?, "foo\rbar");
    try expectEqualOptionalString(removeNewline("foo\r\nbar\r\n").?, "foo\r\nbar");
    try expectEqualOptionalString(removeNewline("foo\n\rbar\n\r").?, "foo\n\rbar");
    try expectEqualOptionalString(removeNewline("foo\r\rbar\r\r").?, "foo\r\rbar\r");
    try expectEqualOptionalString(removeNewline("foo\n\nbar\n\n").?, "foo\n\nbar\n");
}

pub const LineIterator = struct {
    remaining: []const u8,

    pub fn init(text: []const u8) !LineIterator {
        if (text.len > 0 and removeNewline(text) == null) return error.MissingNewline;
        return .{ .remaining = text };
    }

    pub fn isEmpty(self: *const LineIterator) bool {
        return self.remaining.len == 0;
    }

    pub fn next(self: *LineIterator) ?[]const u8 {
        return splitLine(&self.remaining);
    }
};

// Splits input into paragraphs delineated by double newline sequences. Each
// item is a list of lines, each terminated by a newline character.
pub const ParagraphIterator = struct {
    it: LineIterator,

    pub fn init(text: []const u8) !ParagraphIterator {
        return .{ .it = try LineIterator.init(text) };
    }

    pub fn isEmpty(self: *const ParagraphIterator) bool {
        return self.it.isEmpty();
    }

    pub fn next(self: *ParagraphIterator) ?[]const u8 {
        if (self.it.isEmpty()) return null;
        const begin = self.it.remaining;
        while (self.it.next()) |line| {
            if (line.len == 0) return begin[0 .. @intFromPtr(line.ptr) - @intFromPtr(begin.ptr)];
        }
        return begin;
    }
};

test "ParagraphIterator basic" {
    var it = try ParagraphIterator.init("foo\n\nbar\nbaz\n\nquux\n");
    try expectEqualOptionalString(it.next(), "foo\n");
    try expectEqualOptionalString(it.next(), "bar\nbaz\n");
    try expectEqualOptionalString(it.next(), "quux\n");
    try expectEqualOptionalString(it.next(), null);
}

test "ParagraphIterator empty" {
    var it = try ParagraphIterator.init("");
    try expectEqualOptionalString(it.next(), null);
}

test "ParagraphIterator missing newline" {
    try expectEqual(ParagraphIterator.init("foobar"), error.MissingNewline);
}

/// Splits the data into lines, stripping newline characters.
///
/// Returns error.MissingNewline if `data` doesn't end with a newline character,
/// or error.OutOfMemory if allocation fails. Otherwise, runs a slice of lines
/// that must be freed by the caller.
pub fn splitLinesAlloc(allocator: std.mem.Allocator, data: []const u8) error{ OutOfMemory, MissingNewline }![][]const u8 {
    var it = try LineIterator.init(data);
    var lines = std.ArrayList([]const u8).init(allocator);
    errdefer lines.deinit();
    while (it.next()) |line| try lines.append(line);
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
    try expectEqual(result, error.MissingNewline);
}

// Iterates over the words in the given string, where a word is a maximal
// substring that does not contain whitespace, as defined by
// std.ascii.isWhitespace().
pub const WordIterator = struct {
    remaining: []const u8,

    pub fn init(text: []const u8) WordIterator {
        return WordIterator{ .remaining = text };
    }

    pub fn next(self: *WordIterator) ?[]const u8 {
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

// Parses the given text into a slice of numbers. The length of the slice
// determines how many numbers to parse. This function is useful to parse lines
// when the number of numbers is exactly known.
pub fn parseNumbersSlice(comptime T: type, numbers: []T, text: []const u8) !void {
    var it = WordIterator.init(text);
    for (numbers) |*number| {
        if (it.next()) |word| {
            number.* = try std.fmt.parseInt(T, word, 10);
        } else {
            return error.TooFewTokens;
        }
    }
    if (it.next() != null) return error.TooManyTokens;
}

/// Parses the given text as a list of numbers in decimal notation.
pub fn parseNumbersAlloc(comptime T: type, allocator: std.mem.Allocator, text: []const u8) ![]T {
    var list = std.ArrayList(T).init(allocator);
    errdefer list.deinit();
    try parseNumbersToList(T, &list, text);
    return list.toOwnedSlice();
}

pub fn parseNumbersToList(comptime T: type, list: *std.ArrayList(T), text: []const u8) !void {
    var it = WordIterator.init(text);
    while (it.next()) |word| try list.append(try std.fmt.parseInt(T, word, 10));
}

pub fn removePrefix(data: []const u8, prefix: []const u8) ?[]const u8 {
    return if (std.mem.startsWith(u8, data, prefix)) data[prefix.len..] else null;
}
