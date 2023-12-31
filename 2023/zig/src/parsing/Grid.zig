const findNewline = @import("./lines.zig").findNewline;
const std = @import("std");

height: usize,
width: usize,
stride: usize,
data: [*]const u8,

const Grid = @This();

pub fn init(data: []const u8) !Grid {
    const firstNl = findNewline(data) orelse return error.MissingNewline;
    const width = firstNl.nl;
    const stride = firstNl.end;
    if (data.len % stride != 0) return error.InvalidSize;
    const height = data.len / stride;
    // This part is theoretically optional: it just verifies that the rest
    // of the file uses the same width and stride.
    var remaining = data[stride..];
    while (remaining.len > 0) {
        const nl = findNewline(remaining) orelse return error.MissingNewline;
        if (nl.nl != width or nl.end != stride) return error.InvalidInput;
        remaining = remaining[stride..];
    }
    return Grid{
        .height = height,
        .width = width,
        .stride = stride,
        .data = data.ptr,
    };
}

pub fn inBounds(self: *const Grid, row: isize, col: isize) bool {
    return 0 <= row and row < self.height and 0 <= col and col < self.width;
}

pub fn charAt(self: *const Grid, row: isize, col: isize) u8 {
    return self.charPtrAt(row, col).*;
}

pub fn charPtrAt(self: *const Grid, row: isize, col: isize) *const u8 {
    std.debug.assert(self.inBounds(row, col));
    return &self.data[@as(usize, @intCast(row)) * self.stride + @as(usize, @intCast(col))];
}

pub fn charAtOr(self: *const Grid, row: isize, col: isize, default: u8) u8 {
    return if (self.inBounds(row, col)) self.charAt(row, col) else default;
}
