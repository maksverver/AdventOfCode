#include "solve-cliquer-common.h"

#include <assert.h>
#include <ctype.h>
#include <stdio.h>
#include <time.h>

graph_t *read_input(FILE *fp) {
    struct timespec ts = timer_start();

    graph_t *g = graph_new(26*26);
    assert(g != NULL);
    char line[80];
    for (int lineno = 1; fgets(line, sizeof(line), fp); ++lineno) {
        size_t n = strlen(line);
        while (n > 0 && isspace(line[n - 1])) --n;
        if (n == 5 && 
            'a' <= line[0] && line[0] <= 'z' &&
            'a' <= line[1] && line[1] <= 'z' &&
            line[2] == '-' &&
            'a' <= line[3] && line[3] <= 'z' &&
            'a' <= line[4] && line[4] <= 'z') {
            int v = (line[0] - 'a')*26 + (line[1] - 'a');
            int w = (line[3] - 'a')*26 + (line[4] - 'a');
            if (v == w) {
                fprintf(stderr, "Loop detected at line %d\n", lineno);
                goto failed;
            }
            if (GRAPH_IS_EDGE_FAST(g, v, w)) {
                fprintf(stderr, "Duplicate edge detected at line %d\n", lineno);
                goto failed;
            }
            GRAPH_ADD_EDGE(g, v, w);
        } else {
            fprintf(stderr, "Could not parse line %d\n", lineno);
            goto failed;
        }
    }

    if (!feof(stdin)) {
        fprintf(stderr, "Failed reading input!\n");
        goto failed;
    }

    if (graph_edge_count(g) == 0) {
        fprintf(stderr, "Graph is empty!\n");
        goto failed;
    }

    if (!graph_test(g, NULL)) {
        fprintf(stderr, "Invalid graph!\n");
        goto failed;
    }

    timer_finish(&ts, "Reading input");
    return g;

failed:
    graph_free(g);
    return NULL;
}

static struct timespec now() {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) == -1) {
        perror("clock_gettime");
        exit(1);
    }
    return ts;
}

struct timespec timer_start() {
    return now();
}

void timer_finish(struct timespec *ts, const char *what) {
    struct timespec finish = now();
    struct timespec start = *ts;

    fprintf(stderr, "%s took: %lld us\n", what,
        (long long) 1e6 * (finish.tv_sec - start.tv_sec) + (finish.tv_nsec - start.tv_nsec) / 1000);
}
