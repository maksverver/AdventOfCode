#include <cassert>
#include <iostream>
#include <vector>
#include <map>
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

#if 0
    // Part 2 (straightforward)
    long long answer2 = 0;
    for (auto [blocked, dir] : todo) if (blocked != start) {
        assert(grid[blocked.r][blocked.c] == '.');
        grid[blocked.r][blocked.c] = '#';
        std::set<std::pair<Point, int>> states;
        Point pos = {blocked.r - DR[dir], blocked.c - DC[dir]};
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

#if 1
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
    #pragma omp parallel for firstprivate(blocks_per_row, blocks_per_col, seen_states) shared(answer2)
    for (size_t i = 0; i < todo.size(); ++i) {
        auto [blocked, dir] = todo[i];
        if (blocked == start) continue;
        blocks_per_row[blocked.r].insert(blocked.c);
        blocks_per_col[blocked.c].insert(blocked.r);
        int r = blocked.r - DR[dir];
        int c = blocked.c - DC[dir];
        seen_states.clear();
        switch ((dir + 1) % 4) {
            for (;;) {
                // We could do this after every step, but it's actually faster not to.
                if (!seen_states.insert(r * W + c).second) goto loop;
                // up
                case 0: {
                    auto it = blocks_per_col[c].lower_bound(r);
                    if (it == blocks_per_col[c].begin()) goto outside;
                    r = *--it + 1;
                }
                // right
                case 1: {
                    auto it = blocks_per_row[r].lower_bound(c);
                    if (it == blocks_per_row[r].end()) goto outside;
                    c = *it - 1;
                }
                // down
                case 2: {
                    auto it = blocks_per_col[c].lower_bound(r);
                    if (it == blocks_per_col[c].end()) goto outside;
                    r = *it - 1;
                }
                // left
                case 3: {
                    auto it = blocks_per_row[r].lower_bound(c);
                    if (it == blocks_per_row[r].begin()) goto outside;
                    c = *--it + 1;
                }
            }
        }
    loop:
        #pragma omp critical
        answer2++;
    outside:
        blocks_per_row[blocked.r].erase(blocked.c);
        blocks_per_col[blocked.c].erase(blocked.r);
    }
    std::cout << answer2 << std::endl;
#endif
}
