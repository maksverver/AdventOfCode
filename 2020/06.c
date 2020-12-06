#include <stdio.h>

int main() {
    int answer1 = 0;
    int answer2 = 0;

    unsigned un = 0;
    unsigned in = 0;

    char line[32];
    while (fgets(line, sizeof(line), stdin)) {
        unsigned mask = 0;
        for (char *p = line; *p && *p >= 'a' && *p <= 'z'; ++p) {
            mask |= 1 << (*p - 'a');
        }
        if (mask == 0) {
            answer1 += __builtin_popcount(un);
            answer2 += __builtin_popcount(in);
            un = 0;
            in = 0;
        } else if (un == 0) {
            un = mask;
            in = mask;
        } else {
            un |= mask;
            in &= mask;
        }
    }
    answer1 += __builtin_popcount(un);
    answer2 += __builtin_popcount(in);

    printf("%d\n%d\n", answer1, answer2);
}
