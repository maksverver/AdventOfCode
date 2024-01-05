const std = @import("std");

/// Wrapper around std.testing.expectEqual() that fixes two problems:
///
///   - Moves the `expected` argument to the end, which reads more naturally.
///     (compare `if (foo() == 42)` with `if (42 == foo())` which is weird.)
///
///   - Lets the expected type to be inferred from the actual type, instead of the
///     other way around. This leads to more readable code because it allows
///     comptime ints and strings to be coerced to the expected type. It's still
///     possible to explicitly cast the expected value with e.g. `@as(u8, 42)`,
///     but usually it's not necessary or even desired to verify the exact type
///     in a unit test.
///
pub fn expectEqual(actual: anytype, expected: @TypeOf(actual)) !void {
    return std.testing.expectEqual(expected, actual);
}

/// Convenience method that checks if two strings are equal.
pub fn expectEqualString(actual: []const u8, expected: []const u8) !void {
    if (!std.mem.eql(u8, actual, expected)) {
        std.debug.print("expected {s}, found {s}\n", .{ expected, actual });
        return error.TestExpectedEqual;
    }
}

/// Convenience method that checks if two optional strings are equal.
pub fn expectEqualOptionalString(actual: ?[]const u8, expected: ?[]const u8) !void {
    if (actual) |a| {
        if (expected) |e| {
            if (!std.mem.eql(u8, a, e)) {
                std.debug.print("expected {s}, found {s}\n", .{ e, a });
                return error.TestExpectedEqual;
            }
        }
    }
    if ((actual == null) != (expected == null)) {
        std.debug.print("expected {?s}, found {?s}\n", .{ expected, actual });
        return error.TestExpectedEqual;
    }
}

/// Convenience method that checks if twos slices of strings are equal.
pub fn expectEqualStringSlice(actual: []const []const u8, expected: []const []const u8) !void {
    try expectEqual(actual.len, expected.len);
    for (actual, expected) |s, t| {
        try expectEqualString(s, t);
    }
}
