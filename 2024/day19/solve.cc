// Advent of Code 2024 Day 19: Linen Layout
//
// Solution using iterative dynamic programming to count strings.
//
// However, it uses s.ends_with() inside the loop, which can take time
// proportional to the length of the pattern to find a match. Therefore the
// algorithm is quadratic in time, worst case.
//
// More accurately, the time complexity is O(nm) where m is the number of
// pattern characters (i.e., the sum of the length of the patterns,
// approximately the length of the first line) and m is the number of target
// characters (i.e., the size of the rest of the file).

#include <cstdint>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

static int64_t Solve(const std::vector<std::string> &patterns, std::string_view target) {
    std::vector<int64_t> count(target.size() + 1);
    count[0] = 1;
    for (size_t i = 1; i <= target.size(); ++i) {
        auto t = target.substr(0, i);
        for (const auto &s : patterns) {
            if (t.ends_with(s)) {
                count[i] += count[i - s.size()];
            }
        }
    }
    return count[target.size()];
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<std::string> patterns;
    for (bool last = false; !last; ) {
        std::string pattern;
        if (!(std::cin >> pattern) || pattern.empty()) {
            std::cerr << "Invalid input!" << std::endl;
            return 1;
        }
        if (pattern.back() == ',') pattern.pop_back(); else last = true;
        patterns.push_back(pattern);
    }

    int64_t answer1 = 0;
    int64_t answer2 = 0;
    std::string target;
    while ((std::cin >> target)) {
        int64_t n = Solve(patterns, target);
        answer1 += n > 0;
        answer2 += n;
        //std::cerr << n << '\n';
    }
    if (!std::cin.eof()) {
        std::cerr << "Input error!\n";
        return 1;
    }
    std::cout << answer1 << '\n' << answer2 << std::endl;
}
