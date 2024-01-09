// Functions to define 2D grids of characters or other values, both owning and
// non-owning.
//
// This file probably does not belong in the parsing/ subdirectory because only
// a tiny part is related to input parsing (see initFromText()), but Zig makes
// it really difficult to share code between files in separate subdiretories, so
// here we are.

const std = @import("std");
const findNewline = @import("./text.zig").findNewline;

// An orientable grid has methods to rotate, reflect and transpose in O(1) time.
const Orientability = enum { fixed, orientable };

// A mutable grid returns non-const pointers to data, allowing the grid contents
// to be modified.
const Mutability = enum { readonly, mutable };

// An grid that is ownable can own a copy of the grid data it references (but
// not necessarily does). It it does own its data, it stores a copy of the
// allocator, and deinit() must be called to free the data.
const Ownability = enum { unowned, ownable };

// The coordinates of a grid cell.
pub const Coords = struct {
    r: usize,
    c: usize,
};

// The four orthognal directions on the square grid.
pub const Dir = enum {
    n, // north
    e, // east
    s, // south
    w, // west

    // Next direction; rotation in clockwise order (e.g. n -> e).
    pub fn next(dir: Dir) Dir {
        return @enumFromInt(dir.asInt() +% 1);
    }

    // Previous direction; rotation in anticlockwise order (e.g. n -> w).
    pub fn prev(dir: Dir) Dir {
        return @enumFromInt(dir.asInt() -% 1);
    }

    pub fn reverse(dir: Dir) Dir {
        return @enumFromInt(dir.asInt() +% 2);
    }

    // Returns 0 for vertical (n/s) or 1 for horizontal (e/w)
    pub fn axis(dir: Dir) u1 {
        return @truncate(dir.asInt());
    }

    pub fn asInt(dir: Dir) u2 {
        return @intFromEnum(dir);
    }

    pub fn asBit(dir: Dir) u4 {
        return @as(u4, 1) << dir.asInt();
    }
};

const GridConfig = struct {
    mutability: Mutability = .readonly,
    ownability: Ownability = .unowned,
    orientability: Orientability = .fixed,

    fn setMutability(config: GridConfig, mutability: Mutability) GridConfig {
        var res = config;
        res.mutability = mutability;
        return res;
    }

    fn setOwnability(config: GridConfig, ownability: Ownability) GridConfig {
        var res = config;
        res.ownability = ownability;
        return res;
    }

    fn setOrientability(config: GridConfig, orientability: Orientability) GridConfig {
        var res = config;
        res.orientability = orientability;
        return res;
    }
};

pub fn compareGrids(a: anytype, b: anytype) bool {
    if (a.height != b.height or a.width != b.width) return false;
    for (0..a.height) |r| {
        for (0..a.width) |c| {
            if (a.charAt(r, c) != b.charAt(r, c)) return false;
        }
    }
    return true;
}

