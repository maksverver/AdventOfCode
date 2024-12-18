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
    dist_t answer1 = -1;
    {
        std::priority_queue<QueueState> todo;
        auto relax = [&](dist_t dist, int dir, size_t v) {
            dist_t &old_dist = dists[4*v + dir];
            if (dist < old_dist) {
                old_dist = dist;
                todo.push(QueueState{dist, dir, v});
            }
        };
        relax(0, 0, start);
        dists[4*start] = 0;
        while (!todo.empty()) {
            if (todo.empty()) [[unlikely]] {
            }
            auto [dist_v, dir, v] = todo.top();
            todo.pop();
            if (dist_v > dists[4*v + dir]) continue;
            if (v == end) [[unlikely]] {
                answer1 = dist_v;
                goto solved;
            }

            size_t w = v + DR[dir]*(ssize_t)stride + DC[dir];
            if (data[w] != '#') relax(dist_v + 1, dir, w);
            relax(dist_v + 1000, (dir + 1) & 3, v);
            relax(dist_v + 1000, (dir + 3) & 3, v);
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
