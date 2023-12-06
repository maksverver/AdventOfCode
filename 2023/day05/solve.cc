#include <assert.h>
#include <stdio.h>

#include <algorithm>
#include <chrono>
#include <ranges>
#include <vector>

struct Range {
  long long begin, end;
};

struct MapEntry {
  long long begin, end, delta;
};

// Assumes map input ranges do not overlap!
long long Solve1(
    const std::vector<std::vector<MapEntry>> &maps,
    std::vector<Range> ranges) {
  // Declared outside the loop to reuse memory.
  std::vector<Range> new_ranges;
  std::vector<Range> kept_ranges;
  for (const auto &map : maps) {
    for (const auto &entry : map) {
      for (auto [a, b] : ranges) {
        if (a >= entry.end || b <= entry.begin) {
          kept_ranges.push_back({a, b});
        } else {
          if (a < entry.begin) {
            kept_ranges.push_back({a, entry.begin});
            a = entry.begin;
          }
          if (b > entry.end) {
            kept_ranges.push_back({entry.end, b});
            b = entry.end;
          }
          new_ranges.push_back({a + entry.delta, b + entry.delta});
        }
      }
      ranges.swap(kept_ranges);
      kept_ranges.clear();
    }
    new_ranges.insert(new_ranges.end(), ranges.begin(), ranges.end());
    ranges.swap(new_ranges);
    new_ranges.clear();
  }
  assert(!ranges.empty());
  return std::ranges::min(
    std::ranges::views::transform(ranges, [](const Range &r) { return r.begin; }));
}

void MergeAndSort(std::vector<Range> &ranges) {
  std::ranges::sort(ranges, {}, &Range::begin);
  size_t j = 0;
  for (size_t i = 1; i < ranges.size(); ++i) {
    if (ranges[i].begin < ranges[j].end) {
      ranges[j].end = std::max(ranges[j].end, ranges[i].end);
    } else {
      ranges[++j] = ranges[i];
    }
  }
  ranges.resize(j + 1);
}

void Translate(const std::vector<MapEntry> &map, std::vector<Range> &ranges, std::vector<Range> &output) {
  size_t i = 0;
  for (auto [range_begin, range_end] : ranges) {
    for ( ; i < map.size(); ++i) {
      auto [entry_begin, entry_end, delta] = map[i];
      if (range_end <= entry_begin) {
        break;
      }
      if (range_begin < entry_begin) {
        output.push_back(Range{range_begin, entry_begin});
        range_begin = entry_begin;
      }
      if (range_begin < entry_end) {
        if (range_end < entry_end) {
          output.push_back(Range{range_begin + delta, range_end + delta});
          range_begin = range_end;
          break;
        }
        output.push_back(Range{range_begin + delta, entry_end + delta});
        range_begin = entry_end;
      }
    }
    if (range_begin < range_end) {
      output.push_back(Range{range_begin, range_end});
    }
  }
}

// Assumes map input ranges do not overlap!
long long Solve2(
    std::vector<std::vector<MapEntry>> maps,
    std::vector<Range> ranges) {
  std::vector<Range> buffer;
  MergeAndSort(ranges);
  for (auto &map : maps) {
    std::ranges::sort(map, {}, &MapEntry::begin);
    Translate(map, ranges, buffer);
    buffer.swap(ranges);
    buffer.clear();
    MergeAndSort(ranges);
  }
  assert(!ranges.empty());
  return ranges.front().begin;
}

struct Timer {
  std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();

  long long ElapsedNanos() const {
    auto elapsed = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(elapsed - start).count();
  }
};

template<class F> auto Benchmark(const char* label, int run_count, F code) -> decltype(code()) {
  assert(run_count > 0);
  Timer timer;
  decltype(code()) res;
  for (int i = 0; i < run_count; ++i) res = code();
  fprintf(stderr, "%s took %lld ns/run (%d runs)\n",
      label, timer.ElapsedNanos()  / run_count, run_count);
  return res;
}

int main() {
  // Read input
  std::vector<long long> seeds;
  std::vector<std::vector<MapEntry>> maps;
  {
    Timer timer;
    scanf("seeds:");
    long long seed = 0;
    while (scanf("%lld", &seed) == 1) {
      seeds.push_back(seed);
    }
    while (!feof(stdin)) {
      scanf("%*s map:");
      std::vector<MapEntry> &map = maps.emplace_back();
      long long dst, src, len;
      while (scanf("%lld %lld %lld", &dst, &src, &len) == 3) {
        map.push_back(MapEntry{src, src + len, dst - src});
      }
      assert(!map.empty());
    }
    fprintf(stderr, "Parsing took %lld ns\n", timer.ElapsedNanos());
  }

  constexpr int repeat = 100'000;

  // Part 1
  {
    std::vector<Range> ranges1;
    ranges1.reserve(seeds.size());
    for (long long seed : seeds) ranges1.push_back({seed, seed + 1});
    long long answer1 = Benchmark("part1 Solve1()", repeat, [&](){ return Solve1(maps, ranges1); });
    long long answer2 = Benchmark("part1 Solve2()", repeat, [&](){ return Solve2(maps, ranges1); });
    assert(answer1 == answer2);
    printf("%lld\n", answer2);
  }

  // Part 2
  {
    std::vector<Range> ranges2;
    assert(seeds.size() % 2 == 0);
    ranges2.reserve(seeds.size() / 2);
    for (size_t i = 0; i < seeds.size(); i += 2) {
      ranges2.push_back({seeds[i], seeds[i] + seeds[i + 1]});
    }
    long long answer1 = Benchmark("part2 Solve1()", repeat, [&](){ return Solve1(maps, ranges2); });
    long long answer2 = Benchmark("part2 Solve2()", repeat, [&](){ return Solve2(maps, ranges2); });
    assert(answer1 == answer2);
    printf("%lld\n", answer2);
  }
}
