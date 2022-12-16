// Advent of Code 2022 Day 14: Regolith Reservoir
// https://adventofcode.com/2022/day/14
//

#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

// For memory map
// #include "sys/mman.h"
// #include "sys/stat.h"
// #include "unistd.h"

namespace {

uint64_t DelayMicros(
    std::chrono::steady_clock::time_point start,
    std::chrono::steady_clock::time_point finish) {
  return std::chrono::duration_cast<std::chrono::microseconds>(finish - start).count();
}

}  // namespace

int main() {
  auto time_start = std::chrono::steady_clock::now();

  std::unordered_map<std::string, int> ids;
  std::vector<int> flow_rates;

  // Read input.
  int start_i = -1;
  int V = 0;
  std::vector<std::vector<std::string>> edges;
  for (std::string line; std::getline(std::cin, line); ) {
    char buf[2];
    int flow_rate = 0;
    int res = sscanf(line.c_str(), "Valve %2c has flow rate=%d;", buf, &flow_rate);
    assert(res == 2);
    std::string src(buf, 2);
    int src_i = V++;
    assert(ids.find(src) == ids.end());
    ids[src] = src_i;
    if (src == "AA") start_i = src_i;
    flow_rates.push_back(flow_rate);
    std::vector<std::string> adj;
    int end = line.size();
    while (end > 0 && isspace(line[end - 1])) --end;
    do {
      std::string dst = line.substr(end - 2, 2);
      adj.push_back(dst);
      end -= 4;
    } while (end > 0 && line[end] == ',');
    edges.push_back(adj);
  }
  assert(std::cin.eof());
  assert(start_i >= 0);

  // Distance matrix between all pairs (Floyd-Warshall)
  std::vector<int> dists(V*V, 999999999);
  for (int i = 0; i < V; ++i) {
    dists[i*V + i] = 0;
    for (const std::string &dst : edges[i]) {
      auto it = ids.find(dst);
      assert(it != ids.end());
      int j = it->second;
      assert(dists[i*V + j] == 999999999);
      dists[i*V + j] = 1;
    }
  }
  for (int k = 0; k < V; ++k) {
    for (int i = 0; i < V; ++i) {
      for (int j = 0; j < V; ++j) {
        dists[i*V + j] = std::min(dists[i*V + j], dists[i*V + k] + dists[k*V + j]);
      }
    }
  }

  // Maximum number of steps to take.
  constexpr int T = 30;

  // Reduce graph to only valves with positive flow
  // Keep track of distances from the original starting valve (which may or may not
  // have a positive flow itself).
  std::vector<int> start_dists;
  {
    std::vector<int> valves_with_flow;
    for (int i = 0; i < V; ++i) {
      if (flow_rates[i] > 0 && dists[start_i * V + i] < T - 1) {
        valves_with_flow.push_back(i);
        start_dists.push_back(dists[start_i * V + i]);
      }
    }
    int new_V = valves_with_flow.size();
    std::vector<int> new_dists(new_V * new_V);
    std::vector<int> new_flow_rates(new_V);
    for (int i = 0; i < new_V; ++i) {
      int v = valves_with_flow[i];
      new_flow_rates[i] = flow_rates[v];
      for (int j = 0; j < new_V; ++j) {
        int w = valves_with_flow[j];
        new_dists[new_V * i + j] = dists[v * V + w];
      }
    }
    V = new_V;
    dists = std::move(new_dists);
    flow_rates = std::move(new_flow_rates);
  }
  std::cerr << "Remaining valves: " << V << '\n';
  std::cerr << "Distance matrix:\n";
  for (int i = 0; i < V; ++i) {
    for (int j = 0; j < V; ++j) {
      std::cerr << std::setw(3) << dists[i*V + j];
    }
    std::cerr << '\n';
  }

  // To support V > 30 I need to change all bit shifts to 64-bit numbers
  assert(V <= 30);

  // Calculate memo[time_left][last_valve][opened]
  constexpr bool compact = true;
  size_t memo_size = (size_t)(T + 1)*V*(1u << (V - compact));
  std::cerr << "Memo size: " << memo_size << " (entries)\n";
  std::vector<int> memo_data(memo_size);
  auto memo = [&memo_data, memo_size, V] (int t, int v, unsigned o) -> int& {
    if (compact) {
      o = (o & ((1u << v) - 1)) | ((o & ~((1u << (v + 1)) - 1)) >> 1);
    }
    size_t index = (((size_t)t*V + v) << (V - compact)) + o;
    return memo_data[index];
  };
  std::cerr << "Memo cost: " << (long long)T * V * (1 << V) * V << " (iterations)\n";
  for (int t = 1; t <= T; ++t) {
    for (int v = 0; v < V; ++v) {
      for (unsigned o = 0; o < (1u << V); ++o) {
        if (o & (1 << v)) {
          int max_value = memo(t - 1, v, o);
          for (int w = 0; w < V; ++w) {
            if ((o & (1 << w)) == 0) {
              int d = dists[v*V + w];
              if (d < t) {
                int value = memo(t - d - 1, w, o | (1u << w)) + (t - d - 1)*flow_rates[w];
                max_value = std::max(max_value, value);
              }
            }
          }
          memo(t, v, o) = max_value;
        }
      }
    }
  }

  // Calculate the maximum total pressure that can be released after time t,
  // but without opening valves from bitmask `o`. This logic is very similar to
  // that used to calculate the memo, above.
  auto max_release = [&](int t, unsigned o) {
    int max_value = 0;
    for (int v = 0; v < V; ++v) {
      if ((o & (1u << v)) == 0) {
        int d = start_dists[v];
        if (d < t) {
          int value = memo(t - d - 1, v, o | (1u << v)) + (t - d - 1)*flow_rates[v];
          max_value = std::max(max_value, value);
        }
      }
    }
    return max_value;
  };

  int answer1 = max_release(30, 0);

  int answer2 = 0;
  for (unsigned o = 0; o < (1u << (V - 1)); ++o) {
    int p = (1u << V) - 1 - o;  // complement of o
    answer2 = std::max(answer2, max_release(26, o) + max_release(26, p));
  }

  auto time_finish = std::chrono::steady_clock::now();

  std::cout << answer1 << std::endl;
  std::cout << answer2 << std::endl;

  std::cerr << "Time: " << DelayMicros(time_start, time_finish) << " us\n";
}
