#include <assert.h>
#include <stdbool.h>
#include <stdio.h>

static void update(int top[], int k, int value) {
  if (value <= top[k - 1]) return;

  int i = k - 1;
  while (i > 0 && value > top[i - 1]) {
    top[i] = top[i - 1];
    --i;
  }
  top[i] = value;
}

static char buf[16 << 20];

int main() {
  int top[3] = {0, 0, 0};

  int num = 0;        // current number
  int sum = 0;        // current sum
  size_t len;
  while ((len = fread(buf, 1, sizeof(buf), stdin)) != 0) {
    for (char *p = buf, *end = buf + len; p != end; ++p) {
      if (*p == '\n') {
        if (num == 0) {
          // New group
          update(top, 3, sum);
          sum = 0;
        } else {
          // End of number.
          sum += num;
          num = 0;
        }
      } else {
        // Next digit.
        //assert(*p >= '0' && *p <= '9');
        num = 10*num + (*p - '0');
      }
    }
  }
  assert(feof(stdin));
  update(top, 3, sum);

  printf("%d\n", top[0]);  // part 1: top sum
  printf("%d\n", top[0] + top[1] + top[2]);  // part 2: sum of top 3 sums
  return 0;
}
