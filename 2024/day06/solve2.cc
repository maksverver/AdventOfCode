// Faster version of solve.cc that caches the nearest block in each of the four
// directions in an array instead of a std::set<>, so lookups are O(1) instead
// of O(log (H + W)). However, this comes at the cost of more expensive insertion
// of obstacles (potentially up to O(H + W), instead of O(log (H + W)) before).
// Seems to be somewhat faster in practice, at least on my own test cases.

#include <cassert>
#include <iostream>
#include <set>
#include <string>
#include <vector>
#include <utility>
#include <unordered_set>

namespace {

const int DR[4] = { -1,  0, +1,   };
const int DC[4] = {  0, +1,  0, -1};

std::vector<std::string> grid;
int H, W;

struct Point {
    int r, c;

    bool InBounds() const {
        return 0 <= r && r < H && 0 <= c && c < W;
    }

    bool Blocked() const {
        return grid[r][c] == '#';
    }

    bool operator==(const Point &) const = default;
    auto operator<=>(const Point &) const = default;
};

Point start;

Point Step(Point p, int dir) {
    return Point{p.r + DR[dir], p.c + DC[dir]};
}

}  // namespace

int main() {
    std::string line;
    while (std::cin >> line) {
        grid.push_back(line); 
    }

    H = grid.size();
    W = grid[0].size();
    for (int r = 0; r < H; ++r) {
        for (int c = 0; c < W; ++c) {
            if (grid[r][c] == '^') {
                start.r = r;
                start.c = c;
            }
        }
    }

    // Part 1 (straightforward)
    std::vector<std::pair<Point, int>> todo;
    {
        std::set<Point> seen;
        Point pos = start;
        int dir = 0;
        for (;;) {
            if (seen.insert(pos).second) {
                todo.push_back({pos, dir});
            }
            auto next_pos = Step(pos, dir);
            if (!next_pos.InBounds()) break;
            if (next_pos.Blocked()) {
                dir = (dir + 1) % 4;
            } else {
                pos = next_pos;
            }
        }
    }
    std::cout << todo.size() << std::endl;

#if 1
    // Part 2 (optimized)
    //
    // Store the position of the blocks in a sorted set per row and column.
    // That way, we can find the next block in any direction in O(log n) time,
    // where n is the number of blocks in the row/column.
    long long answer2 = 0;
    std::vector<std::vector<int>> nearest_top   (H, std::vector<int>(W));
    std::vector<std::vector<int>> nearest_right (H, std::vector<int>(W));
    std::vector<std::vector<int>> nearest_bottom(H, std::vector<int>(W));
    std::vector<std::vector<int>> nearest_left  (H, std::vector<int>(W));

    for (int c = 0; c < W; ++c) {
        int last = -1;
        for (int r = 0; r < H; ++r) {
            nearest_top[r][c] = last;
            if (grid[r][c] == '#') last = r;
        }
    }
    for (int r = 0; r < H; ++r) {
        int last = -1;
        for (int c = 0; c < W; ++c) {
            nearest_left[r][c] = last;
            if (grid[r][c] == '#') last = c;
        }
    }
    for (int c = 0; c < W; ++c) {
        int last = H;
        for (int r = H - 1; r >= 0; --r) {
            nearest_bottom[r][c] = last;
            if (grid[r][c] == '#') last = r;
        }
    }
    for (int r = 0; r < H; ++r) {
        int last = W;
        for (int c = W - 1; c >= 0; --c) {
            nearest_right[r][c] = last;
            if (grid[r][c] == '#') last = c;
        }
    }

    // Keep outside the loop to avoid reallocating memory, for a small performance boost.
    std::unordered_set<unsigned> seen_states;
    #pragma omp parallel for firstprivate(nearest_left, nearest_right, nearest_top, nearest_bottom, seen_states) shared(answer2)
    for (size_t i = 0; i < todo.size(); ++i) {
        auto [blocked, dir] = todo[i];
        if (blocked == start) continue;

        auto [br, bc] = blocked;
        int r = br - DR[dir];
        int c = bc - DC[dir];

        // Early-out: check if turning at the current position would immediately
        // lead to exiting the loop. If so, there is no point in updating the
        // grid with the new obstacle. This doesn't seem to speed up the solution
        // in practice, so it's disabled.
        if (false) {
            switch ((dir + 1) % 4) {
                case 0: if (nearest_top[r][c] < 0) continue; break;
                case 1: if (nearest_right[r][c] >= W) continue; break;
                case 2: if (nearest_bottom[r][c] >= H) continue; break;
                case 3: if (nearest_left[r][c] < 0) continue; break;
            }
        }

        int r_top = nearest_top[br][bc];
        int c_left = nearest_left[br][bc];
        int r_bottom = nearest_bottom[br][bc];
        int c_right = nearest_right[br][bc];

        if (true) {
            // We need to insert the new block in the nearest_-arrays, updating all the cells
            // above, right, below and left of the blocked cell, up to the next blocked cell,
            // or the end of the grid.
            //
            //  .....#.......
            //  .....|.......
            //  .....|.......
            //  .....|.......
            //  -----X---#..#
            //  .....|.......
            //  .....|.......
            //
            for (int r = r_top + 1; r < br; ++r) nearest_bottom[r][bc] = br;
            for (int c = bc + 1; c < c_right; ++c) nearest_left[br][c] = bc;
            for (int r = br + 1; r < r_bottom; ++r) nearest_top[r][bc] = br;
            for (int c = c_left + 1; c < bc; ++c) nearest_right[br][c] = bc;
        } else {
            // The above routine can be optimized by observing that in the
            // simulation below, the guard can only come towards the obstacle
            // after hitting a block that lies just one space off one of the
            // lines drawn above:
            //
            //  .....#....
            //  ..........
            //  .....c#...
            //  ..........
            //  .....Xa.b#
            //  ......#.#.
            //  ..........
            //
            // For example, if the guard approaches point `a` or `b` from above,
            // then he turns right towards the new block X, but if he's moving
            // down the column between `a` and `b` he will never hit X.
            //
            // Similarly, if the guard moves towards c from the left, then he
            // hits an obstacle, turns right, and hits X from above.
            //
            // This means we only need to update cells a, b, c etc. and we can
            // use the nearest_-arrays to look up the relevant cells.
            //
            // Although this updates strictly fewer cells, the logic is
            // apparently slower in practice, which is why this is disabled by
            // default.
            if (bc + 1 < W) {
                for (int r = nearest_top[br][bc + 1]; r > r_top; r = nearest_top[r][bc + 1]) {
                    nearest_bottom[r][bc] = br;
                }
            }
            if (br + 1 < H) {
                for (int c = nearest_right[br + 1][bc]; c < c_right; c = nearest_right[br + 1][c]) {
                    nearest_left[br][c] = bc;
                }
            }
            if (bc > 0) {
                for (int r = nearest_bottom[br][bc - 1]; r < r_bottom; r = nearest_bottom[r][bc - 1]) {
                    nearest_top[r][bc] = br;
                }
            }
            if (br > 0) {
                for (int c = nearest_left[br - 1][bc]; c > c_left; c = nearest_left[br - 1][c]) {
                    nearest_right[br][c] = bc;
                }
            }
        }

        seen_states.clear();
        switch ((dir + 1) % 4) {
            for (;;) {
                // We could do this after every step, but it's actually faster not to.
                if (!seen_states.insert(r * W + c).second) goto loop;
                // up
                case 0:
                    r = nearest_top[r][c] + 1;
                    if (r == 0) goto outside;
                // right
                case 1:
                    c = nearest_right[r][c] - 1;
                    if (c == W - 1) goto outside;
                // down
                case 2:
                    r = nearest_bottom[r][c] - 1;
                    if (r == H - 1) goto outside;
                // left
                case 3:
                    c = nearest_left[r][c] + 1;
                    if (c == 0) goto outside;
            }
        }
    loop:
        #pragma omp critical
        answer2++;
    outside:

        if (true) {
            for (int r = r_top + 1; r < br; ++r) nearest_bottom[r][bc] = r_bottom;
            for (int c = bc + 1; c < c_right; ++c) nearest_left[br][c] = c_left;
            for (int r = br + 1; r < r_bottom; ++r) nearest_top[r][bc] = r_top;
            for (int c = c_left + 1; c < bc; ++c) nearest_right[br][c] = c_right;
        } else {
            if (bc + 1 < W) {
                for (int r = nearest_top[br][bc + 1]; r > r_top; r = nearest_top[r][bc + 1]) {
                    nearest_bottom[r][bc] = r_bottom;
                }
            }
            if (br + 1 < H) {
                for (int c = nearest_right[br + 1][bc]; c < c_right; c = nearest_right[br + 1][c]) {
                    nearest_left[br][c] = c_left;
                }
            }
            if (bc > 0) {
                for (int r = nearest_bottom[br][bc - 1]; r < r_bottom; r = nearest_bottom[r][bc - 1]) {
                    nearest_top[r][bc] = r_top;
                }
            }
            if (br > 0) {
                for (int c = nearest_left[br - 1][bc]; c > c_left; c = nearest_left[br - 1][c]) {
                    nearest_right[br][c] = c_right;
                }
            }
        }
    }
    std::cout << answer2 << std::endl;
#endif
}
