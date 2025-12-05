#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdio>
#include <cinttypes>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

using namespace std::chrono;

struct Timer {
    Timer(const char *what) : what(what) {}

    ~Timer() {
        auto finish = high_resolution_clock::now();
        std::clog << what << " took " << duration_cast<microseconds>(finish - start) << '\n';
    }

    const char *what;
    high_resolution_clock::time_point start = high_resolution_clock::now();
};

using i64 = int64_t;

int main() {
    Timer timer("Everything");

    std::vector<std::pair<i64, i64>> ranges;
    std::vector<i64> ingredients;
    {
        Timer timer("Parsing");
        for (;;) {
            i64 l, r;
            int n = scanf("%" PRId64 "-%" PRId64, &l, &r);
            if (n == 2) {
                ranges.push_back({l, r + 1});
            } else if (n == 1) {
                ingredients.push_back(l);
                break;
            } else {
                fprintf(stderr, "Invalid input!\n");
                return 1;
            }
        }
        for (i64 i; scanf("%" PRId64 "d", &i) == 1;) {
            ingredients.push_back(i);
        }
    }
    assert(!ingredients.empty());

    // Merge ranges
    {
        Timer timer("Sorting ranges");
        std::ranges::sort(ranges);
    }
    if (!ranges.empty()) {
        Timer timer("Merging ranges");
        size_t i = 0;
        auto [l, r] = ranges[0];
        for (size_t j = 1; j < ranges.size(); ++j) {
            auto [l2, r2] = ranges[j];
            if (l2 <= r) {
                if (r2 > r) r = r2;
            } else {
                ranges[i++] = {l, r};
                l = l2;
                r = r2;
            }
        }
        ranges[i++] = {l, r};
        ranges.resize(i);
    }

    // Part 1
    {
        Timer timer("Part 1");
        i64 answer1 = 0;
        for (auto i : ingredients) {
            auto it = std::ranges::lower_bound(ranges, i, {}, [](std::pair<i64, i64> p) { return p.second; });
            if (it != ranges.end() && i > it->first) ++answer1;
        }
        std::cout << answer1 << '\n';
    }

    // Part 2
    {
        Timer timer("Part 2");
        i64 answer2 = 0;
        for (auto [l, r]: ranges) answer2 += r - l;
        std::cout << answer2 << '\n';
    }
}
