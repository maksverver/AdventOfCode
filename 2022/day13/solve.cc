// Advent of Code 2022 Day 13: Distress Signal
// https://adventofcode.com/2022/day/13
//
// A super cool almost-sublinear solution that uses no additional memory!
//
// The general idea behind this is that the comparison visits the elements of
// the data structure in the same order as they appear in the input, so instead
// of first parsing and then comparing, we can compare the string representations
// directly, and bail out as soon as a difference is found.

#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

// For memory map
#include "sys/mman.h"
#include "sys/stat.h"
#include "unistd.h"

namespace {

bool isdigit(char ch) {
  return '0' <= ch && ch <= '9';
}

// For debugging.
void PrintLine(const char *p) {
  while (*p && *p != '\n') std::cerr << *p++;
  std::cerr << '\n';
}

// Parses leading digits as a base 10 numbers and updates p to point at the first
// non-digit character following it.
int NextNumber(const char *&p) {
  assert(isdigit(*p));
  int res = *p++ - '0';
  while (isdigit(*p)) res = 10*res + *p++ - '0';
  return res;
}

// Compares a nested structure against a single value.
//
// Examples:
//
//  Compare("[5]", 5) == 0
//  Compare("[[5]]", 5) == 0
//  Compare("[5]", 4) == 1
//  Compare("[5]", 7) == -1
//  Compare("[5,[]]", 5) == 1
//
// If the result of the comparison 0, p will have been updated to point past
// the closing bracket of the matched string. Otherwise, the value of p is
// undefined.
int Compare(const char *&p_in, int i) {
  const char *p = p_in;
  while (*p == '[') ++p;
  if (*p == ']') return -1;
  assert(isdigit(*p));
  int depth = p - p_in;
  int res = *p++ - '0';
  while (res <= i && isdigit(*p)) {
    res = 10*res + (*p++ - '0');
  }
  if (res != i) return res - i;
  if (*p == ',') return 1;
  while (depth > 0) {
    assert(*p == ']');
    ++p;
    --depth;
  }
  p_in = p;
  return 0;
}

// Compares to strings representing nested structures.
//
// Technically this can still be optimized somewhat since we know that
// certain characters can't follow others. For example, if we just compared two
// numbers, we know that the next character cannot be a digit for either p or q,
// but we still do a check here on the next loop iteration.
int Compare(const char *p, const char *q) {
  for (;;) {
    if (isdigit(*p) && isdigit(*q)) {
      int v = NextNumber(p);
      int w = NextNumber(q);
      if (v != w) return v - w;
    } else if (*p == *q) {
      ++p;
      ++q;
    } else if (*p == ',' || *q == ']') {
      return 1;
    } else if (*p == ']' || *q == ',') {
      return -1;
    } else if (*p == '[') {
      int c = Compare(p, NextNumber(q));
      if (c != 0) return c;
    } else if (*q == '[') {
      int c = Compare(q, NextNumber(p));
      if (c != 0) return -c;
    } else {
      assert(false);
    }
  }
  assert(*p == '\n' && *q == '\n');
  return 0;
}

// This is kind of an optimized version of Compare(p, i) above.
//
// Returns the first number value embedded in the string, or -1 if the first
// leaf element is an empty list. This can be used to compare against the input
// markers [[2]] and [[6]].
int FirstNumber(const char *p) {
  while (*p == '[') ++p;
  if (*p == ']') return -1;
  assert(isdigit(*p));
  int res = *p++ - '0';
  // Early out: we only need to know if the value is less than 6 or not.
  while (res < 6 && isdigit(*p)) {
    res = 10*res + (*p++ - '0');
  }
  return res;
}

static size_t FileSize(int fd) {
  struct stat st;
  int res = fstat(fd, &st);
  assert(res == 0);
  return st.st_size;
}

uint64_t DelayMicros(
    std::chrono::steady_clock::time_point start,
    std::chrono::steady_clock::time_point finish) {
  return std::chrono::duration_cast<std::chrono::microseconds>(finish - start).count();
}

}  // namespace

int main() {
  auto time_start = std::chrono::steady_clock::now();

  size_t len = FileSize(STDIN_FILENO);
  const char *data = (const char*) mmap(NULL, len, PROT_READ, MAP_SHARED, STDIN_FILENO, 0);
  assert(data != MAP_FAILED);

  int index = 0;
  long long answer1 = 0;
  int lt2 = 0;
  int lt6 = 0;
  for (const char *p = data, *end = p + len; p != end; ) {
    const char *eol1 = (char*) memchr(p, '\n', end - p);
    assert(eol1);
    const char *q = eol1 + 1;
    const char *eol2 = (char*) memchr(q, '\n', end - q);
    assert(eol2);

    // For part 1: add up indices of correctly ordered pairs.
    ++index;
    if (Compare(p, q) < 0) answer1 += index;

    // For part 2: count which strings are less than [[2]] and [[6]] respectively.
    int i1 = FirstNumber(p);
    int i2 = FirstNumber(q);
    lt2 += i1 < 2;
    lt6 += i1 < 6;
    lt2 += i2 < 2;
    lt6 += i2 < 6;

    p = eol2 + 1;
    if (p != end) {
      assert(*p == '\n');
      ++p;
    }
  }
  long long answer2 = (long long) (lt2 + 1) * (lt6 + 2);

  auto time_finish = std::chrono::steady_clock::now();

  std::cout << answer1 << std::endl;
  std::cout << answer2 << std::endl;

  std::cerr << "Time: " << DelayMicros(time_start, time_finish) << " us\n";
}
