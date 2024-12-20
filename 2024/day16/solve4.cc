// Similar to solve3.cc, but uses a priority queue to keep track of which
// distances are used in the bucket queue, so we can skip over empty entries.
//
// This changes the time complexity from O(n + d) to O(n + x log y) where
// d is the maximum distance visited, x is the number of distinct distances
// visited, and y is the average number of distances in the queue.
//
// It turns out that x log y isn't really smaller than d in practice.
// For maze-large.txt:
//
//  - Number of elements in the pq:         79.3 on average (log(79.3, 2) ~ 6.3 )
//  - Number of distinct distances:  4,208,490
//  - Maximum distance used:        20,718,422  (= the answer to part 1 + 1000)
//  - Number of elements pushed:    57,099,732
//
// log(79.3, 2) ~ 6.3, while 20,718,422 / 4,208,490 ~ 4.9, so the overhead from
// the priority queue is larger than the time saved, even ignoring constant
// factors.

#include <cassert>
#include <iostream>
#include <limits>
#include <queue>
#include <string_view>
#include <vector>

// For mmap:
#include "sys/mman.h"
#include "sys/stat.h"
#include "unistd.h"

static size_t FileSize(int fd) {
  struct stat st;
  int res = fstat(fd, &st);
  if (res != 0) {
    perror("fstat");
    exit(1);
  }
  return st.st_size;
}

constexpr int DR[4] = {  0, +1,  0, -1 };
constexpr int DC[4] = { +1,  0, -1,  0 };

using dist_t = int32_t;

struct QueueState {
    dist_t dist;
    int dir;
    size_t field_index;

    auto operator<=>(const QueueState &qs) const {
        return qs.dist <=> dist;
    }
};

constexpr dist_t move_cost = 1;
constexpr dist_t turn_cost = 1000;
constexpr dist_t max_cost = std::max(move_cost, turn_cost);

int main() {
    size_t size = FileSize(STDIN_FILENO);
    const char * const data = (const char*)mmap(NULL, size, PROT_READ, MAP_SHARED, STDIN_FILENO, 0);
    assert(data != MAP_FAILED);

    std::string_view s(data, size);
    const size_t W = s.find('\n');
    if (W == std::string_view::npos) {
        std::cerr << "Missing newline in input file!\n";
        return 1;
    }
    const size_t stride = W + 1;
    if (s.size() % stride != 0) {
        std::cerr << "Invalid input file size! (file size: " << size << "; first line length: " << W << ")\n";
        return 1;
    }

    size_t start = s.find('S');
    size_t end = s.find('E');
    if (start == std::string_view::npos) {
        std::cerr << "Missing start ('S')!\n";
        return 1;
    }
    if (end == std::string_view::npos) {
        std::cerr << "Missing end ('E')!\n";
        return 1;
    }

    // Dijkstra's algorithm
    auto dists = std::vector<dist_t>(s.size() * 4, std::numeric_limits<dist_t>::max());
    dist_t answer1 = std::numeric_limits<dist_t>::max();
    {
        std::priority_queue<dist_t, std::vector<dist_t>, std::greater<dist_t>> dist_todo;
        std::vector<std::pair<int, size_t>> todo[max_cost + 1];  // per dist: dir, vertex
        auto relax = [&](dist_t dist, int dir, size_t v) {
            dist_t &old_dist = dists[4*v + dir];
            if (dist < old_dist) {
                auto &buffer = todo[dist % (max_cost + 1)];
                if (buffer.empty()) dist_todo.push(dist);
                old_dist = dist;
                buffer.push_back({dir, v});
            }
        };
        relax(0, 0, start);
        while (!dist_todo.empty()) {
            dist_t cur_dist = dist_todo.top();
            dist_todo.pop();
            auto &cur = todo[cur_dist % (max_cost + 1)];
            for (auto [dir, v] : cur) {
                if (cur_dist > dists[4*v + dir]) continue;
                if (v == end) [[unlikely]] {
                    answer1 = cur_dist;
                    goto solved;
                }

                size_t w = v + DR[dir]*(ssize_t)stride + DC[dir];
                if (data[w] != '#') relax(cur_dist + move_cost, dir, w);
                relax(cur_dist + turn_cost, (dir + 1) & 3, v);
                relax(cur_dist + turn_cost, (dir + 3) & 3, v);
            }
            cur.clear();  // reuse later
        }
        std::cerr << "End not reachable!" << std::endl;
        return 1;
    }
solved:

    // Part 1: minimum distance to finish
    std::cout << answer1 << std::endl;

    // Part 2: find number of position in path from start to finish.
    auto seen = std::vector<char>(s.size() * 4, 0);
    {
        std::vector<QueueState> todo;
        auto Add = [&](dist_t dist, int dir, size_t v) {
            if (dists[4*v + dir] == dist && !seen[4*v + dir]) {
                seen[4*v + dir] = 1;
                todo.push_back(QueueState{dist, dir, v});
            }
        };
        for (int dir = 0; dir < 4; ++dir) Add(answer1, dir, end);
        for (size_t i = 0; i < todo.size(); ++i) {
            auto [dist_v, dir, v] = todo[i];
            Add(dist_v - 1, dir, v - DR[dir]*(ssize_t)stride - DC[dir]);
            Add(dist_v - 1000, (dir + 3) & 3, v);
            Add(dist_v - 1000, (dir + 1) & 3, v);
        }
    }
    size_t answer2 = 0;
    for (size_t i = 0; i < seen.size(); i += 4) {
        answer2 += seen[i] | seen[i + 1] | seen[i + 2] | seen[i + 3];
    }
    std::cout << answer2 << std::endl;
}
