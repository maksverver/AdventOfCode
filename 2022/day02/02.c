#include <assert.h>
#include <stdio.h>
#include <stdint.h>

#define P(x, i) ((uint64_t) x << (4*i))
#define PACK(a, b, c, d, e, f, g, h, i) ( \
  P(a, 0) | P(b, 1) | P(c, 2) | \
  P(d, 4) | P(e, 5) | P(f, 6) | \
  P(g, 8) | P(h, 9) | P(i, 10))

static const uint64_t a = PACK(
  4, 1, 7,
  8, 5, 2,
  3, 9, 6);
static const uint64_t b = PACK(
  3, 1, 2,
  4, 5, 6,
  8, 9, 7);

static char buf[4 << 20];

int main() {
  int points1 = 0;
  int points2 = 0;
  int64_t c[3][3] = {};
  size_t n = 0;
  while ((n = fread(buf, 1, sizeof(buf), stdin)) != 0) {
    assert(n % 4 == 0);
    for (char *p = buf, *end = buf + n; p != end; p += 4) {
      ++c[p[0] - 'A'][p[2] - 'X'];
    }
  }
  assert(feof(stdin));
  for (int i = 0; i < 3; ++i) {
    for (int j = 0; j < 3; ++j) {
      points1 += c[i][j] * ((a >> (4*(4*j + i))) & 0xf);
      points2 += c[i][j] * ((b >> (4*(4*j + i))) & 0xf);
    }
  }
  printf("%d\n", points1);
  printf("%d\n", points2);
  return 0;
}
