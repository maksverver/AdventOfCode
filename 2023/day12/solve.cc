#include <algorithm>
#include <chrono>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

class Solver {
public:
  Solver(std::string s_in, const std::vector<int> &runs)
      : s(s_in + '.'), runs(runs) {
    max_hashes.resize(s.size());
    for (int i = (int)s.size() - 2; i >= 0; --i) {
      max_hashes[i] = s[i] != '.' ? max_hashes[i + 1] + 1 : 0;
    }
    length_needed.resize(runs.size());
    for (int i = (int)runs.size() - 1; i >= 0; --i) {
      length_needed[i] = (i + 1 < runs.size() ? length_needed[i + 1] : 0) + (runs[i] + 1);
    }
  }

  int64_t operator()() {
    memo = std::vector<int64_t>(s.size() * runs.size());
    return Calc(0, 0);
  }

private:
  std::string s;
  const std::vector<int> &runs;
  std::vector<int> length_needed;
  std::vector<int> max_hashes;
  std::vector<int64_t> memo;

  int64_t Calc(int i, int j) {
    if (j == runs.size()) {
      return std::find(s.begin() + i, s.end(), '#') == s.end();
    }
    if ((int) s.size() - i < length_needed[j]) {
      return 0;
    }

    int key = runs.size()*i + j;
    int64_t &m = memo[key];
    if (m != 0) return m - 1;

    int64_t res = 0;
    if (s[i] != '#') {
      res += Calc(i + 1, j);
    }
    int n = runs[j];
    if (max_hashes[i] >= n && s[i + n] != '#') {
      res += Calc(i + n + 1, j + 1);
    }
    m = res + 1;
    return res;
  }
};

struct Timer {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();

  long long ElapsedNanos() const {
    auto elapsed = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(elapsed - start).count();
  }
};

int main() {
  Timer timer;

  int64_t answer1 = 0;
  int64_t answer2 = 0;

  // Parse input.
  std::string pattern;
  while (std::cin >> pattern) {
    std::vector<int> runs;
    char sep = std::cin.get();
    assert(sep == ' ');
    int i = 0;
    std::cin >> i;
    runs.push_back(i);
    while ((sep = std::cin.get()) == ',') {
      std::cin >> i;
      runs.push_back(i);
    }
    assert(sep == '\n');

    // Solve part 1.
    answer1 += Solver(pattern, runs)();

    // Solve part 2.
    std::string pattern2 = pattern;
    for (int i = 0; i < 4; ++i) pattern2 += '?' + pattern;
    std::vector<int> runs2 = runs;
    for (int i = 0; i < 4; ++i) runs2.insert(runs2.end(), runs.begin(), runs.end());
    answer2 += Solver(pattern2, runs2)();
  }
  assert(std::cin.eof());

  std::cout << answer1 << '\n' << answer2 << '\n';
  std::cerr << "Took " << timer.ElapsedNanos() / 1.e6 << " ms\n";
}
