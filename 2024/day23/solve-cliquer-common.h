#ifndef SOLVE_CLIQUER_COMMON_H_INCLUDED
#define SOLVE_CLIQUER_COMMON_H_INCLUDED

#include <cliquer/cliquer.h>
#include <stdio.h>
#include <time.h>

graph_t *read_input(FILE *);

struct timespec timer_start();

void timer_finish(struct timespec *ts, const char *what);

#endif  /* ndef SOLVE_CLIQUER_COMMON_H_INCLUDED */
