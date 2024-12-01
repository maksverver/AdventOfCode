// Solution that runs in O(n + max_val) time, where n is the number of lines
// of input, and max_val is the maximum value. This is better than O(n log n)
// when the values are relatively close to the number of lines.

#include <cstdio>
#include <cinttypes>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>

using namespace std::chrono;

struct Timer {
    Timer(const char *what) : what(what) {}

    ~Timer() {
        auto finish = high_resolution_clock::now();
        std::cerr << what << " took " << duration_cast<milliseconds>(finish - start) << '\n';
    }

    const char *what;
    high_resolution_clock::time_point start = high_resolution_clock::now();
};

int64_t GetMaximum(const std::vector<std::pair<int64_t,int64_t>> &v) {
    int64_t res = std::numeric_limits<int64_t>::min();
    for (auto [x, y] : v) res = std::max(res, std::max(x, y));
    return res;
}

int main() {
    std::vector<std::pair<int64_t,int64_t>> input;

    {
        Timer timer("Reading input");
        int64_t x, y;
        while (scanf("%" SCNd64 "%" SCNd64, &x, &y) == 2) input.push_back({x, y});
        assert(feof(stdin));
        assert(!input.empty());
    }

    int64_t max_val = 0;
    std::vector<int64_t> a;
    std::vector<int64_t> b;

    {
        Timer timer("Preprocessing");
        for (auto [x, y] : input) max_val = std::max(max_val, std::max(x, y));
        a.resize(max_val + 1);
        b.resize(max_val + 1);
        for (auto [x, y] : input) a[x]++, b[y]++;
    }

    {
        Timer timer("Solving part 1");
        int64_t answer1 = 0;
        int64_t delta = 0;
        for (int64_t x = 0; x <= max_val; ++x) {
            delta += a[x] - b[x];
            answer1 += std::abs(delta);
        }
        assert(delta == 0);
        std::cout << answer1 << std::endl;
    }

    {
        Timer timer("Solving part 2");
        int64_t answer2 = 0;
        for (int64_t x = 0; x <= max_val; ++x) answer2 += x * a[x] * b[x];
        std::cout << answer2 << std::endl;
    }
}
