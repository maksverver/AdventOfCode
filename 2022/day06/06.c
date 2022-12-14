#include <assert.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

// Returns the first position in data where the last k characters are distinct,
// or 0 if there is no such position.
static size_t solve(const char *data, size_t len, int k) {
  assert(k > 0);
  size_t last[26] = {};

  size_t first_pos = k;
  for (size_t i = 0; i < len; ++i) {
    int ch = data[i] - 'a';
    //assert(ch >= 0 && ch < 26);
    size_t p = last[ch] + k;
    last[ch] = i + 1;
    if (p > first_pos) {
      first_pos = p;
    } else if (first_pos == i + 1) {
      return first_pos;
    }
  }
  return 0;
}

void run_tests() {
  assert(solve("aaaaaaa", 7, 1) == 1);
  assert(solve("aaaaaaa", 7, 2) == 0);
  assert(solve("abcdabcdabcd", 12, 4) == 4);
  assert(solve("abcaabcaabcd", 12, 4) == 12);
  assert(solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 30, 4) == 7);
  assert(solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 30, 14) == 19);
}

static size_t filesize(int fd) {
  struct stat st;
  int res = fstat(fd, &st);
  assert(res == 0);
  return st.st_size;
}

int main() {
  run_tests();

  // Map standard input into memory.
  size_t len = filesize(STDIN_FILENO);
  char *data = mmap(NULL, len, PROT_READ, MAP_SHARED, STDIN_FILENO, 0);
  assert(data != MAP_FAILED);

  // Trim trailing whitespace.
  while (len > 0 && isspace(data[len - 1])) --len;

  printf("%zu\n", solve(data, len, 4));
  printf("%zu\n", solve(data, len, 14));
}
