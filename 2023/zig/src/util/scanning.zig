//! Functions to scan text.

const std = @import("std");

/// Afunction that returns the length of the prefix of its text argument that
/// matches, or null if there is no match.
pub const ScanFn = fn ([]const u8) ?usize;

fn scanNewline(text: []const u8) ?usize {
    if (text.len > 0) {
        if (text[0] == '\r') {
            return if (text.len > 1 and text[1] == '\n') 2 else 1;
        }
        if (text[0] == '\n') {
            return if (text.len > 1 and text[1] == '\r') 2 else 1;
        }
    }
    return null;
}

/// Matches a newline sequence, which is one of "\r", "\n", "\r\n" or "\n\r".
pub const newline: ScanFn = scanNewline;

fn matchPredicate(comptime predicate: fn (u8) bool, comptime not_empty: bool) ScanFn {
    return struct {
        fn f(text: []const u8) ?usize {
            var i: usize = 0;
            while (i < text.len and predicate(text[i])) i += 1;
            if (not_empty and i == 0) return null;
            return i;
        }
    }.f;
}

fn isHorizontalWhitespace(ch: u8) bool {
    return ch == ' ' or ch == '\t';
}

/// Matches a (possibly empty) sequence of horizontal whitespace characters:
/// space (32) or tab (8).
pub const horizontalWhitespace: ScanFn = matchPredicate(isHorizontalWhitespace, false);

/// Matches a nonempty string of alphabetic characters (a-z, A-Z).
pub const alphabetic: ScanFn = matchPredicate(std.ascii.isAlphabetic, true);

/// Matches a nonempty string of alphanumeric characters (a-z, A-Z, 0-9).
pub const alphanumeric: ScanFn = matchPredicate(std.ascii.isAlphanumeric, true);

fn isTokenChar(c: u8) bool {
    return !std.ascii.isWhitespace(c);
}

// Matches a token: a non-empty sequence of non-whitespace characters.
pub const token: ScanFn = matchPredicate(isTokenChar, true);

/// Matches the expected string exactly (including space!)
pub fn scanText(comptime expected: []const u8) ScanFn {
    return struct {
        fn f(text: []const u8) ?usize {
            if (std.mem.startsWith(u8, text, expected)) return expected.len;
            return null;
        }
    }.f;
}

fn scanNumber(text: []const u8) ?usize {
    var i: usize = 0;
    if (i < text.len and text[i] == '-' or text[i] == '+') i += 1;
    var j: usize = i;
    while (j < text.len and std.ascii.isAlphanumeric(text[j])) j += 1;
    if (j > i) return j else return null;
}

/// Matches a number with an optional leading sign (+/-).
///
/// Note: currently this technically accepts any alphanumeric string in order to
/// accept numbers in any base. Possible improvement: add arguments to specify
/// the base (and maybe whether a sign is allowed) to restrict matched strings.
pub const number: ScanFn = scanNumber;
