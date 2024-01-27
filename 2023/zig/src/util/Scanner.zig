// A text scanner.
//
// Also see the scanning functions in scanning.zig.

const std = @import("std");
const scanning = @import("scanning.zig");

const Scanner = @This();

/// Remaining text.
text: []const u8,

/// Initializes the scanner from the given text.
pub fn init(text: []const u8) Scanner {
    return .{ .text = text };
}

/// Returns whether the scanner is empty, i.e., the remaining text has length 0.
pub fn isEmpty(self: Scanner) bool {
    return self.text.len == 0;
}

/// Returns the prefix of the remaining text that matches according to the
/// given scanning function f, and updates the remaining text to skip past it,
/// or returns error.NoMatch if the text does not match.
pub fn scan(self: *Scanner, comptime f: scanning.ScanFn) error{NoMatch}![]const u8 {
    if (f(self.text)) |l| {
        const res = self.text[0..l];
        self.text = self.text[l..];
        return res;
    } else {
        return error.NoMatch;
    }
}

/// Similar to scan(), this returns the text matched by f, but it if there is a
/// match, the remaining text is not updated, and if there is no match, then
/// this returns null instead of an error.
pub fn peek(self: Scanner, comptime f: scanning.ScanFn) ?[]const u8 {
    if (f(self.text)) |l| return self.text[0..l];
    return null;
}

/// Similar to scan(), except this does not return the matched text, only an
/// void (if there is a match) or error.NoMatch (if there is none).
pub fn skip(self: *Scanner, comptime f: scanning.ScanFn) error{NoMatch}!void {
    _ = try scan(self, f);
}

/// Similar to skip(), except this does not throw an error if the there is no
/// match. That means that if the prefix of the remaining text matches the
/// scanning function f, it is skipped, otherwise nothing happens.
pub fn maybeSkip(self: Scanner, comptime f: scanning.ScanFn) void {
    skip(self, f) catch {};
}

/// Scans a base 10 integer.
pub fn scanInt(self: *Scanner, comptime T: type) !T {
    return self.scanIntBase(T, 10);
}

/// Scans an integer in the given base.
pub fn scanIntBase(self: *Scanner, comptime T: type, base: u8) !T {
    if (scanning.number(self.text)) |l| {
        const i = try std.fmt.parseInt(T, self.text[0..l], base);
        self.text = self.text[l..];
        return i;
    } else {
        return error.NoMatch;
    }
}

/// Convenience method to skip any amount of horizontal whitespace (including none at all).
pub fn skipHorizontalSpace(self: *Scanner) void {
    return self.skip(scanning.horizontalWhitespace) catch unreachable;
}

/// Convenience method to skip an expected newline (which fails if the newline is missing).
pub fn skipNewline(self: *Scanner) !void {
    return self.skip(scanning.newline);
}

/// Convenience method to skip static text, which must be matched exactly,
/// including space!
pub fn skipText(self: *Scanner, comptime text: []const u8) !void {
    return self.skip(scanning.scanText(text));
}

/// Prints the remaining input of the scanner for debugging. This is useful
/// to debug parse failures.
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
