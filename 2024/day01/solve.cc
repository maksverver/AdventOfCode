#include <algorithm>
#include <cstdio>
#include <cassert>
#include <chrono>
#include <iostream>
#include <unordered_map>
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
        long long x, y;
        while (scanf("%lld %lld\n", &x, &y) == 2) {
            a.push_back(x);
            b.push_back(y);
            ++n;
        }
        assert(feof(stdin));
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

    {
        Timer timer("Solving part 2");
        std::unordered_map<long long, long long> a_count;
        std::unordered_map<long long, long long> b_count;
        for (int x : a) a_count[x]++;
        for (int y : b) b_count[y]++;
        long long answer2 = 0;
        for (auto [x, n] : a_count) answer2 += n * x * b_count[x];
        std::cout << answer2 << std::endl;
    }
}
