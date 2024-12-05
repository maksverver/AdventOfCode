// Solution that runs in O(n) time using std::nth_element.
//
// Note: this is technically incorrect, just like incorrect.py

#include <algorithm>
#include <cassert>
#include <cstdio>
#include <vector>

const int LIM = 100;

static int order[LIM][LIM];

static bool compare(int p, int q) {
    return order[p][q] < 0;
}

static int peekc(FILE *fp) {
    int ch = getc(fp);
    ungetc(ch, fp);
    return ch;
}

int main() {
    long long answer1 = 0;
    long long answer2 = 0;
    while (peekc(stdin) != '\n') {
        int p = 0, q = 0;
        if (scanf("%d|%d", &p, &q) != 2 || getc(stdin) != '\n') {
            fprintf(stderr, "Invalid input\n");
            exit(1);
        }
        assert(p != q && 0 <= p && p < LIM && 0 <= q && q < LIM);
        order[p][q] = -1;
        order[q][p] = +1;
    }
    while (peekc(stdin) != EOF) {
        int p;
        if (scanf("%d", &p) != 1) {
            fprintf(stderr, "Invalid input\n");
            exit(1);
        }
        std::vector<int> v(1, p);
        while (scanf(",%d", &p) == 1) {
            v.push_back(p);
        }
        if (getc(stdin) != '\n') {
            fprintf(stderr, "Invalid input\n");
            exit(1);
        }
        assert(v.size() % 2 == 1);
        auto middle = v.begin() + v.size() / 2;
        if (std::is_sorted(v.begin(), v.end(), compare)) {
            answer1 += *middle;
        } else {
            std::nth_element(v.begin(), middle, v.end(), compare);
            answer2 += *middle;

        }
    }
    printf("%lld\n%lld\n", answer1, answer2);
}
