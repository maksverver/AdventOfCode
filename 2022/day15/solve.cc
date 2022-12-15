// Advent of Code 2022 Day 14: Regolith Reservoir
// https://adventofcode.com/2022/day/14
//

#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

// For memory map
// #include "sys/mman.h"
// #include "sys/stat.h"
// #include "unistd.h"

namespace {

constexpr int target_y = 2'000'000;
constexpr int multiply = 4'000'000;
constexpr int max_x    = 4'000'000;
constexpr int max_y    = 4'000'000;

struct Sensor {
  int x, y, r;
};

struct Line {
  int x1, y1, x2, y2;
};

bool IsCovered(const std::vector<Sensor> &sensors, int bx, int by) {
  // maybe binary search for viable range?
  for (auto [x, y, r] : sensors) {
    if (abs(x - bx) + abs(y - by) <= r) return true;
  }
  return false;
}

template <class T> void MakeUnique(std::vector<T> &v) {
  std::sort(v.begin(), v.end());
  v.erase(std::unique(v.begin(), v.end()), v.end());
}

int CountSegmentsSpan(std::vector<std::pair<int, int>> &segments) {
  std::sort(segments.begin(), segments.end());
  int last_x = std::numeric_limits<int>::min();
  int covered = 0;
  for (auto [x1, x2] : segments) {
    if (last_x < x2) {
      if (last_x < x1) {
        covered += x2 - x1 + 1;
      } else {
        covered += x2 - last_x;
      }
      last_x = x2;
    }
  }
  return covered;
}

uint64_t DelayMicros(
    std::chrono::steady_clock::time_point start,
    std::chrono::steady_clock::time_point finish) {
  return std::chrono::duration_cast<std::chrono::microseconds>(finish - start).count();
}

void CalculateDiagonals(
    const std::vector<Sensor> sensors,
    std::vector<Line> &diags1,
    std::vector<Line> &diags2) {
  for (auto [x, y, r] : sensors) {
    diags1.push_back(Line{x, y - r - 1, x + r + 1, y});
    diags1.push_back(Line{x - r - 1, y, x, y + r + 1});
    diags2.push_back(Line{x - r - 1, y, x, y - r - 1});
    diags2.push_back(Line{x, y + r + 1, x + r + 1, y});
  }
}

// This takes the most time. I could probably optimize it e.g. by partitioning
// the space into blocks and doing intersection within blocks.
void CalculateCandidates(
    const std::vector<Line> &diags1,
    const std::vector<Line> &diags2,
    std::vector<std::pair<int, int>> &candidates) {
  for (auto [d1x1, d1y1, d1x2, d1y2] : diags1) {
    int x_lo = std::max(d1x1, 0);
    int x_hi = std::min(d1x2, max_x);
    int y_lo = std::max(0, d1y1);
    int y_hi = std::min(d1y2, max_y);
    for (auto [d2x1, d2y1, d2x2, d2y2] : diags2) {
      // calculate intersection point via x-axis intersection
      int x1 = (d1x1 - d1y1);
      int x2 = (d2x1 + d2y1);
      int d = x2 - x1;
      if (d & 1) continue;  // not on integer point
      int y = d >> 1;
      int x = x1 + y;
      assert(x == x2 - y);
      if (x >= std::max(x_lo, d2x1) && x <= std::min(x_hi, d2x2) &&
          y >= std::max(y_lo, d2y2) && y <= std::min(y_hi, d2y1)) {
        candidates.push_back({x, y});
      }
    }
  }
  std::cerr << candidates.size() << " candidates\n";
  MakeUnique(candidates);
  std::cerr << candidates.size() << " unique candidates\n";
}

}  // namespace

int main() {
  auto time_start = std::chrono::steady_clock::now();

  // For part 1
  std::vector<int> beacon_xs;
  std::vector<std::pair<int, int>> segments;

  // For part 2
  std::vector<Sensor> sensors;

  // Read input.
  int x, y, bx, by;
  while (scanf("Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d\n", &x, &y, &bx, &by) == 4) {
    int r = abs(bx - x) + abs(by - y);

    // For part 1
    int dx = r - abs(y - target_y);
    if (dx >= 0) segments.push_back({x - dx, x + dx});
    if (by == target_y) beacon_xs.push_back(bx);

    // For part 2
    sensors.push_back(Sensor{x, y, r});
  }

  // Solve part 1.
  MakeUnique(beacon_xs);
  int answer1 = CountSegmentsSpan(segments) - beacon_xs.size();

  // Solve part 2.
  std::vector<Line> diags1;
  std::vector<Line> diags2;
  CalculateDiagonals(sensors, diags1, diags2);

  // I could speed this up by deduplicating while searching and stopping when I
  // find the first solution, but that would prevent me from using this solution
  // to check the correctness of my own data sets.
  std::vector<std::pair<int, int>> candidates;
  CalculateCandidates(diags1, diags2, candidates);

  std::chrono::steady_clock::time_point time_finish;
  long long answer2 = -1;
  for (auto [x, y] : candidates) {
    if (!IsCovered(sensors, x, y)) {
      // Solution found!
      if (answer2 != -1) {
        std::cerr << "Multiple solutions! "
            << (answer2 / multiply) << ',' << (answer2 % multiply) << " and "
             << x << ',' << y << std::endl;
        exit(1);
      }
      answer2 = (long long) x * multiply + y;
      time_finish = std::chrono::steady_clock::now();

      // Check for invalid data:
      for (int xx = x - 1; xx <= x + 1; ++xx) {
        for (int yy = y - 1; yy <= y + 1; ++yy) {
          if (xx != x || yy != y) {
            if (!IsCovered(sensors, xx, yy)) {
              std::cerr << "Multiple solutions! " << x << ',' << y << " and "
                  << xx << ',' << y << std::endl;
              exit(1);
            }
          }
        }
      }
    }
  }

  if (answer2 == -1) time_finish = std::chrono::steady_clock::now();

  std::cout << answer1 << std::endl;
  std::cout << answer2 << std::endl;

  std::cerr << "Time: " << DelayMicros(time_start, time_finish) << " us\n";
}
