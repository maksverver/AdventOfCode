// More efficient version of solve4.cc that uses bitmasks to track empty sets.
// This allows us to skip empty buckets 64 at a time, which is at least a lot
// faster than doing it individually, and incurs less overhead when adding
// elements. Still, it's not faster than solve3.cc

#include <cassert>
#include <cstdint>
#include <iostream>
#include <limits>
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

// Should be unsigned so division/modulo operations are fast.
using dist_t = uint_fast32_t;

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

// Subtract max_cost because the implementation of part2 underflows.
constexpr dist_t max_dist = std::numeric_limits<dist_t>::max() - max_cost;


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
    auto dists = std::vector<dist_t>(s.size() * 4, max_dist);
    dist_t answer1 = max_dist;
    {
        using mask_t = uint_fast64_t;
        constexpr int mask_bits = 64;

        // Note: since we use 64-bits bit mask, max_cost (1001) must be rounded
        // up to a multiple of 64 (1024), and then we need to add another 64 to
        // avoid the annoying situation where lower bits of the mask we are
        // working on are getting set (1088). Then I rounded that up again to
        // the next power of 2 so modulo/division operations are efficient.
        constexpr int buffer_size = 2048;
        std::vector<std::pair<int, size_t>> todo[buffer_size];  // per dist: dir, vertex
        static_assert (buffer_size % mask_bits == 0);
        mask_t nonempty_masks[buffer_size / mask_bits] = {};
        dist_t max_dist = 0;
        auto relax = [&](dist_t dist, int dir, size_t v) {
            dist_t &old_dist = dists[4*v + dir];
            if (dist < old_dist) {
                auto &buffer = todo[dist % buffer_size];
                old_dist = dist;
                nonempty_masks[dist % buffer_size / mask_bits] |= mask_t{1} << (dist % mask_bits);
                buffer.push_back({dir, v});
            }
        };
        relax(0, 0, start);
        dist_t base_dist = 0;
        while (base_dist <= max_dist) {
            for (int chunk = 0; chunk < buffer_size / mask_bits; ++chunk) {
                mask_t &mask = nonempty_masks[chunk];
                while (mask) {
                    int lowest_bit_index = std::countr_zero(mask);
                    mask ^= mask_t{1} << lowest_bit_index;
                    dist_t dist = base_dist + mask_bits*chunk + lowest_bit_index;
                    max_dist = dist + max_cost;
                    auto &batch = todo[dist % buffer_size];
                    for (auto [dir, v] : batch) {
                        if (dist > dists[4*v + dir]) continue;
                        if (v == end) [[unlikely]] {
                            answer1 = dist;
                            goto solved;
                        }

                        size_t w = v + DR[dir]*(ssize_t)stride + DC[dir];
                        if (data[w] != '#') relax(dist + move_cost, dir, w);
                        relax(dist + turn_cost, (dir + 1) & 3, v);
                        relax(dist + turn_cost, (dir + 3) & 3, v);
                    }
                    batch.clear();  // reuse later
                }
            }
            base_dist += buffer_size;
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
            // Note: these subtractions may underflow.
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
