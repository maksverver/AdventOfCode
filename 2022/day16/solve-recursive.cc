// Advent of Code 2022 Day 16: Proboscidea Volcanium
// https://adventofcode.com/2022/day/16

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

// Whether to use the compact memo representation (saves half the memory.
// but slightly slower to compute memo indices).
constexpr bool compact = true;

// Maximum number of steps to take.
constexpr int T = 30;

// Maximum number of steps to for the second problem.
constexpr int T2 = 26;

static_assert(T >= T2);

int V;
std::vector<int> start_dists;
std::vector<int> dists;
std::vector<int> flow_rates;
std::vector<int> memo_data;

int &Memo(int t, int v, unsigned o, bool extra) {
  if (compact) {
    o = (o & ((1u << v) - 1)) | ((o & ~((1u << (v + 1)) - 1)) >> 1);
  }
  size_t index = (((size_t)(t - 1 + T2*extra)*V + v) << (V - compact)) + o;
  return memo_data[index];
}

int &Dist(int v, int w) {
  return dists[v * V + w];
}

int MaxRelease(int t, unsigned o, bool extra);

int Calc(int t, int v, unsigned o, bool extra) {
  if (t == 0) return 0;
  int &m = Memo(t, v, o, extra);
  if (m >= 0) return m;
  assert(o & (1 << v));
  int max_value = extra > 0 ? MaxRelease(T2, o, false) : 0;
  for (int w = 0; w < V; ++w) {
    if ((o & (1 << w)) == 0) {
      int d = Dist(v, w);
      if (d < t) {
        int value = Calc(t - d - 1, w, o | (1u << w), extra) + (t - d - 1)*flow_rates[w];
        max_value = std::max(max_value, value);
      }
    }
  }
  return m = max_value;
};

int MaxRelease(int t, unsigned o, bool extra) {
  int max_value = 0;
  for (int v = 0; v < V; ++v) {
    if ((o & (1u << v)) == 0) {
      int d = start_dists[v];
      if (d < t) {
        int value = Calc(t - d - 1, v, o | (1u << v), extra) + (t - d - 1)*flow_rates[v];
        max_value = std::max(max_value, value);
      }
    }
  }
  return max_value;
}

}  // namespace

int main() {
  auto time_start = std::chrono::steady_clock::now();

  std::unordered_map<std::string, int> ids;

  // Read input.
  int start_i = -1;
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
  dists.assign(V*V, 999999999);
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

  // Reduce graph to only valves with positive flow
  // Keep track of distances from the original starting valve (which may or may not
  // have a positive flow itself).
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

  // Note: could reduce memory somewhat by clearing part of the memo between
  // part 1 and part 2, (so that we have T rows for part 1 and 2*T2 rows for
  // part 2).
  size_t memo_size1 = (size_t)(T * V) << (V - compact);
  size_t memo_reuse = (size_t)(T2 * V) << (V - compact);
  size_t memo_size2 = (size_t)(2 * T2 * V) << (V - compact);
  std::cerr << "Memo size part 1: " << memo_size1 << " (entries)\n";
  std::cerr << "Memo size part 2: " << memo_size2 << " (entries)\n";
  memo_data.assign(memo_size1, -1);

  // Calculate the maximum total pressure that can be released after time t,
  // but without opening valves from bitmask `o`. This logic is very similar to
  // that used to calculate the memo, above.

  int answer1 = MaxRelease(T, 0, 0);

  // Shrink to discard data we don't want to reuse, the extend to initialize
  // new entries to -1.
  memo_data.resize(memo_reuse, -1);
  memo_data.resize(memo_size2, -1);

  int answer2 = MaxRelease(T2, 0, true);

  auto time_finish = std::chrono::steady_clock::now();

  std::cout << answer1 << std::endl;
  std::cout << answer2 << std::endl;

  std::cerr << "Time: " << DelayMicros(time_start, time_finish) << " us\n";
}
