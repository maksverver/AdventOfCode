#include <assert.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include <cliquer/cliquer.h>

static graph_t *read_input() {
    graph_t *g = graph_new(26*26);
    assert(g != NULL);
    char line[80];
    while (fgets(line, sizeof(line), stdin)) {
        size_t n = strlen(line);
        while (n > 0 && isspace(line[n - 1])) --n;
        assert(n == 5);
        assert('a' <= line[0] && line[0] <= 'z');
        assert('a' <= line[1] && line[1] <= 'z');
        assert(line[2] == '-');
        assert('a' <= line[3] && line[3] <= 'z');
        assert('a' <= line[4] && line[4] <= 'z');
        int v = (line[0] - 'a')*26 + (line[1] - 'a');
        int w = (line[3] - 'a')*26 + (line[4] - 'a');
        assert(!GRAPH_IS_EDGE_FAST(g, v, w));
        GRAPH_ADD_EDGE(g, v, w);
    }
    return g;
}

static boolean callback1(set_t s, graph_t *g, clique_options *opts) {
    for (int v = 26 * ('t' - 'a'); v < SET_MAX_SIZE(s) && v < 26*('t' - 'a' + 1); ++v) {
        if (SET_CONTAINS(s, v)) {
            ++*(int*)opts->user_data;
            break;
        }
    }
    return TRUE;
}

static void solve_part1(graph_t *g) {
    int answer = 0;
    cliquer_options opts = {
        .reorder_function = reorder_by_default,
        .user_function = callback1,
        .user_data = &answer,
    };
    printf("%d\n", clique_unweighted_find_all(g, 3, 3, FALSE, &opts));
    printf("%d\n", answer);
}

static boolean callback2(set_t s, graph_t *g, clique_options *opts) {
    int size = 0;
    for (int v = 0; v < SET_MAX_SIZE(s); v++) {
        if (SET_CONTAINS(s, v)) {
            if (size > 0) putchar(',');
            putchar('a' + v / 26);
            putchar('a' + v % 26);
            ++size;
        }
    }
    printf("\n");
    return TRUE;
}

static void solve_part2(graph_t *g) {
    cliquer_options opts = {
        .reorder_function = reorder_by_default,
        .user_function = callback2,
    };
    int found = clique_unweighted_find_all(g, 0, 0, TRUE, &opts);
    assert(found == 1);
}

static struct timespec now() {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) == -1) {
        perror("clock_gettime");
        exit(1);
    }
    return ts;
}

static struct timespec timer_start() {
    return now();
}

static void timer_finish(struct timespec *ts, const char *what) {
    struct timespec finish = now();
    struct timespec start = *ts;

    fprintf(stderr, "%s took: %lld ms\n", what,
        (long long) 1e6 * (finish.tv_sec - start.tv_sec) + (finish.tv_nsec - start.tv_nsec) / 1000);
}


int main() {
    struct timespec ts = timer_start();
    graph_t *g = read_input();
    timer_finish(&ts, "Reading input");

    if (!feof(stdin)) {
        fprintf(stderr, "Invalid input!\n");
        return 1;
    }

    if (graph_edge_count(g) == 0) {
        fprintf(stderr, "Graph is empty!\n");
        return 1;
    }

    if (!graph_test(g, NULL)) {
        fprintf(stderr, "Invalid graph!\n");
        return 1;
    }

    /* Note: for large graphs part 1 is actually much slower than part 2,
       which is ironic considering how fast part 2 is. For an actually fast
       solution using bitsets, see solve-part-1.cc */
    ts = timer_start();
    solve_part1(g);
    timer_finish(&ts, "Solving part 1");

    ts = timer_start();
    solve_part2(g);
    timer_finish(&ts, "Solving part 2");

    graph_free(g);
}
