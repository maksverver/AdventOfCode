// Version of Grid which can be transposed.
//
// Could be extended to support reflection and rotation too.
//
// Keep the supported methods in sync with Grid.zig

const std = @import("std");
const findNewline = @import("./text.zig").findNewline;

pub fn ReorientableGrid(comptime T: type, comptime mutable: bool) type {
    return struct {
        height: usize,
        width: usize,
        baseIndex: usize,
        rowStride: isize,
        colStride: isize,
        data: SliceT,
        allocator: ?std.mem.Allocator,

        const SliceT = if (mutable) []T else []const T;
        const PtrT = if (mutable) *T else *const T;

        const Self = @This();

        pub fn init(data: SliceT) !Self {
            return initInternal(data, null);
        }

        // Like `init`, but `allocator` is used to free `data` in deinit().
        pub fn initOwned(data: SliceT, allocator: std.mem.Allocator) !Self {
            return initInternal(data, allocator);
        }

        fn initInternal(data: SliceT, allocator: ?std.mem.Allocator) !Self {
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
            std.debug.assert(height > 0);
            std.debug.assert(width > 0);
            return Self{
                .height = height,
                .width = width,
                .baseIndex = 0,
                .rowStride = @as(isize, @intCast(stride)),
                .colStride = 1,
                .data = data,
                .allocator = allocator,
            };
        }

        pub fn deinit(self: Self) void {
            std.debug.assert(self.allocator != null);
            if (self.allocator) |a| a.free(self.data);
        }

        pub fn inBounds(self: Self, row: isize, col: isize) bool {
            return 0 <= row and row < self.height and 0 <= col and col < self.width;
        }

        pub fn charAt(self: Self, row: isize, col: isize) T {
            return self.charPtrAt(row, col).*;
        }

        pub fn charPtrAt(self: Self, row: isize, col: isize) PtrT {
            std.debug.assert(row >= 0 and col >= 0);
            return self.charPtrAtU(@as(usize, @intCast(row)), @as(usize, @intCast(col)));
        }

        pub fn charAtOr(self: Self, row: isize, col: isize, default: T) T {
            return if (self.inBounds(row, col)) self.charAt(row, col) else default;
        }

        // Like charAt(), but with unsigned coordinates.
        pub fn charAtU(self: Self, row: usize, col: usize) T {
            return self.charPtrAtU(row, col).*;
        }

        fn idx(self: Self, row: usize, col: usize) usize {
            std.debug.assert(row < self.height and col < self.width);
            return @as(usize, @intCast(@as(isize, @intCast(self.baseIndex)) +
                @as(isize, @intCast(row)) * self.rowStride +
                @as(isize, @intCast(col)) * self.colStride));
        }

        // Like charPtrAt(), but with unsigned coordinates.
        pub fn charPtrAtU(self: Self, row: usize, col: usize) PtrT {
            return &self.data[self.idx(row, col)];
        }

        pub fn transposed(self: Self) Self {
            return .{
                .height = self.width,
                .width = self.height,
                .baseIndex = self.idx(0, 0),
                .rowStride = self.colStride,
                .colStride = self.rowStride,
                .data = self.data,
                .allocator = self.allocator,
            };
        }

        // Rotate the grid 90 degrees clockwise.
        pub fn rotatedClockwise(self: Self) Self {
            return .{
                .height = self.width,
                .width = self.height,
                .baseIndex = self.idx(0, self.width - 1),
                .rowStride = -self.colStride,
                .colStride = self.rowStride,
                .data = self.data,
                .allocator = self.allocator,
            };
        }

        // Rotate the grid 90 degrees anticlockwise.
        pub fn rotatedAnticlockwise(self: Self) Self {
            return .{
                .height = self.width,
                .width = self.height,
                .baseIndex = self.idx(self.height - 1, 0),
                .rowStride = self.colStride,
                .colStride = -self.rowStride,
                .data = self.data,
                .allocator = self.allocator,
            };
        }

        // Creates a mutable copy of the current grid. Must be freed by calling deinit().
        pub fn mutableCopy(self: Self, allocator: std.mem.Allocator) !ReorientableGrid(T, true) {
            return .{
                .height = self.height,
                .width = self.width,
                .baseIndex = self.baseIndex,
                .rowStride = self.rowStride,
                .colStride = self.colStride,
                .data = try allocator.dupe(T, self.data),
                .allocator = allocator,
            };
        }

        pub fn isEqualTo(self: Self, other: Self) bool {
            const h = self.height;
            if (other.height != h) return false;
            const w = self.width;
            if (other.width != w) return false;
            for (0..h) |r| {
                for (0..w) |c| {
                    if (self.charAtU(r, c) != other.charAtU(r, c)) return false;
                }
            }
            return true;
        }
    };
}
