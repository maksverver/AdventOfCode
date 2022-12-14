#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

namespace {

struct Point {
  int32_t r, c;

  Point() { r = 0; c = 0; }

  uint64_t Id() const {
    return (uint64_t{(uint32_t) c} << 32) | uint64_t{(uint32_t) r};
  }
};

template <class T> size_t CountDistinct(std::vector<T> &v) {
  if (v.empty()) return 0;
  std::sort(v.begin(), v.end());
  size_t res = 1;
  for (size_t i = 1; i < v.size(); ++i) {
    res += (v[i] != v[i - 1]);
  }
  return res;
}

}  // namespace

int main() {
  // Intentionally leak memory to save on deallocation time.
  auto *visited1 = new std::vector<uint64_t>();
  auto *visited2 = new std::vector<uint64_t>();
  const int len = 10;
  Point rope[len] = {};
  if (len > 1) visited1->push_back(rope[1].Id());
  if (len > 9) visited2->push_back(rope[9].Id());
  char dir;
  int dist;
  while (scanf("%[UDRL] %d\n", &dir, &dist) == 2) {
    int dr = dir == 'U' ? +1 : dir == 'D' ? -1 : 0;
    int dc = dir == 'R' ? +1 : dir == 'L' ? -1 : 0;
    for (int step = 0; step < dist; ++step) {
      // TODO: check for int overflow?
      rope[0].r += dr;
      rope[0].c += dc;
      for (int i = 1; i < len; ++i) {
        int dr = rope[i - 1].r - rope[i].r;
        int dc = rope[i - 1].c - rope[i].c;
        int clamped_dr = std::clamp(dr, -1, 1);
        int clamped_dc = std::clamp(dc, -1, 1);
        if (dr == clamped_dr && dc == clamped_dc) break;
        rope[i].r += clamped_dr;
        rope[i].c += clamped_dc;
        if (i == 1) visited1->push_back(rope[i].Id());
        if (i == 9) visited2->push_back(rope[i].Id());
      }
    }
  }
  assert(feof(stdin));

  size_t answer1 = CountDistinct(*visited1);
  size_t answer2 = CountDistinct(*visited2);

  std::cout << answer1 << std::endl;
  std::cout << answer2 << std::endl;
}
