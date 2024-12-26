/* Solves part 2 by using Cliquer to find the maximum clique.

Cliquer: https://users.aalto.fi/~pat/cliquer.html

This is very fast in practice!
*/

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "solve-cliquer-common.h"

static boolean callback(set_t s, graph_t *g, clique_options *opts) {
    /* Maximum clique found! */
    if (opts->user_data) {
        timer_finish((struct timespec*) opts->user_data, "Solving part 2");
        opts->user_data = NULL;
    }

    /* Print the answer. */
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

    /* We could return FALSE here to abort the search, but keep running to verify
       that the maximum clique is actually unique.*/
    return TRUE;
}

int main() {
    graph_t *g = read_input(stdin);
    if (g == NULL) return EXIT_FAILURE;

    struct timespec ts = timer_start();
    cliquer_options opts = {
        .reorder_function = reorder_by_default,
        .user_function = callback,
        .user_data = (void*) &ts,
    };
    int found = clique_unweighted_find_all(g, 0, 0, TRUE, &opts);
    graph_free(g);

    if (found < 1) {
        fprintf(stderr, "No cliques found!\n");
        return EXIT_FAILURE;
    }
    if (found > 1) {
        fprintf(stderr, "Multiple maximum cliques found!\n");
        return EXIT_FAILURE;
    }
}
