#include <array>
#include <algorithm>
#include <chrono>
#include <cassert>
#include <cstdint>
#include <deque>
#include <functional>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

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

using state_t = std::vector<std::pair<int, int>>;

state_t GetState(const std::vector<int> &todo) {
  state_t result;
  result.reserve(todo.size());
  for (int pos : todo) result.push_back({pos, counts[3][pos]});
  return result;
}

struct StateHash {
  size_t operator()(const state_t *v) const {
    size_t hash = 0;
    for (auto [pos, count] : *v) {
      hash ^= random_keys[pos]*count;
    }
    return hash;
  }
};

struct StateEqual {
  bool operator()(const state_t *a, const state_t *b) const {
    if (a->size() != b->size()) return false;
    std::ranges::sort(const_cast<state_t&>(*a));
    std::ranges::sort(const_cast<state_t&>(*b));
    return *a == *b;
  }
};

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
  std::vector<int> todo;
  for (int i = 0; i < H * W; ++i) {
    if (data[i] == 'O') {
      int pos = next[0][i];
      assert(pos != -1);
      if (counts[0][pos]++ == 0) todo.push_back(pos);
    }
  }

  int64_t answer = 0;
  if (!part2) {
    for (int pos : GetOccupied(0, todo)) answer += H - pos/W;
  } else {
    // Complete first step.
    std::vector<int> temp;
    Tumble(0, 1, todo, temp);
    Tumble(1, 2, todo, temp);
    Tumble(2, 3, todo, temp);

    // Execute until cycle is detected.
    std::deque<state_t> states;
    std::unordered_map<const state_t*, int, StateHash, StateEqual> seen;
    int *previous = nullptr;
    for (;;) {
      states.push_back(GetState(todo));
      previous = &seen[&states.back()];
      if (*previous != 0) break;
      *previous = states.size();
      Tumble4(todo, temp);
    }
    int steps = states.size();
    int cycle_length = steps - *previous;
    int remaining_steps = 1000000000 - steps;
    assert(remaining_steps >= 0);
    remaining_steps %= cycle_length;
    const state_t &final_state = states.at(*previous + remaining_steps - 1);
    for (auto [start, count] : final_state) {
      for (int i = 0; i < count; ++i) {
        int pos = start + i * stripes[3].along.stride;
        answer += H - pos / W;
      }
    }
  }

  // Reset counts for next call to Solve()
  for (int i : todo) counts[0][i] = 0;
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
