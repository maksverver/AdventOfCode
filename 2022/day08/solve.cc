#include <algorithm>
#include <atomic>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

// For memory map
#include "sys/mman.h"
#include "sys/stat.h"
#include "unistd.h"

namespace {

// Set to 0 to disable multithreading and solve on main thread.
const int num_threads = std::thread::hardware_concurrency();

uint8_t *M;

int H = 0, W = 0, stride = 0;

// Returns the element at row r, column c, in the input.
inline uint8_t val(int r, int c) {
  return M[stride*r + c];
}

__attribute__((always_inline))  // does this actually help?
inline void SolveTree(int r, int c, int64_t &visible_count, int64_t &max_score) {
  int left = c - 1, right = c + 1, top = r - 1, bottom = r + 1;
  uint8_t v = val(r, c);
  bool visible = false;
  while (left >= 0 && val(r, left) < v) --left;
  if (left < 0) visible = true, ++left;
  while (right < W && val(r, right) < v) ++right;
  if (right >= W) visible = true, --right;
  while (top >= 0 && val(top, c) < v) --top;
  if (top < 0) visible = true, ++top;
  while (bottom < H && val(bottom, c) < v) ++bottom;
  if (bottom >= H) visible = true, --bottom;

  if (visible) ++visible_count;

  int64_t score = (int64_t) (c - left) * (right - c) * (r - top) * (bottom - r);
  max_score = std::max(score, max_score);
}

// Atomically updates `acc` to the max of `acc` and `val`.
inline void UpdateMax(std::atomic<int64_t> &acc, int64_t val) {
  int64_t cur = acc;
  while (val > cur) if (acc.compare_exchange_weak(cur, val)) return;
}

void SolveThread(
    std::atomic<int64_t> *visible_count,
    std::atomic<int64_t> *max_score,
    std::atomic<int> *next_row) {
  for (;;) {
    int r = (*next_row)++;
    if (r >= H) break;
    int64_t vc = 0;
    int64_t ms = 0;
    for (int c = 0; c < W; ++c) SolveTree(r, c, vc, ms);
    *visible_count += vc;
    UpdateMax(*max_score, ms);
  }
}

uint64_t DelayMicros(
    std::chrono::steady_clock::time_point start,
    std::chrono::steady_clock::time_point finish) {
  return std::chrono::duration_cast<std::chrono::microseconds>(finish - start).count();
}

static size_t FileSize(int fd) {
  struct stat st;
  int res = fstat(fd, &st);
  assert(res == 0);
  return st.st_size;
}

}  // namespace

int main() {
  auto start = std::chrono::steady_clock::now();

  {
    size_t len = FileSize(STDIN_FILENO);
    void *data = mmap(NULL, len, PROT_READ, MAP_SHARED, STDIN_FILENO, 0);
    assert(data != MAP_FAILED);

    M = (uint8_t*) data;
    W = std::find(M, M + len, '\n') - M;
    stride = W + 1;
    H = len / stride;
    assert(H > 0 && W > 0 && len % stride == 0);
  }

  int64_t visible_count = 0;
  int64_t max_score = 0;
  if (num_threads == 0) {
    for (int r = 0; r < H; ++r) {
      for (int c = 0; c < W; ++c) {
        SolveTree(r, c, visible_count, max_score);
      }
    }
  } else {
    std::atomic<int64_t> vc;
    std::atomic<int64_t> ms;
    std::atomic<int> next_row;
    {
      std::vector<std::thread> threads;
      for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(SolveThread, &vc, &ms, &next_row);
      }
      for (auto &t : threads) t.join();
      assert(next_row == H + num_threads);
    }
    visible_count = vc;
    max_score = ms;
  }

  auto finish = std::chrono::steady_clock::now();

  std::cout << visible_count << std::endl;
  std::cout << max_score << std::endl;

  std::cerr << "Total time: " << DelayMicros(start, finish) << " us\n";
}
