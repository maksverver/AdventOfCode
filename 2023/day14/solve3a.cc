#include <array>
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
#define CHEATING 0

std::mt19937_64 rng;    // 64-bit RNG. Doesn't really need to be seeded.

// The input grid, as a contiguous string without whitespace.
std::string data;

// Height and width of the grid.
int H, W;

// counts[dir][pos] is the number of boulders that rest against the wall
// adjacent to `pos` in direction `dir`. Only one direction is active at a time;
// the other directions are zero vectors.
std::vector<int> counts[4];

// walls[dir][pos] is the position where a boulder ends up in the given direction
std::vector<int> next[4];

// Random keys used to generate hash codes for vectors. To be 100% correct these
// should be large, distinct prime numbers instead, but random 64-bit integers
// work just as well in practice (the chance of generating 0 or a duplicate is
// negligble).
std::vector<size_t> random_keys;

struct Axis {
  int stride, length;
};

struct Stripes {
  int start;
  Axis across;
  Axis along;
};

std::array<Stripes, 4> stripes;

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

  // Generate random keys.
  random_keys.resize(H * W);
  for (size_t &key : random_keys) key = rng();

  stripes = {
    Stripes{0,         Axis{1, W}, Axis{ W, H}},  // North (columns)
    Stripes{0,         Axis{W, H}, Axis{ 1, W}},  // West (rows)
    Stripes{(H - 1)*W, Axis{1, W}, Axis{-W, H}},  // South (reverse columns)
    Stripes{(W - 1),   Axis{W, H}, Axis{-1, W}},  // East (reverse rows)
  };

  // Precalculate the nearest wall for each direction.
  for (int dir = 0; dir < 4; ++dir) {
    next[dir].assign(H * W, -1);
    auto [start, across, along] = stripes[dir];
    for (int i = 0; i < across.length; ++i) {
      int wall = -1;
      for (int j = 0; j < along.length; ++j) {
        int pos = start + across.stride * i + along.stride * j;
        if (data[pos] == '#') {
          wall = -1;
        } else {
          if (wall == -1) wall = pos;
          next[dir][pos] = wall;
        }
      }
    }
  }

  // Initialize counts to 0.
  for (auto &v : counts) v.assign(H * W, 0);
}

std::vector<int> GetOccupied(int dir, const std::vector<int> &todo) {
  std::vector<int> occupied;
  for (int start : todo) {
    for (int i = 0; i < counts[dir][start]; ++i) {
      occupied.push_back(start + i*stripes[dir].along.stride);
    }
  }
  return occupied;
}

void DebugPrint(int dir, const std::vector<int> &todo) {
  std::cerr << "\ndir=" << dir << '\n';
  for (int pos : todo) {
    std::cerr << pos << " (" << pos / W << "," << pos % W << ") " << counts[dir][pos] << std::endl;
  }

  std::cerr << '\n';

  std::vector<int> occupied = GetOccupied(dir, todo);
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

#if CHEATING
size_t GetKey(int dir, const std::vector<int> &todo) {
  size_t result = 0;
  for (int pos : todo) result ^= random_keys[pos] * counts[dir][pos];
  return result;
}
#else
std::vector<size_t> GetKey(int dir, const std::vector<int> &todo) {
  std::vector<size_t> result;
  result.reserve(todo.size());
  for (int pos : todo) result.push_back(random_keys[pos] * counts[dir][pos]);
  return result;
}

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

void Tumble(int dir, int next_dir, std::vector<int> &todo, std::vector<int> &temp) {
  assert(temp.empty());
  int stride = stripes[dir].along.stride;
  for (int start : todo) {
    int n = counts[dir][start];
    counts[dir][start] = 0;
    for (int i = 0; i < n; ++i) {
      int pos = start + i*stride;
      int next_pos = next[next_dir][pos];
      assert(next_pos != -1);
      if (counts[next_dir][next_pos]++ == 0) temp.push_back(next_pos);
    }
  }
  todo.resize(0);
  temp.swap(todo);
}

void Tumble4(std::vector<int> &todo, std::vector<int> &temp) {
  Tumble(3, 0, todo, temp);
  Tumble(0, 1, todo, temp);
  Tumble(1, 2, todo, temp);
  Tumble(2, 3, todo, temp);
}

int64_t Solve(bool part2) {
  // Fill initial counts
  int dir = 0;
  std::vector<int> todo;
  for (int i = 0; i < H * W; ++i) {
    if (data[i] == 'O') {
      int pos = next[dir][i];
      assert(pos != -1);
      if (counts[dir][pos]++ == 0) todo.push_back(pos);
    }
  }
  if (part2) {
    // Complete first step.
    std::vector<int> temp;
    Tumble(0, 1, todo, temp);
    Tumble(1, 2, todo, temp);
    Tumble(2, 3, todo, temp);
    dir = 3;

    // Execute until cycle is detected.
    int steps = 1;
#if CHEATING
    std::unordered_map<size_t, int> seen;
#else
    std::unordered_map<std::vector<size_t>, int, VectorHash, VectorEqual> seen;
#endif
    int *previous = nullptr;
    while (*(previous = &seen[GetKey(dir, todo)]) == 0) {
      *previous = steps++;
      Tumble4(todo, temp);
    }
    int cycle_length = steps - *previous;
    int remaining_steps = 1000000000 - steps;
    assert(remaining_steps >= 0);
    remaining_steps %= cycle_length;
std::cerr << "steps=" << steps << " cycle_length=" << cycle_length << " remaining_steps=" << remaining_steps << std::endl;
    for (int i = 0; i < remaining_steps % cycle_length; ++i) Tumble4(todo, temp);
  }

  int64_t answer = 0;
  for (int pos : GetOccupied(dir, todo)) answer += H - pos/W;
  for (int i : todo) counts[dir][i] = 0;  // reset for next call to Solve()
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
