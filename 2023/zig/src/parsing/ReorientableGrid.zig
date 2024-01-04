// Version of Grid which can be transposed.
//
// Could be extended to support reflection and rotation too.
//
// Keep the supported methods in sync with Grid.zig

const PlainGrid = @import("./Grid.zig");
const std = @import("std");

height: usize,
width: usize,
rowStride: usize,
colStride: usize,
data: [*]const u8,

const Grid = @This();

pub fn init(data: []const u8) !Grid {
    const plainGrid = try PlainGrid.init(data);
    return Grid{
        .height = plainGrid.height,
        .width = plainGrid.width,
        .rowStride = plainGrid.stride,
        .colStride = 1,
        .data = plainGrid.data,
    };
}

pub fn inBounds(self: Grid, row: isize, col: isize) bool {
    return 0 <= row and row < self.height and 0 <= col and col < self.width;
}

pub fn charAt(self: Grid, row: isize, col: isize) u8 {
    return self.charPtrAt(row, col).*;
}

pub fn charPtrAt(self: Grid, row: isize, col: isize) *const u8 {
    std.debug.assert(row >= 0 and col >= 0);
    return self.charPtrAtU(@as(usize, @intCast(row)), @as(usize, @intCast(col)));
}

pub fn charAtOr(self: Grid, row: isize, col: isize, default: u8) u8 {
    return if (self.inBounds(row, col)) self.charAt(row, col) else default;
}

// Like charAt(), but with unsigned coordinates.
pub fn charAtU(self: Grid, row: usize, col: usize) u8 {
    return self.charPtrAtU(row, col).*;
}

// Like charPtrAt(), but with unsigned coordinates.
pub fn charPtrAtU(self: Grid, row: usize, col: usize) *const u8 {
    std.debug.assert(row < self.height and col < self.width);
    return &self.data[row * self.rowStride + col * self.colStride];
}

pub fn transpose(self: Grid) Grid {
    return .{
        .height = self.width,
        .width = self.height,
        .rowStride = self.colStride,
        .colStride = self.rowStride,
        .data = self.data,
    };
}
