#include <algorithm>
#include <chrono>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

// Assume we can use the xor hash to identify solutions uniquely. This doesn't
// work if there are hash collisions, but that doesn't seem to be the case in
// practice.
#define CHEATING 1

std::mt19937_64 rng;

struct Line {
  int start, count, stride;
};

class Tumbler {
  int start, stride, count, key;
  std::vector<std::reference_wrapper<Tumbler>> adjacent;

  friend std::ostream &operator<<(std::ostream &os, const Tumbler &t);

public:
  Tumbler(int start, int stride)
      : start(start), stride(stride), count(0), key(rng()) {}

  void Connect(Tumbler &t) {
    adjacent.push_back(t);
  }

  void Inc(std::vector<std::reference_wrapper<Tumbler>> &todo) {
    if (count++ == 0) todo.push_back(*this);
  }

  void Process(std::vector<std::reference_wrapper<Tumbler>> &todo) {
    assert(count <= adjacent.size());
    int n = count;
    count = 0;
    for (int i = 0; i < n; ++i) adjacent[i].get().Inc(todo);
  }

  void GetIndices(std::vector<int> &output) const {
    for (int i = 0; i < count; ++i) output.push_back(start + stride * i);
  }

  void ExtractIndices(std::vector<int> &output) {
    GetIndices(output);
    count = 0;
  }

  size_t Key() const {
    return key * count;
  }
};

std::ostream &operator<<(std::ostream &os, const Tumbler &t) {
  return os << "Tumbler{" << t.start << ", " << t.stride << ", " << t.count << "}";
}

using tumblers_t = std::vector<std::reference_wrapper<Tumbler>>;

std::string data;
int H, W;
std::vector<Tumbler*> tumblers[4];

void Initialize() {
  // Read input.
  std::getline(std::cin, data);
  assert(!data.empty());
  H = 1, W = data.size();
  for (std::string line; std::getline(std::cin, line); ) {
    assert(line.size() == W);
    data += line;
    ++H;
  }
  assert(std::cin.eof());

  std::vector<Line> lines[4];
  for (int c = 0; c != W; ++c) lines[0].push_back(Line{c, H, W});
  for (int r = 0; r != H; ++r) lines[1].push_back(Line{W*r, W, 1});
  for (int c = 0; c != W; ++c) lines[2].push_back(Line{(H - 1)*W + c, H, -W});
  for (int r = 0; r != H; ++r) lines[3].push_back(Line{W*r + W - 1, W, -1});

  // Create tumblers
  for (int dir = 0; dir < 4; ++dir) {
    tumblers[dir].assign(H * W, nullptr);
    for (auto [start, count, stride] : lines[dir]) {
      Tumbler *t = nullptr;
      for (int pos = start; count-- > 0; pos += stride) {
        if (data[pos] == '#') {
          t = nullptr;
        } else {
          if (t == nullptr) t = new Tumbler(pos, stride);
          tumblers[dir][pos] = t;
        }
      }
    }
  }

  // Connect tumblers
  for (int dir = 0; dir < 4; ++dir) {
    int next_dir = (dir + 1) % 4;
    for (auto [start, count, stride] : lines[dir]) {
      Tumbler *t = nullptr;
      for (int pos = start; count-- > 0; pos += stride) {
        Tumbler *t = tumblers[dir][pos];
        if (t != nullptr) {
          Tumbler *u = tumblers[next_dir][pos];
          assert(u != nullptr);
          t->Connect(*u);
        }
      }
    }
  }
}

void DebugPrint(const tumblers_t &todo) {
  std::cerr << '\n';

  std::vector<int> occupied;
  for (const auto &t : todo) {
    std::cerr << t.get() << '\n';
    t.get().GetIndices(occupied);
  }

  std::cerr << '\n';

  std::ranges::sort(occupied);
  size_t pos = 0;
  for (int i = 0; i < H; ++i) {
    for (int j = 0; j < W; ++j) {
      int k = W*i + j;
      char ch = data[k];
      if (ch != '#') {
        assert(pos == occupied.size() || occupied[pos] >= k);
        if (pos < occupied.size() && occupied[pos] == k) {
          ch = 'O';
          ++pos;
        } else {
          ch = '.';
        }
      }
      std::cerr << ch;
    }
    std::cerr << '\n';
  }
  assert(pos == occupied.size());
}

void Tumble(tumblers_t &todo, tumblers_t &temp, int count) {
  assert(temp.empty());
  while (count-- > 0) {
    for (auto &t : todo) t.get().Process(temp);
    todo.clear();
    temp.swap(todo);
  }
}

#if CHEATING
size_t GetKey(const tumblers_t &tumblers) {
  size_t result = 0;
  for (const auto &t : tumblers) result ^= t.get().Key();
  return result;
}
#else
std::vector<size_t> GetKey(const tumblers_t &tumblers) {
  std::vector<size_t> result;
  result.reserve(tumblers.size());
  for (const auto &t : tumblers) result.push_back(t.get().Key());
  return result;
}
#endif

#if !CHEATING
struct VectorHash {
  size_t operator()(const std::vector<size_t> &v) const {
    size_t hash = 0;
    for (size_t i : v) hash ^= i;
    return hash;
  }
};

struct VectorEqual {
  int operator()(const std::vector<size_t> &a, const std::vector<size_t> &b) const {
    if (a.size() != b.size()) return false;
    std::ranges::sort(const_cast<std::vector<size_t>&>(a));
    std::ranges::sort(const_cast<std::vector<size_t>&>(b));
    return a == b;
  }
};
#endif

int64_t Solve(bool part2) {
  // Fill initial tumblers
  tumblers_t todo;
  for (int i = 0; i < H * W; ++i) {
    if (data[i] == 'O') {
      Tumbler *t = tumblers[0][i];
      assert(t != nullptr);
      t->Inc(todo);
    }
  }

  if (part2) {
    // Complete first step.
    tumblers_t temp;
    Tumble(todo, temp, 3);

    // Execute until cycle is detected.
    int steps = 1;
#if CHEATING
    std::unordered_map<size_t, int> seen;
#else
    std::unordered_map<std::vector<size_t>, int, VectorHash, VectorEqual> seen;
#endif
    int *previous = nullptr;
    while (*(previous = &seen[GetKey(todo)]) == 0) {
      *previous = steps++;
      Tumble(todo, temp, 4);
    }
    int cycle_length = steps - *previous;
    int remaining_steps = 1000000000 - steps;
    assert(remaining_steps >= 0);
    Tumble(todo, temp, remaining_steps % cycle_length * 4);
  }

  std::vector<int> occupied;
  for (auto &t : todo) t.get().ExtractIndices(occupied);
  int64_t answer = 0;
  for (int i : occupied) answer += H - i/W;
  return answer;
}

struct Timer {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();

  long long ElapsedNanos() const {
    auto elapsed = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(elapsed - start).count();
  }
};

}  // namespace

int main() {
  Timer timer;

  Initialize();
  std::cout << Solve(false) << std::endl;
  std::cout << Solve(true) << std::endl;

  std::cerr << "Took " << timer.ElapsedNanos() / 1.e6 << " ms\n";
}
