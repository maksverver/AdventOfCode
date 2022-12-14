#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>

static void insert(int top[], int k, int value) {
  if (value <= top[k - 1]) return;
  int i = k - 1;
  while (i > 0 && value > top[i - 1]) top[i] = top[i - 1], --i;
  top[i] = value;
}

int main() {
  int top[3] = {0, 0, 0};

  // Map input file into memory.
  int fd = 0;  // stdin
  struct stat st;
  int res = fstat(fd, &st);
  assert(res == 0);
  size_t len = st.st_size;
  char *buf = mmap(NULL, len, PROT_READ, MAP_SHARED, fd, 0);
  assert(buf != MAP_FAILED);
  res = madvise(buf, len, MADV_SEQUENTIAL | MADV_WILLNEED);
  assert(res == 0);

  bool start = true;  // at start of line?
  int num = 0;        // current number
  int sum = 0;        // current sum
  for (; len > 0; --len, ++buf) {
    if (*buf == '\n') {
      if (start) {
        // New group
        insert(top, 3, sum);
        sum = 0;
      } else {
        // End of number.
        sum += num;
        num = 0;
        start = true;
      }
    } else {
      // Next digit.
      //assert(*buf >= '0' && *buf <= '9');
      num = 10*num + (*buf - '0');
      start = false;
    }
  }
  if (sum > top[2]) insert(top, 3, sum);

  printf("%d\n", top[0]);  // part 1: top sum
  printf("%d\n", top[0] + top[1] + top[2]);
  return 0;
}
