// Functions to define 2D grids of characters or other values, both owning and
// non-owning. This file probably does not belong in the parsing/ subdirectory
// because only a tiny part is related to input parsing.

const std = @import("std");
const findNewline = @import("./text.zig").findNewline;

// An orientable grid has methods to rotate and transpose in real time.
const Orientability = enum { fixed, orientable };

// A mutable grid returns non-const pointers to data, allowing the grid contents
// to be modified.
const Mutability = enum { readonly, mutable };

// An allocatable grid is one that can own a copy of its data. In that case it
// must be deinitialized by calling deinit(). Mostly useful for mutable grids.
const Allocatability = enum { unowned, allocatable };

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
    orientability: Orientability = .fixed,
    allocatability: Allocatability = .unowned,

    fn makeAllocatable(config: GridConfig) GridConfig {
        var res = config;
        res.allocatability = true;
        return res;
    }
};

pub fn Grid(comptime T: type, comptime config: GridConfig) type {

    // Currently StaticGrid doesn't support owning copies of its data. There is
    // no fundamental reason it couldn't; it just hasn't been implement yet.
    std.debug.assert(config.orientability == .orientable or config.allocatability == .unowned);

    const SliceT = if (config.mutability == .mutable) []T else []const T;
    const PtrT = if (config.mutability == .mutable) *T else *const T;
    const DataT = if (config.allocatability == .allocatable) SliceT else if (config.mutability == .mutable) [*]T else [*]const T;
    const AllocatorT = if (config.allocatability == .allocatable) ?std.mem.Allocator else void;
    const allocatorNull = if (config.allocatability == .allocatable) null else {};

    const StaticGrid = struct {
        height: usize,
        width: usize,
        stride: usize,
        data: DataT,

        const Self = @This();

        fn initUnowned(height: usize, width: usize, stride: usize, data: DataT) Self {
            return Self{
                .height = height,
                .width = width,
                .stride = stride,
                .data = data,
            };
        }

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

        pub fn charAt(self: Self, row: usize, col: usize) u8 {
            return self.charPtrAt(row, col).*;
        }

        pub fn charPtrAt(self: Self, row: usize, col: usize) PtrT {
            std.debug.assert(row < self.height and col < self.width);
            return &self.data[row * self.stride + col];
        }

        pub fn charAtPos(self: Self, pos: Coords) u8 {
            return self.charPtrAtPos(pos).*;
        }

        pub fn charPtrAtPos(self: Self, pos: Coords) PtrT {
            return self.charPtrAt(pos.r, pos.c);
        }

        pub fn indexOf(self: Self, ch: u8) !Coords {
            for (0..self.height) |r| {
                for (0..self.width) |c| {
                    if (self.charAt(r, c) == ch) return .{ .r = r, .c = c };
                }
            }
            return error.NotFound;
        }
    };

    const OrientableGrid = struct {
        height: usize,
        width: usize,
        baseIndex: usize,
        rowStride: isize,
        colStride: isize,
        data: SliceT,
        allocator: AllocatorT = allocatorNull,

        const Self = @This();

        // pub fn init(data: SliceT) !Self {
        //     return initInternal(data, null);
        // }

        // pub fn initUnowned()

        // Allocates a grid of the given dimensions. The result must be freed with deinit().
        // If `value` is not null, all elements are initialized to the given value, otherwise
        // they are left undefined.
        // pub fn initAlloc(allocator: std.mem.Allocator, height: usize, width: usize, value: ?T) !Self {
        //     var data = try allocator.alloc(T, width * height);
        //     if (value) |v| @memset(data, v);
        //     return Self{
        //         .height = height,
        //         .width = width,
        //         .baseIndex = 0,
        //         .rowStride = @as(isize, @intCast(width)),
        //         .colStride = 1,
        //         .data = data,
        //         .allocator = allocator,
        //     };
        // }

        // Like `init`, but `allocator` is used to free `data` in deinit().
        // pub fn initOwned(data: SliceT, allocator: std.mem.Allocator) !Self {
        //     return initInternal(data, allocator);
        // }

        // fn initInternal(data: SliceT, allocator: ?std.mem.Allocator) !Self {
        //     const firstNl = findNewline(data) orelse return error.MissingNewline;
        //     const width = firstNl.nl;
        //     const stride = firstNl.end;
        //     if (data.len % stride != 0) return error.InvalidSize;
        //     const height = data.len / stride;
        //     // This part is theoretically optional: it just verifies that the rest
        //     // of the file uses the same width and stride.
        //     var remaining = data[stride..];
        //     while (remaining.len > 0) {
        //         const nl = findNewline(remaining) orelse return error.MissingNewline;
        //         if (nl.nl != width or nl.end != stride) return error.InvalidInput;
        //         remaining = remaining[stride..];
        //     }
        //     std.debug.assert(height > 0);
        //     std.debug.assert(width > 0);
        //     return Self{
        //         .height = height,
        //         .width = width,
        //         .baseIndex = 0,
        //         .rowStride = @as(isize, @intCast(stride)),
        //         .colStride = 1,
        //         .data = data,
        //         .allocator = allocator,
        //     };
        // }

        pub fn deinit(self: Self) void {
            std.debug.assert(self.allocator != null);
            if (self.allocator) |a| a.free(self.data);
        }

        pub fn charAt(self: Self, row: usize, col: usize) T {
            return self.charPtrAt(row, col).*;
        }

        pub fn charPtrAt(self: Self, row: usize, col: usize) PtrT {
            return &self.data[self.idx(row, col)];
        }

        pub fn charAtPos(self: Self, pos: Coords) T {
            return self.charPtrAtPos(pos).*;
        }

        pub fn charPtrAtPos(self: Self, pos: Coords) PtrT {
            return self.charPtrAt(pos.r, pos.c);
        }

        fn idx(self: Self, row: usize, col: usize) usize {
            std.debug.assert(row < self.height and col < self.width);
            return @as(usize, @intCast(@as(isize, @intCast(self.baseIndex)) +
                @as(isize, @intCast(row)) * self.rowStride +
                @as(isize, @intCast(col)) * self.colStride));
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
        pub fn mutableCopy(self: Self, allocator: std.mem.Allocator) !Grid(T, config.makeAllocatable()) {
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
                    if (self.charAt(r, c) != other.charAt(r, c)) return false;
                }
            }
            return true;
        }
    };

    const GridT = if (config.orientability == .orientable) OrientableGrid else StaticGrid;
    return GridT;
}

pub const TextGrid = Grid(u8, .{});

// Initializes a grid by splitting `text` into lines. All lines must be of equal
// length. The result is a grid referencing an unowned copy of the input data.
pub fn parseTextGrid(text: []const u8) !TextGrid {
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
    return TextGrid.initUnowned(height, width, stride, text.ptr);
}
