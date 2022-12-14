#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <random>
#include <string>
#include <vector>

namespace {

std::mt19937 InitializeRng() {
  std::array<int, 624> seed_data;
  std::random_device dev;
  std::generate_n(seed_data.data(), seed_data.size(), std::ref(dev));
  std::seed_seq seq(std::begin(seed_data), std::end(seed_data));
  return std::mt19937(seq);
}

std::mt19937 rng = InitializeRng();

int RandInt(int a, int b) {
  std::uniform_int_distribution<int> dist(a, b);
  return dist(rng);
}

std::array<std::pair<int, int>, 4> Neighbors(int r, int c, int dist) {
  return {{{r - dist, c}, {r, c - dist}, {r + dist, c}, {r, c + dist}}};
}

const int H = 3999, W = 2999;
// const int H = 21, W = 41;
// const int H = 7, W = 5;
std::vector<std::string> maze;

bool Dfs(int r, int c) {
  if (r < 0 || r >= H || c < 0 || c >= W) return false;
  if (maze[r][c] == '.') return false;
  maze[r][c] = '.';

  auto neighbors = Neighbors(r, c, 2);
  std::shuffle(std::begin(neighbors), std::end(neighbors), rng);
  for (auto [r2, c2] : neighbors) {
    if (Dfs(r2, c2)) {
      maze[(r + r2)/2][(c + c2)/2] = '.';
    }
  }

  return true;
}

}  // namespace

int main() {

  maze = std::vector<std::string>(H, std::string(W, '#'));

  // Put the end close to the middle
  int end_r = H/2 + RandInt(-H/20, +H/20)*2;
  int end_c = W/2 + RandInt(-W/20, +W/20)*2;
  Dfs(end_r, end_c);

  std::vector<std::vector<int>> dist(H, std::vector<int>(W, -1));
  std::vector<std::vector<std::pair<int, int>>> next(H, std::vector<std::pair<int, int>>(W));
  std::vector<std::pair<int, int>> todo = {};
  int max_dist = 0;
  dist[end_r][end_c] = 0;
  todo.push_back({end_r, end_c});
  for (size_t i = 0; i < todo.size(); ++i) {
    auto [r, c] = todo[i];
    for (auto [r2, c2]: Neighbors(r, c, 2)) {
      if (0 <= r2 && r2 < H && 0 <= c2 && c2 < W && maze[(r + r2)/2][(c + c2)/2] == '.' && dist[r2][c2] == -1) {
        dist[r2][c2] = max_dist = dist[r][c] + 1;
        next[r2][c2] = {r, c};
        todo.push_back({r2, c2});
      }
    }
  }
  std::cerr << max_dist * 2 << std::endl;

  for (auto [r, c]: todo) {
    int d = dist[r][c];
    assert(d <= max_dist);
    char ch = d == 0 ? 'z' : d == 1 ? 'y' : char('x' - (24*(d - 2)/(max_dist - 2 + 1)));
    maze[r][c] = ch;
    if (d > 0) {
      auto [r2, c2] = next[r][c];
      maze[(r + r2)/2][(c + c2)/2] = ch;
    }
  }

  std::vector<std::string> old_maze = maze;
  for (int r = 0; r < H; ++r) {
    for (int c = 0; c < W; ++c) {
      if (maze[r][c] == '#') {
        // Note: it's possible for a wall to have only wall-neighbors
        char ch = 'a';
        for (auto [r2, c2]: Neighbors(r, c, 1)) {
          if (0 <= r2 && r2 < H && 0 <= c2 && c2 < W && 'a' <= old_maze[r2][c2] && old_maze[r2][c2] <= 'z') {
            ch = std::max(ch, std::min('z', char(old_maze[r2][c2] + 2)));
          }
        }
        maze[r][c] = char(RandInt(ch, 'z'));
      }
    }
  }

  std::vector<std::pair<int, int>> starts;
  for (auto [r, c]: todo) if (dist[r][c] == max_dist) starts.push_back({r, c});
  std::shuffle(starts.begin(), starts.end(), rng);
  auto [start_r, start_c] = starts[0];

  maze[start_r][start_c] = 'S';

  maze[end_r][end_c] = 'E';

  for (const auto &line : maze) {
    std::cout << line << std::endl;
  }
}
