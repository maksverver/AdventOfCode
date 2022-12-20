#include <array>
#include <deque>
#include <cassert>
#include <cstdio>
#include <iostream>
#include <vector>

#ifdef WITH_ABSL_HASH_SET
#include <absl/hash/hash.h>
#include <absl/container/flat_hash_set.h>
#else
#include <set>
#endif

namespace {

struct Point {
  int x, y, z;

  auto operator<=>(const Point&) const = default;

#ifdef WITH_ABSL_HASH_SET
  template <typename H>
  friend H AbslHashValue(H h, const Point& p) {
    return H::combine(std::move(h), p.x, p.y, p.z);
  }
#endif
};

Point operator+(Point p, Point q) {
  return Point{p.x + q. x, p.y + q.y, p.z + q.z};
}

std::ostream &operator<<(std::ostream &os, const Point &p) {
  return os << p.x << ',' << p.y << ',' << p.z;
}

#ifdef WITH_ABSL_HASH_SET
using PointSet = absl::flat_hash_set<Point>;
#else
using PointSet = std::set<Point>;
#endif

std::array<Point, 6> directions = {
  Point{+1, 0, 0},
  Point{-1, 0, 0},
  Point{0, +1, 0},
  Point{0, -1, 0},
  Point{0, 0, +1},
  Point{0, 0, -1},
};

/*
std::array<Point, 6> Neighbors(const Point &p) {
  auto [x, y, z] = p;
  return {
    Point{x + 1, y, z},
    Point{x - 1, y, z},
    Point{x, y + 1, z},
    Point{x, y - 1, z},
    Point{x, y, z + 1},
    Point{x, y, z - 1},
  };
}
*/

long SolvePart1(const PointSet &points) {
  long result = 0;
  for (Point p : points) {
    for (const Point &d : directions) {
      result += !points.contains(p + d);
    }
  }
  return result;
}

// Find an arbitrary point just outside the point set.
Point FindStartingPoint(const PointSet &points) {
  assert(!points.empty());
  Point p = *std::min_element(points.begin(), points.end());
  --p.x;
  return p;
}

long SolvePart2(const PointSet &points) {
  // Note: this assumes all points are connected!
  PointSet seen;
  std::deque<Point> todo;
  Point starting_point = FindStartingPoint(points);
  todo.push_back(starting_point);
  seen.insert(starting_point);
  long exterior_area = 0;
  while (!todo.empty()) {
    Point p = todo.front();
    todo.pop_front();
    bool adj = false;
    for (const Point &d : directions) {
      Point q = p + d;
      if (points.contains(q)) {
        ++exterior_area;
        adj = true;
      }
    }
    if (adj) {
      for (const Point &d : directions) {
        Point q = p + d;
        if (!points.contains(q)) {
          if (!seen.contains(q)) {
            seen.insert(q);
            todo.push_back(q);
          }
          for (const Point &e : directions) {
            Point r = q + e;
            if (!points.contains(r) && !seen.contains(r)) {
              seen.insert(r);
              todo.push_back(r);
            }
          }
        }
      }
    }
  }
  return exterior_area;
}

}  // namespace

int main(int argc, char *argv[]) {
  PointSet points;
  for (int x, y, z; scanf("%d,%d,%d", &x, &y, &z) == 3; ) {
    points.insert(Point{x, y, z});
  }
  printf("%ld\n", SolvePart1(points));
  printf("%ld\n", SolvePart2(points));
}
