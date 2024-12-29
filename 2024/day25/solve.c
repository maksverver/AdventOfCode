#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define REP(i, n) for (int i = 0; i < n; ++i)

int main() {
    int keys [6][6][6][6][6] = {};
    int locks[6][6][6][6][6] = {};

    // Parse input. This is surprisingly annoying :-/
    for (;;) {
        char buf[7*6 + 1];
        ssize_t nread = fread(buf, 1, sizeof(buf), stdin);
        if (nread == 0) {
            break;
        }
        if (nread < 7*6) {
            fprintf(stderr, "Unexpected end of file!\n");
            exit(1);
        }
        int h[5] = {};
        REP(c, 5) REP(r, 5) h[c] += buf[6*(r + 1) + c] == '#';
        if (buf[0] == '#') {
            locks[h[0]][h[1]][h[2]][h[3]][h[4]]++;
        } else {
            keys[h[0]][h[1]][h[2]][h[3]][h[4]]++;
        }
        if (nread == 7*6) break;
    }
    assert(feof(stdin));

    long long answer = 0;
    REP(a, 6) REP(b, 6) REP(c, 6) REP(d, 6) REP(e, 6) {
        int n = locks[a][b][c][d][e];
        if (n == 0) continue;
        REP(f, 6-a) REP(g, 6-b) REP(h, 6-c) REP(i, 6-d) REP(j, 6-e) {
            int m = keys[f][g][h][i][j];
            answer += (long long) n * m;
        }
    }
    printf("%lld\n", answer);
}
