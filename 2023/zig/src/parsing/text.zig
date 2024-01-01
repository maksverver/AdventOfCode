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

/// Splits the data into lines, stripping newline characters.
///
/// Returns error.MissingNewline if `data` doesn't end with a newline character.
/// Otherwise, runs a slice of lines that must be freed by the caller.
pub fn splitLines(allocator: std.mem.Allocator, data: []const u8) error{ OutOfMemory, EndOfInput }![][]const u8 {
    var lines = std.ArrayList([]const u8).init(allocator);
    defer lines.deinit();

    var remaining = data;
    while (remaining.len > 0) {
        if (findNewline(remaining)) |sep| {
            try lines.append(remaining[0..sep.nl]);
            remaining = remaining[sep.end..];
        } else {
            return error.EndOfInput;
        }
    }
    return lines.toOwnedSlice();
}

test "splitLines() basic" {
    const lines = try splitLines(std.testing.allocator, "foo\nbar\nquux\n");
    defer std.testing.allocator.free(lines);

    try expectEqualStringSlice(lines, &[_][]const u8{ "foo", "bar", "quux" });
}

test "splitLines() crlf" {
    const lines = try splitLines(std.testing.allocator, "foo\r\nbar\r\nquux\r\n");
    defer std.testing.allocator.free(lines);

    try expectEqualStringSlice(lines, &[_][]const u8{ "foo", "bar", "quux" });
}

test "splitLines() empty input" {
    const lines = try splitLines(std.testing.allocator, "");
    try expectEqual(lines.len, 0);
}

test "splitLines() missing newline" {
    const result = splitLines(std.testing.allocator, "foo\nbar");
    try expectEqual(result, error.EndOfInput);
}

// Splits a string into words seperated by whitespace.
pub fn splitWords(allocator: std.mem.Allocator, data: []const u8) ![][]const u8 {
    var words = std.ArrayList([]const u8).init(allocator);
    errdefer words.deinit();
    var pos: usize = 0;
    while (pos < data.len) {
        while (pos < data.len and std.ascii.isWhitespace(data[pos])) pos += 1;
        const begin = pos;
        while (pos < data.len and !std.ascii.isWhitespace(data[pos])) pos += 1;
        if (begin < pos) try words.append(data[begin..pos]);
    }
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

pub fn parseNumbers(comptime T: type, allocator: std.mem.Allocator, words: []const []const u8) ![]T {
    var numbers = try allocator.alloc(T, words.len);
    errdefer allocator.free(numbers);
    for (words, 0..) |word, i| {
        numbers[i] = try std.fmt.parseInt(T, word, 10);
    }
    return numbers;
}

pub fn removePrefix(data: []const u8, prefix: []const u8) ![]const u8 {
    if (!std.mem.startsWith(u8, data, prefix)) return error.InvalidCharacter;
    return data[prefix.len..];
}
