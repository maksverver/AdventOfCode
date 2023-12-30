const std = @import("std");

// Detects a newline sequence (either CR, LF, CR LF, or LF CR) in `data` and
// returns a pair {nl, end} indicating where the newline sequence begins and
// ends, or returns null if no newlines are found.
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

// Splits the data into lines, stripping newline characters.
//
// Returns error.MissingNewline if `data` doesn't end with a newline character.
// Otherwise, runs a slice of lines that must be freed by the caller.
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
