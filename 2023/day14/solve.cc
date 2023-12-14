#include <algorithm>
#include <chrono>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

std::string data;
size_t H, W;

void TumbleLine(size_t start, size_t count, size_t stride) {
  size_t i = start;
  for (size_t j = start; count--; j += stride) {
    if (data[j] == '#') {
      i = j + stride;
    } else if (data[j] == 'O') {
      if (i != j) {
        data[j] = '.';
        data[i] = 'O';
      }
      i += stride;
    }
  }
}

void North() { for (size_t c = 0; c != W; ++c) TumbleLine(c, H, W); }
void West()  { for (size_t r = 0; r != H; ++r) TumbleLine(W*r, W, 1); }
void South() { for (size_t c = 0; c != W; ++c) TumbleLine((H - 1)*W + c, H, -W); }
void East()  { for (size_t r = 0; r != H; ++r) TumbleLine(W*r + W - 1, W, -1); }

int64_t GetLoad() {
  int64_t answer = 0;
  for (size_t i = 0; i != data.size(); ++i) if (data[i] == 'O') answer += H - i / W;
  return answer;
}

inline uint64_t Fnv1a_64(const uint8_t data[], size_t len) {
  uint64_t h = 14695981039346656037u;
  for (size_t i = 0; i < len; ++i) {
    h ^= data[i];
    h *= 1099511628211u;
  }
  return h;
}

void DebugPrint() {
  std::cerr << '\n';
  for (size_t i = 0; i != H; ++i) {
    for (size_t j = 0; j != W; ++j) {
      std::cerr << data[W*i + j];
    }
    std::cerr << '\n';
  }
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

  int64_t answer1 = 0;
  int64_t answer2 = 0;

  std::getline(std::cin, data);
  assert(!data.empty());
  H = 1, W = data.size();
  for (std::string line; std::getline(std::cin, line); ) {
    assert(line.size() == W);
    data += line;
    ++H;
  }
  assert(std::cin.eof());

  North();

  std::cout << GetLoad() << std::endl;

  West();
  South();
  East();
  std::unordered_map<uint64_t, int> seen;
  int steps = 1;
  uint64_t hash;
  while (!seen.contains(hash = Fnv1a_64(reinterpret_cast<uint8_t*>(data.data()), data.size()))) {
    seen[hash] = steps;
    North(), West(), South(), East();
    ++steps;
    if (seen.size() % 1000000 == 0) std::cerr << seen.size() << std::endl;
  }
  int cycle_length = steps - seen[hash];
  int remaining_steps = 1000000000 - steps;
  assert(remaining_steps >= 0);
  remaining_steps %= cycle_length;
  while (remaining_steps--) North(), West(), South(), East();

  std::cout << GetLoad() << std::endl;

  std::cerr << "Took " << timer.ElapsedNanos() / 1.e6 << " ms\n";
}
