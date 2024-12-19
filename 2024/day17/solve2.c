// Version of solve2.c which converts more of the logic into C code,
// allowing more to be optimized.
//
// Specifically, the decoding logic depends only on the two operands to the
// two `bxl` instructions. We can use that to calculate the output values
// without simulating the program explicitly.
//
// This runs super fast in practice (less than 100 micro(!)seconds), even though
// part 2 needs about 1000 recursive invocations of SolveBackward().

#include <assert.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>

static int NextOutput(uint64_t A, int x, int y) {
    int tmp = (A & 7) ^ x;
    return tmp ^ y ^ ((A >> tmp) & 7);
}

static void Part1(uint64_t A, int x, int y) {
    for (int i = 0; A != 0; ++i) {
        int val = NextOutput(A, x, y);
        A >>= 3;
        if (i > 0) putchar(',');
        printf("%d", val);
    }
    printf("\n");
}

static uint64_t SolveBackward(const int program[16], int x, int y, uint64_t A, int pos) {
    if (pos-- == 0) return A;

    uint64_t answer = -1;
    for (unsigned bits = 0; bits < 8; ++bits) {
        uint64_t next_A = (A << 3) | bits;
        int val = NextOutput(next_A, x, y);
        if (val == program[pos]) {
            uint64_t next_answer = SolveBackward(program, x, y, next_A, pos);
            if (next_answer < answer) answer = next_answer;
        }
    }
    return answer;
}

static void Part2(const int program[16], int x, int y) {
    printf("%" PRIu64 "\n", SolveBackward(program, x, y, 0, 16));
}

#include <stdlib.h>
#include <time.h>

static struct timespec Now() {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) == -1) {
        perror("clock_gettime");
        exit(1);
    }
    return ts;
}

int main() {
    struct timespec start = Now();

    uint64_t initial_A;
    uint64_t initial_B;
    uint64_t initial_C;
    int program[16];
    if (scanf(
            "Register A: %" SCNu64 "\n"
            "Register B: %" SCNu64 "\n"
            "Register C: %" SCNu64 "\n"
            "\n"
            "Program: %d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
            &initial_A, &initial_B, &initial_C,
            &program[ 0], &program[ 1], &program[ 2], &program[ 3], 
            &program[ 4], &program[ 5], &program[ 6], &program[ 7], 
            &program[ 8], &program[ 9], &program[10], &program[11], 
            &program[12], &program[13], &program[14], &program[15]
        ) != 19 || !feof(stdin) || initial_A < 0 || initial_B != 0 || initial_C != 0) {
        fprintf(stderr, "Invalid input!\n");
        return 1;
    }

    int x = -1, y = -1;
    assert(program[ 0] == 2 && program[ 1] == 4);  // bst A
    assert(program[14] == 3 && program[15] == 0);  // jnz 0
    for (int i = 2; i < 14; i += 2) {
        if (program[i] == 1) {  // bxl
            if (x == -1) {
                x = program[i + 1];
            } else if (y == -1) {
                y = program[i + 1];
            } else {
                fprintf(stderr, "Too many bxl instructions!\n");
                return 1;
            }
        }
    }
    if (y == -1) {
        fprintf(stderr, "Not enough bxl instructions!\n");
        return 1;
    }

    Part1(initial_A, x, y);
    Part2(program, x, y);

    struct timespec finish = Now();

    fprintf(stderr, "Execution time: %lld ns\n",
        (long long) 1e9 * (finish.tv_sec - start.tv_sec) + (finish.tv_nsec - start.tv_nsec));
}
