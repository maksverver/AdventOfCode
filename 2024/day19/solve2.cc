// Variant of solve.cc that uses Knuth-Morris-Pratt (KMP) string searching
// to find occurrences of patterns in targets more efficiently.
//
// This has time complexity O(m + Mn) where m is the number of characters in
// patterns, M is the count of patterns, and n is the number of characters in
// the rest of the file. This should be faster when the patterns are few in
// number, but they are long on average.

#include <cstdint>
#include <iostream>
#include <memory>
#include <span>
#include <string>
#include <string_view>
#include <vector>

namespace {

std::unique_ptr<ssize_t[]> BuildPartialMatchTable(std::string_view s) {
    auto table = std::make_unique<ssize_t[]>(s.size() + 1);
    table[0] = -1;
    ssize_t i = 0;
    for (size_t j = 1; j < s.size(); ++j) {
        if (s[i] == s[j]) {
            table[j] = table[i];
        } else {
            table[j] = i;
            do i = table[i]; while (i >= 0 && s[i] != s[j]);
        }
        ++i;
    }
    table[s.size()] = i;
    return table;
}

class Matcher {
  public:
    Matcher(std::string_view pattern) : pattern(pattern),
        table(BuildPartialMatchTable(pattern)) {};

    class State {
      public:
        State() = default;
        State(const Matcher &m) : pattern(m.pattern), table(m.table.get()), i(0) {}

        void Reset() { i = 0; }

        bool Accept(char ch) {
            if (pattern[i] == ch) {
                if ((size_t) i + 1 == pattern.size()) {
                    i = table[pattern.size()];
                    return true;
                }
            } else {
                do i = table[i]; while (i >= 0 && pattern[i] != ch);
            }
            ++i;
            return false;
        }

        std::string_view Pattern() const { return pattern; }

      private:
        std::string_view pattern;
        const ssize_t *table = nullptr;
        ssize_t i = 0;
    };

    State Start() const { return State(*this); }

  private:
    std::string_view pattern;
    std::unique_ptr<ssize_t[]> table;
};

int64_t Solve(std::span<Matcher::State> states, std::string_view target) {
    for (auto &s : states) s.Reset();

    std::vector<int64_t> count(target.size() + 1);
    count[0] = 1;
    for (size_t i = 1; i <= target.size(); ++i) {
        char ch = target[i - 1];
        for (auto &s : states) {
            if (s.Accept(ch)) {
                count[i] += count[i - s.Pattern().size()];
            }
        }
    }
    return count[target.size()];
}

}  // namespace

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    // Read patterns.
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

    // Build pattern matchers.
    std::vector<Matcher> matchers;
    matchers.reserve(patterns.size());
    for (const auto &pattern : patterns) matchers.emplace_back(pattern);

    std::vector<Matcher::State> states;
    states.reserve(patterns.size());
    for (const auto &matcher : matchers) states.emplace_back(matcher);

    int64_t answer1 = 0;
    int64_t answer2 = 0;
    std::string target;
    while ((std::cin >> target)) {
        int64_t n = Solve(states, target);
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
