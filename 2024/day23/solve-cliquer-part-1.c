/* Solves part 1 by enumerating all 3-cliques with Cliquer.

Cliquer: https://users.aalto.fi/~pat/cliquer.html

This is incredibly slow! Don't use this.

I included it to show how the Cliquer API can be used to solve part 1, too,
but this is not a good solution when searching for a large number of small
cliques, since each clique has to be handled individually, so the runtime
is at least proportional to the answer and in practive even worse since we
filter out cliques that do not contain vertices whose name starts with 't'.

See solve-part-1.cc for a much faster approach.
*/

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "solve-cliquer-common.h"

static boolean callback(set_t s, graph_t *g, clique_options *opts) {
    for (int v = 26 * ('t' - 'a'); v < SET_MAX_SIZE(s) && v < 26*('t' - 'a' + 1); ++v) {
        if (SET_CONTAINS_FAST(s, v)) {
            ++*(int*)opts->user_data;
            break;
        }
    }
    return TRUE;
}

int main() {
    graph_t *g = read_input(stdin);
    if (g == NULL) return EXIT_FAILURE;

    struct timespec ts = timer_start();
    int answer = 0;
    cliquer_options opts = {
        .reorder_function = reorder_by_default,
        .user_function = callback,
        .user_data = &answer,
    };
    clique_unweighted_find_all(g, 3, 3, FALSE, &opts);
    timer_finish(&ts, "Solving part 1");
    printf("%d\n", answer);

    graph_free(g);
}
