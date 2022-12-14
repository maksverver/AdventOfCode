#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <map>
#include <mutex>
#include <string>
#include <thread>
#include <utility>
#include <vector>

namespace {

struct Point {
  int32_t r = 0, c = 0;

  friend auto operator<=>(const Point&, const Point&) = default;

  uint64_t Id() const {
    return uint64_t{(uint32_t) r} | (uint64_t{(uint32_t) c} << 32);
  }
};

// Sorts the vector and removes duplicate elements.
template <class T> void MakeUnique(std::vector<T> &v) {
  std::sort(v.begin(), v.end());
  v.erase(std::unique(v.begin(), v.end()), v.end());
}

// Merges two vectors that are sorted and contain no duplicates each
// (although there may be elements that appear in both vectors separately).
// into a new vector that is also sorted and contains no duplicates.
template <class T>
void MergeUnique(std::vector<T> *result, const std::vector<T> &v, const std::vector<T> &w) {
  assert(result->empty());
  result->reserve(v.size() + w.size());
  size_t i = 0, j = 0;
  while (i < v.size() && j < w.size()) {
    if (v[i] < w[j]) result->push_back(std::move(v[i++])); else
    if (w[j] < v[i]) result->push_back(std::move(w[j++])); else {
      result->push_back(std::move(v[i++]));
      ++j;  // erase duplicate
    }
  }
  while (i < v.size()) result->push_back(std::move(v[i++]));
  while (j < w.size()) result->push_back(std::move(w[j++]));
}

template <class T>
std::vector<T> MergeUnique(const std::vector<T> &v, const std::vector<T> &w) {
  std::vector<T> merged;
  MergeUnique(&merged, v, w);
  return merged;
}

template <class T, size_t chunk_size = 8*1000*1000>
class OnlineDeduplicator {
  std::vector<T> buffer;
  std::vector<std::vector<T>*> stack;
  std::vector<std::jthread> threads;
  std::mutex mutex;

public:
  OnlineDeduplicator() {
    buffer.reserve(chunk_size);
  }

  ~OnlineDeduplicator() {
    for (auto *p : stack) delete p;
  }

  // This should only be called from the main thread!
  void Add(T t) {
    buffer.push_back(t);
    if (buffer.size() == chunk_size) {
      auto *chunk = new std::vector<T>();
      chunk->reserve(chunk_size);
      chunk->swap(buffer);

      const std::lock_guard<std::mutex> lock(mutex);
      threads.emplace_back([this, chunk] {
        MakeUnique(*chunk);
        AddSortedPart(0, chunk);
      });
    }
  }

  void JoinAllThreads() {
    // Need to do this in a loop because threads may spawn more threads.
    for (;;) {
      std::vector<std::jthread> tmp;
      {
        // Can't keep the mutex locked because it would not give threads a
        // chance to finish.
        const std::lock_guard<std::mutex> lock(mutex);
        tmp.swap(threads);
      }
      if (tmp.empty()) break;
      std::cerr << tmp.size() << " threads left\n";
    }
  }

  std::vector<T> Finalize() {
    JoinAllThreads();

    std::vector<T> result;
    MakeUnique(buffer);
    result.swap(buffer);
    for (auto *p : stack) {
      if (p != nullptr) {
        result = std::move(MergeUnique(result, *p));
      }
    }
    for (auto *p : stack) delete p;
    stack.clear();
    return result;
  }

private:
  void AddSortedPart(int level, std::vector<T> *v) {
    const std::lock_guard<std::mutex> lock(mutex);

    std::cout << "AddSortedPart " << level << ' ' << v->size() << std::endl;
    if (level == stack.size()) {
      stack.push_back(v);
      return;
    }
    assert(level < stack.size());
    std::vector<T> *&elem = stack[level];
    if (elem == nullptr) {
      elem = v;
      return;
    }
    std::vector<T> *w = elem;
    elem = nullptr;

    threads.emplace_back([this, v, w, level] {
      std::vector<T> *merged = new std::vector<T>;
      MergeUnique(merged, *v, *w);
      delete v;
      delete w;
      AddSortedPart(level + 1, merged);
    });
  }
};

}  // namespace

int main() {
  OnlineDeduplicator<uint64_t> visited1;
  OnlineDeduplicator<uint64_t> visited2;
  const int len = 10;
  Point rope[len] = {};
  if (len > 1) visited1.Add(rope[1].Id());
  if (len > 9) visited2.Add(rope[9].Id());

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
        if (i == 1) visited1.Add(rope[i].Id());
        if (i == 9) visited2.Add(rope[i].Id());
      }
    }
  }
  assert(feof(stdin));

  size_t answer1 = 0;
  size_t answer2 = 0;
  std::cerr << "Finalization starting..."  << std::endl;
  {
    std::jthread finalize1([&]{ answer1 = visited1.Finalize().size(); });
    std::jthread finalize2([&]{ answer2 = visited2.Finalize().size(); });
  }
  std::cerr << "Finalization complete!" << std::endl;
  std::cout << answer1 << std::endl;
  std::cout << answer2 << std::endl;
}
