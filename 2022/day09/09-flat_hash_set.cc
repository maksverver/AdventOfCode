#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <string>
#include <utility>

#include <absl/hash/hash.h>
#include <absl/container/flat_hash_set.h>

namespace {

struct Point {
  int32_t r = 0, c = 0;

  friend auto operator<=>(const Point&, const Point&) = default;

  template <typename H>
  friend H AbslHashValue(H h, const Point& p) {
    return H::combine(std::move(h), p.r, p.c);
  }
};

}  // namespace

int main() {
  // Intentionally leak memory to save on deallocation time.
  auto *visited1 = new absl::flat_hash_set<Point>();
  auto *visited2 = new absl::flat_hash_set<Point>();
  Point rope[10] = {};
  visited1->insert(rope[1]);
  visited2->insert(rope[9]);

  char dir;
  int dist;
  while (scanf("%[UDRL] %d\n", &dir, &dist) == 2) {
    int dr = dir == 'U' ? +1 : dir == 'D' ? -1 : 0;
    int dc = dir == 'R' ? +1 : dir == 'L' ? -1 : 0;
    for (int step = 0; step < dist; ++step) {
      // TODO: check for int overflow?
      rope[0].r += dr;
      rope[0].c += dc;
      for (int i = 1; i < 10; ++i) {
        int dr = rope[i - 1].r - rope[i].r;
        int dc = rope[i - 1].c - rope[i].c;
        int clamped_dr = std::clamp(dr, -1, 1);
        int clamped_dc = std::clamp(dc, -1, 1);
        if (dr == clamped_dr && dc == clamped_dc) break;
        rope[i].r += clamped_dr;
        rope[i].c += clamped_dc;
        if (i == 1) visited1->insert(rope[i]);
        if (i == 9) visited2->insert(rope[i]);
      }
    }
  }
  assert(feof(stdin));
  std::cout << visited1->size() << std::endl;
  std::cout << visited2->size() << std::endl;
}