pub fn Grid(comptime T: type, comptime config: GridConfig) type {
    const SliceT = switch (config.mutability) {
        .readonly => []const T,
        .mutable => []T,
    };
    const PtrT = switch (config.mutability) {
        .readonly => *const T,
        .mutable => *T,
    };
    const ManyItemPtrT = switch (config.mutability) {
        .readonly => [*]const T,
        .mutable => [*]T,
    };
    const DataT = switch (config.orientability) {
        .fixed => ManyItemPtrT,
        .orientable => SliceT,
    };
    const AllocatorT = switch (config.ownability) {
        .ownable => ?std.mem.Allocator,
        .unowned => void,
    };
    const allocatorNull = switch (config.ownability) {
        .ownable => null, // optional
        .unowned => {}, // void
    };

    // The fixed grid has a fixed orientation. It contains width and height to
    // describe the dimensions of the grid, and the row stride which is used to
    // index into `data`.
    //
    // Keep the methods in sync with OrientableGrid below, where it makes sense.
    const FixedGrid = struct {
        height: usize,
        width: usize,
        stride: usize,
        data: DataT,
        allocator: AllocatorT = allocatorNull,

        const Self = @This();

        pub fn initUnowned(height: usize, width: usize, stride: usize, data: DataT) Self {
            return .{
                .height = height,
                .width = width,
                .stride = stride,
                .data = data,
            };
        }

        pub fn initOwned(allocator: std.mem.Allocator, height: usize, width: usize, stride: usize, data: DataT) Self {
            return .{
                .height = height,
                .width = width,
                .stride = stride,
                .data = data,
                .allocator = allocator,
            };
        }

        // Returns a newly-allocated a grid of dimensions height × width with the given initial value.
        // deinit() must be called to free the allocated memory.
        pub fn initAlloc(allocator: std.mem.Allocator, height: usize, width: usize, initial_value: T) !Self {
            // In theory we could accept a stride argument that can be larger
            // than width, but is there a reasonable use case for it?
            const stride = width;
            const data = try allocator.alloc(T, height * stride);
            @memset(data, initial_value);
            return Self.initOwned(allocator, height, width, stride, data.ptr);
        }

        // Initializes a grid by splitting `text` into lines. All lines must be
        // of equal length. The result is a grid referencing an unowned copy of
        // the input data.
        pub fn initFromText(text: []const u8) !Self {
            const firstNl = findNewline(text) orelse return error.MissingNewline;
            const width = firstNl.nl;
            const stride = firstNl.end;
            if (text.len % stride != 0) return error.InvalidSize;
            const height = text.len / stride;
            // This part is theoretically optional: it just verifies that the rest
            // of the file uses the same width and stride.
            var remaining = text[stride..];
            while (remaining.len > 0) {
                const nl = findNewline(remaining) orelse return error.MissingNewline;
                if (nl.nl != width or nl.end != stride) return error.InvalidInput;
                remaining = remaining[stride..];
            }
            return Self.initUnowned(height, width, stride, text.ptr);
        }

        pub fn deinit(self: Self) void {
            if (self.allocator) |a| a.free(self.dataSlice());
        }

        pub fn dataSlice(self: Self) SliceT {
            return self.data[0 .. (self.height - 1) * self.stride + self.width];
        }

        // Creates a mutable copy of the current grid. Must be freed by calling deinit().
        pub fn duplicate(
            self: Self,
            comptime mutability: Mutability,
            allocator: std.mem.Allocator,
        ) !Grid(T, config.setOwnability(.ownable).setMutability(mutability)) {
            return .{
                .height = self.height,
                .width = self.width,
                .stride = self.stride,
                .data = (try allocator.dupe(T, self.dataSlice())).ptr,
                .allocator = allocator,
            };
        }

        // Maybe later: a method to return a readonly and/or unowned copy of this grid.

        pub fn move(self: Self, pos: Coords, dir: Dir, dist: usize) ?Coords {
            return switch (dir) {
                .n => if (pos.r >= dist) .{ .r = pos.r - dist, .c = pos.c } else null,
                .e => if (self.width - pos.c > dist) .{ .r = pos.r, .c = pos.c + dist } else null,
                .s => if (self.height - pos.r > dist) .{ .r = pos.r + dist, .c = pos.c } else null,
                .w => if (pos.c >= dist) .{ .r = pos.r, .c = pos.c - dist } else null,
            };
        }

        pub fn moveBy(self: Self, pos: Coords, dr: isize, dc: isize) ?Coords {
            var r = @as(isize, @intCast(pos.r)) + dr;
            var c = @as(isize, @intCast(pos.c)) + dc;
            if (0 <= r and r < self.height and 0 <= c and c < self.width) {
                return Coords{
                    .r = @as(usize, @intCast(r)),
                    .c = @as(usize, @intCast(c)),
                };
            }
            return null;
        }

        pub fn charAt(self: Self, row: usize, col: usize) T {
            return self.charPtrAt(row, col).*;
        }

        pub fn charPtrAt(self: Self, row: usize, col: usize) PtrT {
            std.debug.assert(row < self.height and col < self.width);
            return &self.data[row * self.stride + col];
        }

        pub fn charAtPos(self: Self, pos: Coords) T {
            return self.charPtrAtPos(pos).*;
        }

        pub fn charPtrAtPos(self: Self, pos: Coords) PtrT {
            return self.charPtrAt(pos.r, pos.c);
        }

        pub fn isEqualTo(self: Self, other: anytype) bool {
            return compareGrids(self, other);
        }

        pub fn indexOf(self: Self, ch: T) !Coords {
            for (0..self.height) |r| {
                for (0..self.width) |c| {
                    if (self.charAt(r, c) == ch) return .{ .r = r, .c = c };
                }
            }
            return error.NotFound;
        }
    };

    // The orientable grid also has a base index and column stride, which allows
    // operations like rotation, reflection, and transposition in O(1) time.
    //
    // Keep the methods in sync with FixedGrid above, where it makes sense.
    const OrientableGrid = struct {
        height: usize,
        width: usize,
        baseIndex: usize,
        rowStride: isize,
        colStride: isize,
        data: DataT,
        allocator: AllocatorT = allocatorNull,

        const Self = @This();

        fn initUnowned(height: usize, width: usize, stride: usize, data: DataT) Self {
            return .{
                .height = height,
                .width = width,
                .baseIndex = 0,
                .rowStride = @as(isize, @intCast(stride)),
                .colStride = 1,
                .data = data,
            };
        }

        // We could/should also support initOwned() and initAlloc() like
        // FixedGrid does, but currently there is no use case for it.

        pub fn initFromText(text: []const u8) !Self {
            const grid = try TextGrid.initFromText(text);
            return Self.initUnowned(grid.height, grid.width, grid.stride, grid.dataSlice());
        }

        pub fn deinit(self: Self) void {
            std.debug.assert(self.allocator != null);
            if (self.allocator) |a| a.free(self.data);
        }

        pub fn charAt(self: Self, row: usize, col: usize) T {
            return self.charPtrAt(row, col).*;
        }

        pub fn charPtrAt(self: Self, row: usize, col: usize) PtrT {
            return &self.data[self._idx(row, col)];
        }

        pub fn charAtPos(self: Self, pos: Coords) T {
            return self.charPtrAtPos(pos).*;
        }

        pub fn charPtrAtPos(self: Self, pos: Coords) PtrT {
            return self.charPtrAt(pos.r, pos.c);
        }

        pub fn isEqualTo(self: Self, other: anytype) bool {
            return compareGrids(self, other);
        }

        fn _idx(self: Self, row: usize, col: usize) usize {
            std.debug.assert(row < self.height and col < self.width);
            return @as(usize, @intCast(@as(isize, @intCast(self.baseIndex)) +
                @as(isize, @intCast(row)) * self.rowStride +
                @as(isize, @intCast(col)) * self.colStride));
        }

        pub fn transposed(self: Self) Self {
            return .{
                .height = self.width,
                .width = self.height,
                .baseIndex = self._idx(0, 0),
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
                .baseIndex = self._idx(0, self.width - 1),
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
                .baseIndex = self._idx(self.height - 1, 0),
                .rowStride = self.colStride,
                .colStride = -self.rowStride,
                .data = self.data,
                .allocator = self.allocator,
            };
        }

        // Creates a mutable copy of the current grid. Must be freed by calling deinit().
        pub fn duplicate(
            self: Self,
            comptime mutability: Mutability,
            allocator: std.mem.Allocator,
        ) !Grid(T, config.setOwnability(.ownable).setMutability(mutability)) {
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
    };

    return switch (config.orientability) {
        .fixed => FixedGrid,
        .orientable => OrientableGrid,
    };
}

pub const TextGrid = Grid(u8, .{});
