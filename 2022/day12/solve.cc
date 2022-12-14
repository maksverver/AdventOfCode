#include <cassert>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <vector>
#include <string>
#include <queue>

namespace {

typedef unsigned short coord_t;

struct Point {
  coord_t r, c;

  friend auto operator<=>(const Point&, const Point&) = default;
};

std::ostream &operator<<(std::ostream &os, const Point &p) {
  return os << p.r << ',' << p.c;
}

bool CanReach(char src, char dst) {
  return dst - src <= 1;
}

int Bfs(const std::vector<std::string> &maze, std::vector<Point> todo, Point finish) {
  int H = maze.size();
  int W = maze[0].size();
  std::vector<std::vector<int>> dist(H, std::vector<int>(W, -1));
  for (const Point &p : todo) dist[p.r][p.c] = 0;
  for (size_t i = 0; i < todo.size(); ++i) {
    coord_t r = todo[i].r;
    coord_t c = todo[i].c;
    auto test = [&](coord_t r2, coord_t c2) {
      if (CanReach(maze[r][c], maze[r2][c2]) && dist[r2][c2] < 0) {
        Point p = {r2, c2};
        if (p == finish) return true;
        dist[r2][c2] = dist[r][c] + 1;
        todo.push_back(p);
      }
      return false;
    };
    if ((r > 0 && test(r - 1, c)) ||
        (r + 1 < H && test(r + 1, c)) ||
        (c > 0 && test(r, c - 1)) ||
        (c + 1 < W && test(r, c + 1))) {
      std::cerr << i + 1 << " points expanded\n";
      return dist[r][c] + 1;
    }
  }
  return -1;
}

int Astar(const std::vector<std::string> &maze, std::vector<Point> starts, Point finish) {
  int H = maze.size();
  int W = maze[0].size();
  std::vector<std::vector<int>> dist(H, std::vector<int>(W, 999'999'999));
  std::vector<std::vector<Point>> todos;

  auto est = [&](const Point &p) {
    return abs(finish.r - p.r) + abs(finish.c - p.c);
  };

  int h = 0;

  auto add = [&](const Point &p, int d) {
    if (d >= dist[p.r][p.c]) return false;
    dist[p.r][p.c] = d;
    int index = d + est(p);
    assert(index >= h);
    if (todos.size() <= index) todos.resize(index + 1);
    todos[index].push_back(p);
    return true;
  };

  for (const Point &p : starts) add(p, 0);

  long long expanded = 0;
  while (h < todos.size()) {
    if (todos[h].empty()) {
      ++h;
      continue;
    }
    Point p = todos[h].back();
    int d = dist[p.r][p.c];
    todos[h].pop_back();
    if (d > dist[p.r][p.c]) continue;  // already expanded
    ++expanded;

    auto test = [&](Point q) {
      if (!CanReach(maze[p.r][p.c], maze[q.r][q.c])) return false;
      if (q == finish) return true;
      add(q, d + 1);
      return false;
    };
    if ((p.r > 0     && test({(coord_t)(p.r - 1), p.c})) ||
        (p.r + 1 < H && test({(coord_t)(p.r + 1), p.c})) ||
        (p.c > 0     && test({p.r, (coord_t)(p.c - 1)})) ||
        (p.c + 1 < W && test({p.r, (coord_t)(p.c + 1)}))) {
      return dist[p.r][p.c] + 1;
    }
  }
  return -1;
}

uint64_t DelayMicros(
    std::chrono::steady_clock::time_point start,
    std::chrono::steady_clock::time_point finish) {
  return std::chrono::duration_cast<std::chrono::microseconds>(finish - start).count();
}

std::string bfs_arg = "bfs";
std::string astar_arg = "astar";

}  // namespace

int main(int argc, char *argv[]) {
  if (argc != 2 || !(bfs_arg == argv[1] || astar_arg == argv[1])) {
    std::cerr << "Usage: " << argv[0] << " [bfs/astar]\n";
    return 1;
  }
  bool bfs = bfs_arg == argv[1];

  auto time_start = std::chrono::steady_clock::now();
  std::vector<std::string> maze;
  std::string line;
  while (std::getline(std::cin, line)) maze.push_back(line);
  assert(std::cin.eof());

  std::vector<Point> start;
  std::vector<Point> starts;
  Point finish;
  for (coord_t r = 0; r < maze.size(); ++r) {
    for (coord_t c = 0; c < maze[r].size(); ++c) {
      if (maze[r][c] == 'S') {
        maze[r][c] = 'a';
        start.push_back({r, c});
      }
      if (maze[r][c] == 'a') {
        starts.push_back({r, c});
      }
      if (maze[r][c] == 'E') {
        maze[r][c] = 'z';
        finish = {r, c};
      }
    }
  }
  assert(start.size() == 1);

  auto time_part1_start = std::chrono::steady_clock::now();
  int answer1 = bfs ? Bfs(maze, std::move(start), finish)  : Astar(maze, std::move(start), finish);
  auto time_part2_start = std::chrono::steady_clock::now();
  int answer2 = bfs ? Bfs(maze, std::move(starts), finish) : Astar(maze, std::move(starts), finish);

  auto time_finish = std::chrono::steady_clock::now();

  std::cout << answer1 << std::endl;
  std::cout << answer2 << std::endl;

  std::cerr << "Total time:  " << std::setw(10) << DelayMicros(time_start, time_finish) << " us\n";
  std::cerr << "  Parsing:   " << std::setw(10) << DelayMicros(time_start, time_part1_start) << " us\n";
  std::cerr << "  Solving 1: " << std::setw(10) << DelayMicros(time_part1_start, time_part2_start) << " us\n";
  std::cerr << "  Solving 2: " << std::setw(10) << DelayMicros(time_part2_start, time_finish) << " us\n";
}
