// A text scanner.
//
// Maybe: refactor this to auto-skip whitespace before tokens?
// Make peekNewline() and peekText() return the same value
// Overall this is not a very orthogonal structure :/

const std = @import("std");

const Scanner = @This();

text: []const u8,

pub fn init(text: []const u8) Scanner {
    return Scanner{ .text = text };
}

pub fn isEmpty(self: Scanner) bool {
    return self.text.len == 0;
}

fn isHorizontalSpace(c: u8) bool {
    return c == ' ' or c == '\t';
}

pub fn skipHorizontalSpace(self: *Scanner) void {
    self.text = self.text[self.peekPredicate(isHorizontalSpace).len..];
}

pub fn peekNewline(self: Scanner) []const u8 {
    var n: usize = 0;
    if (self.text[0] == '\r') {
        n = 1;
        if (n < self.text.len and self.text[n] == '\n') n += 1;
    } else if (self.text[0] == '\n') {
        n = 1;
        if (n < self.text.len and self.text[n] == '\r') n += 1;
    }
    return self.text[0..n];
}

pub fn skipNewline(self: *Scanner) !void {
    if (self.text.len == 0) return error.EndOfInput;
    const nl = self.peekNewline();
    if (nl.len == 0) return error.InvalidCharacter;
    self.text = self.text[nl.len..];
}

// Returns a maximal substring of consecutive characters matching `predicate`.
pub fn peekPredicate(self: Scanner, comptime predicate: fn (c: u8) bool) []const u8 {
    var end: usize = 0;
    while (end < self.text.len and predicate(self.text[end])) {
        end += 1;
    }
    return self.text[0..end];
}

pub fn scanPredicate(self: *Scanner, comptime predicate: fn (c: u8) bool) ![]const u8 {
    const s = self.peekPredicate(predicate);
    if (s.len == 0) return error.InvalidCharacter;
    self.text = self.text[s.len..];
    return s;
}

pub fn scanInt(self: *Scanner, comptime T: type) !T {
    const s = self.peekPredicate(std.ascii.isDigit);
    if (s.len == 0) return error.InvalidCharacter;
    const result = try std.fmt.parseInt(T, s, 10);
    self.text = self.text[s.len..];
    return result;
}

pub fn peekText(self: Scanner, text: []const u8) bool {
    if (std.mem.startsWith(u8, self.text, text)) {
        return true;
    }
    return false;
}

pub fn peekAlphabetic(self: *Scanner) ![]const u8 {
    return self.peekPredicate(std.ascii.isAlphabetic);
}

pub fn scanAlphabetic(self: *Scanner) ![]const u8 {
    return self.scanPredicate(std.ascii.isAlphabetic);
}

pub fn peekAlphanumeric(self: *Scanner) ![]const u8 {
    return self.peekPredicate(std.ascii.isAlphanumeric);
}

pub fn scanAlphanumeric(self: *Scanner) ![]const u8 {
    return self.scanPredicate(std.ascii.isAlphanumeric);
}

pub fn skipText(self: *Scanner, text: []const u8) !void {
    if (!std.mem.startsWith(u8, self.text, text)) return error.InvalidCharacter;
    self.text = self.text[text.len..];
}

pub fn debugPrintRemainingInput(self: Scanner) void {
    const maxLen = 100;
    if (self.text.len <= maxLen) {
        std.debug.print("Remaining input: [{s}]\n", .{self.text});
    } else {
        std.debug.print(
            "Remaining input: [{s}] (and {d} more bytes)\n",
            .{ self.text[0..maxLen], self.text.len - maxLen },
        );
    }
}
