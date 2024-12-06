#include <cassert>
#include <iostream>
#include <vector>
#include <set>
#include <string>
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
    std::set<Point> positions;
    {
        Point pos = start;
        int dir = 0;
        for (;;) {
            positions.insert(pos);
            auto next_pos = Step(pos, dir);
            if (!next_pos.InBounds()) break;
            if (next_pos.Blocked()) {
                dir = (dir + 1) % 4;
            } else {
                pos = next_pos;
            }
        }
        std::cout << positions.size() << std::endl;
    }

    // Part 2 (straightforward)
#if 0
    long long answer2 = 0;
    for (Point blocked : positions) if (blocked != start) {
        assert(grid[blocked.r][blocked.c] == '.');
        grid[blocked.r][blocked.c] = '#';
        std::set<std::pair<Point, int>> states;
        Point pos = start;
        int dir = 0;
        for (;;) {
            if (!states.insert({pos, dir}).second) {
                // Already visited. Loop detected!
                answer2++;                
                break;
            }
            auto next_pos = Step(pos, dir);
            if (!next_pos.InBounds()) {
                // Outside reached. No loop!
                break;
            }
            if (next_pos.Blocked()) {
                dir = (dir + 1) % 4;
            } else {
                pos = next_pos;
            }
        }
        grid[blocked.r][blocked.c] = '.';

    }
    std::cout << answer2 << std::endl;
#endif

    // Part 2 (optimized)
    //
    // Store the position of the blocks in a sorted set per row and column.
    // That way, we can find the next block in any direction in O(log n) time,
    // where n is the number of blocks in the row/column.
    long long answer2 = 0;
    std::vector<std::set<int>> blocks_per_row(H);
    std::vector<std::set<int>> blocks_per_col(W);
    for (int r = 0; r < H; ++r) {
        for (int c = 0; c < W; ++c) {
            if (grid[r][c] == '#') {
                blocks_per_row[r].insert(c);
                blocks_per_col[c].insert(r);
            }
        }
    }
    // Keep outside the loop to avoid reallocating memory, for a small performance boost.
    std::unordered_set<unsigned> seen_states;
    for (Point blocked : positions) if (blocked != start) {
        blocks_per_row[blocked.r].insert(blocked.c);
        blocks_per_col[blocked.c].insert(blocked.r);
        auto [r, c] = start;
        seen_states.clear();
        for (;;) {
            // We could do this after every step, but it's actually faster not to.
            if (!seen_states.insert(r * W + c).second) goto loop;
            // up
            {
                auto it = blocks_per_col[c].lower_bound(r);
                if (it == blocks_per_col[c].begin()) goto outside;
                r = *--it + 1;
            }
            // right
            {
                auto it = blocks_per_row[r].lower_bound(c);
                if (it == blocks_per_row[r].end()) goto outside;
                c = *it - 1;
            }
            // down
            {
                auto it = blocks_per_col[c].lower_bound(r);
                if (it == blocks_per_col[c].end()) goto outside;
                r = *it - 1;
            }
            // left
            {
                auto it = blocks_per_row[r].lower_bound(c);
                if (it == blocks_per_row[r].begin()) goto outside;
                c = *--it + 1;
            }
        }
    loop:
        answer2++;
    outside:
        blocks_per_row[blocked.r].erase(blocked.c);
        blocks_per_col[blocked.c].erase(blocked.r);
    }
    std::cout << answer2 << std::endl;
}
