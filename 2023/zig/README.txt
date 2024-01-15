Solutions to Advent of Code 2023 (https://adventofcode.com/2023/)
implemented in Zig (https://ziglang.org/).


## Solution times

Running on an Intel(R) Core(TM) i7-7560U CPU @ 2.40GHz (single threaded)

╔═════╤════════╤════════╤═════════╤═════════╤═════════╤═════════╤═════════╗
║ Day │ Part 1 │ Part 2 │Time (ms)│ Parsing │ Solve 1 │ Solve 2 │ Solving ║
╟─────┼────────┼────────┼─────────┼─────────┼─────────┼─────────┼─────────╢
║   1 │ OK     │ OK     │   0.155 │   0.050 │   0.033 │   0.072 │       - ║
║   2 │ OK     │ OK     │   0.045 │       - │       - │       - │   0.045 ║
║   3 │ OK     │ OK     │   0.290 │   0.012 │   0.240 │   0.033 │       - ║
║   4 │ OK     │ OK     │   0.125 │   0.116 │       - │       - │   0.009 ║
║   5 │ OK     │ OK     │   0.153 │   0.086 │   0.009 │   0.012 │       - ║
║   6 │ OK     │ OK     │   0.028 │   0.011 │   0.007 │   0.001 │       - ║
║   7 │ OK     │ OK     │   0.450 │   0.203 │   0.134 │   0.108 │       - ║
║   8 │ OK     │ OK     │   0.569 │   0.281 │   0.049 │   0.223 │       - ║
║   9 │ OK     │ OK     │   0.220 │       - │       - │       - │   0.206 ║
║  10 │ OK     │ OK     │   0.134 │   0.012 │       - │       - │   0.123 ║
║  11 │ OK     │ OK     │   0.040 │   0.012 │       - │       - │   0.028 ║
║  12 │ OK     │ OK     │   2.802 │       - │       - │       - │   2.764 ║
║  13 │ OK     │ OK     │   0.094 │       - │       - │       - │   0.094 ║
║  14 │ OK     │ OK     │  10.623 │   0.066 │   0.061 │  10.487 │       - ║
║  15 │ OK     │ OK     │   0.699 │   0.019 │   0.086 │   0.593 │       - ║
║  16 │ OK     │ OK     │  36.902 │   0.014 │   0.894 │  35.835 │       - ║
║  17 │ OK     │ OK     │  16.596 │   0.018 │   7.380 │   9.198 │       - ║
║  18 │ OK     │ OK     │   0.080 │       - │       - │       - │   0.080 ║
║  19 │ OK     │ OK     │   0.243 │   0.202 │   0.018 │   0.023 │       - ║
║  20 │ OK     │ OK     │   1.788 │   0.085 │   0.534 │   1.142 │       - ║
║  21 │ OK     │ OK     │   0.552 │   0.013 │   0.513 │   0.016 │       - ║
║  22 │ OK     │ OK     │   0.338 │   0.313 │   0.010 │   0.012 │       - ║
║  23 │ OK     │ OK     │ 140.609 │   0.012 │   0.303 │ 140.294 │       - ║
║  24 │ OK     │ OK     │   0.709 │   0.227 │   0.470 │   0.007 │       - ║
║  25 │ OK     │ -      │   0.562 │   0.427 │   0.133 │       - │       - ║
╚═════╧════════╧════════╧═════════╧═════════╧═════════╧═════════╧═════════╝
Total time: 219.884 ms


## Requirements

These solutions require Zig to be installed. They were written for Zig 0.11.0.
To check which version of Zig is installed, run;

% zig version
0.11.0


## Running

To build and run all solutions on the official test data:

% zig build run                             (runs in debug mode)
% zig build run -Doptimize=ReleaseFast      (runs with optimizations)

To run only some solutions, or the same solution multiple times (which is useful
for benchmarking):

% zig build run -Doptimize=ReleaseFast -- 7 7 7

The last-built executable is written to zig-out/bin/aoc, which can be run with:

% time zig-out/bin/aoc


## Testing

To run all tests:

% zig build test

Or with slightly more information:

% zig build test --summary all


## Individual days

Individual days can be run with:

% zig run src/day1.zig < input.txt

And tested with:

% zig test src/day1.zig

Days can also be compiled into stand-alone executables which read from stdin and
write answers to stdout:

% zig build-exe -O ReleaseFast src/day1.zig
% time ./day1 < ../testdata/01.in


## Some interesting solutions

 - src/day11.zig (runs really fast!)
 - src/day14.zig (clever algorithm)
 - src/day17.zig (Dijkstra's algorithm)
 - src/day18.zig (combines parsing with solving)
 - src/day19.zig (normalizes input while parsing)
 - src/day20.zig (implements polymorphism with a tagged union)
 - src/day22.zig (clever algorithm)
 - src/day25.zig (graph builder)


## Observations about Zig

Zig is a low level systems programming language, so it is not an obvious choice
for a high-level problem solving challenge like Advent of Code. I used Zig
because I wanted to learn the language, and because I was curious how much
performance I could gain compared to my earlier Python solutions (see the parent
directory).

I experimented with different approaches for different problems (e.g., using an
imperative search with an ArrayList in one case, and using recusion in another
case). I optimized some solutions for speed at the expense of clarity, while
not bothering to optimize others. I added utility functions for some recurring
work, mostly input parsing, but did not always go back to retrofit them to
previously-implemented solutions. I tried to make memory allocations correct,
ensuring that memory leaks cannot occur. In a few cases I used the
ArenaAllocator and didn't bother releasing memory at all (which often also helps
with performance).

All in all, I think the Zig code I wrote is reasonable, but likely not the
cleanest and most idiomatic possible. However, I did manage to solve all
problems and I learned a few things about Zig along the way. Below is a summary
of my observations.


Positives:

  - The zig command line tool is easy to use.

  - Zig integrates nicely into Visual Studio Code, with syntax highlighting and
    code completion thanks to the Zig Language Server (zls).

  - Zig binaries often run very fast! Sometimes faster than efficient
    implementations in other fast languages like C++ or Rust.

  - Zig encourages unit testing by making it really easy to interleave tests
    with implementation code, and easy to build and run those tests.

    (Caveat: I struggled a little with refAllDeclsRecursive() to make sure all
    unit tests were included in `zig build test`.)

  - comptime evaluation is neat! It makes generics easy to read and write, and
    is pretty powerful. (For example, see src/parsing/grids.zig)

  - The raw string syntax (\\) is novel and useful. It allows code to be
    indented while preserving whitespace in the string itself.

  - Runtime checks in debug mode help detecting bugs early. This includes
    detecting computational errors like integer overflow, accessing empty
    optionals, and even detecting memory leaks.

  - Executables have low memory overhead. This is because a minimal Zig program
    doesn't use many resources, and because there is considerable friction to
    memory allocation (you need an allocator, you need to handle
    error.OutOfMemory, and you need to ensure memory is freed correctly) the
    language encourages authors to use dynamic allocations only when strictly
    necessary.


Negatives:

  - Integer conversions are annoying.

    While modern languages like Java typically make integers signed by default,
    Zig chooses to use `usize` wherever possible, which means you cannot
    subtract values or add negative values and then compare them against bounds
    (e.g. an expression like (r + dr >= 0) causes integer underflow).

    I wonder if it would be better if containers used a shorter length, e.g.
    u63 on 64-bit platforms, which can be safely converted to both i64 and u64.

    On the other hand, I was sometimes able to rewrite my code in a way that
    avoided integer conversions (for example, replacing (r - dist >= 0) with
    (r >= dist) in Grid.move()), so maybe I just need more practice with Zig.

  - It's annoying that ranges are always usized. I feel like I should be able
    to write `for (a..b) |x| {..}` and have `x` be of the same type as a and b.
    Similarly, why can't I use negative values? Or ranges that go from high down
    to low?

  - GeneralPurposeAllocator is pretty slow! ArenaAlocator is much faster, but
    often still much slower than the libc-based allocators, of which glibc is
    significantly faster than musl libc. For example: src/day17.zig

  - AutoHashTable is pretty slow compared to other languages, even interpreted
    ones like Python. This is probably partially due to allocators being slow in
    general, but they are also slow when reserving capacity up-front.

  - Correct error handling feels really error prone, especially when dealing
    with memory allocations. For example, it's easy to mistakenly write:

      try matrix.append(try row.toOwnedSlice())

    which leaks memory if the second allocation fails. And it's easy to
    accidentally free dangling pointers, for example:

      var array = try allocator.alloc([]usize, 10);
      errdefer allocator.free(array);
      errdefer for (array) |p| allocator.free(p);
      for (array) |*p| p.* = try allocator.alloc(array);

    Both of these errors are hard to detect since they only occur when some but
    not all of the allocations fail, which is rare.

    I think tooling could help to detect some of these bugs. For example, it
    should be possible to automatically rerun a unit test with allocations
    failing at different points.

    On the implementation side I found that wrappers like ArrayList can help, in
    that they make it easier to build deeply nested data structures correctly,
    but at the cost that they are harder to access: compare
    list.items[1].items[2] with array[1][2].

  - On the topic of allocations, it's kind of annoying that there is no deep
    ownership concept. Maybe there should be a version of ArrayList that calls
    deinit() (for structs) or free() (for slices) or destroy() (for pointers) on
    its elements when it's deinited?

  - Compiler error messages weren't always very clear. Often the compiler error
    didn't seem to include any part the code that caused the error. For example:

        pub fn main() void {
          std.debug.print("{}\n", 42);
        }

    Currently generates the following error message:

        /usr/lib/zig/std/fmt.zig:87:9: error: expected tuple or struct argument, found comptime_int
        @compileError("expected tuple or struct argument, found " ++ @typeName(ArgsType));
        ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    With no reference to the source line in main(). This is not a problem in
    this small example, but in a large file it can be quite difficult to figure
    out which line caused the error. My only workaround so far is to build and
    test early and often, so the number of changed lines is small enough to be able to
    quickly spot the culprit.

  - Relative imports can't access source files outside the current subdirectory
    tree. I know the correct solution is to bundle subdirectories into named
    packages, but that prevents `zig run src/bla.zig` and require to go through
    `zig build` instead, which is considerably slower, and requires all targets
    to be explicitly declared (which would be particularly annoying for Advent
    of Code, where there are essentially 25 separate binaries).


Although this looks like a lot of negatives, the majority are not intrinsic to
the language (e.g., slow allocators, confusing compiler errors) so they will
likely improve as the language and its implementation matures.

Neutral observations about solving the Advent of Code problems in Zig:

  - Writing parsing code is quite tricky, especially if you want to build
    complex data structures dynamically, and even more so if you want to handle
    deallocation in the case of errors 100% correctly.

    For many problems, parsing the input was the hardest part, in every sense:
    the most complex to write, taking up the most lines of code, and taking most
    time when run.

    I found the Builder pattern useful to make input parsing more manageable,
    where the Builder's interface serves as an abstraction between the input
    file syntax and the logical structure of the input.

    For examples, see src/day8.zig, src/day20.zig, or src/day25.zig.

  - Zig does not offer a native form of polymorphism. There are a few options:

      1. A generic function that takes one or more comptime function values.

      2. A generic function that takes a comptime struct type, which must have
         some methods. The downside of that approach is that Zig has no way to
         express the interface of the struct (it will be just “anytype”), unlike
         e.g. C++ concepts or Rust traits.

      3. A runtime function that accepts a runtime function pointer, possibly
         with a context pointer. This is used extensively by the standard
         library, e.g. for custom comparisons when sorting. I used it for the
         parse() callback in the Environment.parseInput() family of functions.

      4. Open interfaces with a vtable. This is how std.mem.Allocator works.
         I did not use this for AOC but it seems generally useful.

      5. Closed interfaces by putting different types in a tagged enum. This can
         in theory be very efficient. I used this in src/day20.zig (see
         ModuleState.process()), where it worked really well since the number of
         different types of modules is small and fixed.

    Overall, I didn't find the lack of language support for polymorphism
    problematic, but then again, Advent of Code problems are relatively small
    and independent. It's possible this does become a problem for larger
    projects.


EOF
