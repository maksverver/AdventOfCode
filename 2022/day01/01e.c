#include <assert.h>
#include <pthread.h>
#include <stdbool.h>
#include <string.h>
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

struct Task {
  char *begin, *end;
  int top[3];
};

static void *process(void *arg) {
  struct Task *const task = arg;
  int top[3] = {0, 0, 0};
  bool start = true;  // at start of line?
  int num = 0;        // current number
  int sum = 0;        // current sum
  for (char *p = task->begin, *end = task->end; p != end; ++p) {
    if (*p == '\n') {
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
      num = 10*num + (*p - '0');
      start = false;
    }
  }
  insert(top, 3, sum);
  memcpy(task->top, top, sizeof(task->top));
  return NULL;
}

#define NUM_THREADS 4

int main() {

  // Map input file into memory.
  int fd = 0;  // stdin
  struct stat st;
  int res = fstat(fd, &st);
  assert(res == 0);
  size_t len = st.st_size;
  char *buf = mmap(NULL, len, PROT_READ, MAP_SHARED, fd, 0);
  assert(buf != MAP_FAILED);
  res = madvise(buf, len, MADV_WILLNEED);
  assert(res == 0);

  struct Task task[NUM_THREADS];
  pthread_t thread[NUM_THREADS];

  size_t pos = 0;
  for (int i = 0; i < NUM_THREADS; ++i) {
    size_t end = i + 1 < NUM_THREADS ? pos + len / NUM_THREADS : len;
    assert(pos - end >= 2);
    while (end < len && !(buf[end - 1] == '\n' && buf[end - 2] == '\n')) ++end;
    task[i].begin = buf + pos;
    task[i].end = buf + end;
    pos = end;
    res = pthread_create(&thread[i], NULL, process, &task[0]);
    assert(res == 0);
  }
  for (int i = 0; i < NUM_THREADS; ++i) {
    res = pthread_join(thread[i], NULL);
    assert(res == 0);
  }

  int top[3] = {0, 0, 0};
  for (int i = 0; i < NUM_THREADS; ++i) {
    for (int j = 0; j < 3; ++j) {
      insert(top, 3, task[0].top[j]);
    }
  }

  printf("%d\n", top[0]);  // part 1: top sum
  printf("%d\n", top[0] + top[1] + top[2]);
  return 0;
}
