// Optimized version of solve.cc that runs part in O(n) time but without
// an axiliary data structure, instead scanning the sorted arrays only once.
//
// This still takes O(n log n) for part 1, where the sorting happens.

#include <algorithm>
#include <cassert>
#include <chrono>
#include <iostream>
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

int main() {
    std::vector<long long> a;
    std::vector<long long> b;
    size_t n = 0;

    {
        Timer timer("Reading input");
        std::ios_base::sync_with_stdio(false);
        std::cin.tie(nullptr);
        long long x, y;
        while (std::cin >> x >> y) {
            a.push_back(x);
            b.push_back(y);
            ++n;
        }
        assert(std::cin.eof());
    }

    {
        Timer timer("Solving part 1");
        std::ranges::sort(a);
        std::ranges::sort(b);
        long long answer1 = 0;
        for (size_t i = 0; i < n; ++i) {
            answer1 += std::abs(a[i] - b[i]);
        }
        std::cout << answer1 << std::endl;
    }

    // Needed for part 2.
    assert(std::ranges::is_sorted(a));
    assert(std::ranges::is_sorted(b));

    {
        Timer timer("Solving part 2");
        long long answer2 = 0;
        size_t i = 0, j = 0;
        while (i < n && j < n) {
            long long x = a[i];
            size_t old_i = i;
            do ++i; while (i < n && a[i] == x);
            while (j < n && b[j] < x) ++j;
            size_t old_j = j;
            while (j < n && b[j] <= x) ++j;
            answer2 += x * (j - old_j) * (i - old_i);
        }
        std::cout << answer2 << std::endl;
    }
}
