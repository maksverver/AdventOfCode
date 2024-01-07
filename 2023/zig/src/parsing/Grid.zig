// Keep this in sync with grids.zig

const findNewline = @import("./text.zig").findNewline;
const std = @import("std");

height: usize,
width: usize,
stride: usize,
data: [*]const u8,

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

pub const Coords = struct {
    r: usize,
    c: usize,
};

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

pub fn move(self: Grid, pos: Coords, dir: Dir, dist: usize) ?Coords {
    return switch (dir) {
        .n => if (pos.r >= dist) .{ .r = pos.r - dist, .c = pos.c } else null,
        .e => if (self.width - pos.c > dist) .{ .r = pos.r, .c = pos.c + dist } else null,
        .s => if (self.height - pos.r > dist) .{ .r = pos.r + dist, .c = pos.c } else null,
        .w => if (pos.c >= dist) .{ .r = pos.r, .c = pos.c - dist } else null,
    };
}

pub fn moveBy(self: Grid, pos: Coords, dr: isize, dc: isize) ?Coords {
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

pub fn charAt(self: Grid, row: usize, col: usize) u8 {
    return self.charPtrAt(row, col).*;
}

pub fn charPtrAt(self: Grid, row: usize, col: usize) *const u8 {
    std.debug.assert(row < self.height and col < self.width);
    return &self.data[row * self.stride + col];
}

pub fn charAtPos(self: Grid, pos: Coords) u8 {
    return self.charPtrAtPos(pos).*;
}

pub fn charPtrAtPos(self: Grid, pos: Coords) *const u8 {
    return self.charPtrAt(pos.r, pos.c);
}
