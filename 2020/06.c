#include <stdio.h>

int main() {
    int answer1 = 0;
    int answer2 = 0;

    unsigned un = 0;
    unsigned in = -1;

    char line[32];
    while (fgets(line, sizeof(line), stdin)) {
        if (line[0] == '\n') {
            answer1 += __builtin_popcount(un);
            answer2 += __builtin_popcount(in);
            un = 0;
            in = -1;
        } else {
            unsigned mask = 0;
            for (char *p = line; *p && *p >= 'a' && *p <= 'z'; ++p) mask |= 1 << (*p - 'a');
            un |= mask;
            in &= mask;
        }
    }
    answer1 += __builtin_popcount(un);
    answer2 += __builtin_popcount(in);

    printf("%d\n%d\n", answer1, answer2);
}
