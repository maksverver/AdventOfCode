// Solver for Advent of Code 2024 Day 17: Chronospatial Computer.
//
// For part 1, I just simulate execution as described.
//
// For part 2, I disassembled my input program:
//
//   0: 2 4    bst A    B = A & 7
//   2: 1 5    bxl 5    B ^= 5
//   4: 7 5    cdv B    C = A >> B
//   6: 0 3    adv 3    A >>= 3
//   8: 1 6    bxl 6    B ^= 6
//  10: 4 3    bxc -    B ^= C
//  12: 5 5    out B    yield (B & 7)
//  14: 3 0    jnz 0    if A != 0: goto 0
//
// And observed:
//
//  - It executes a single loop while A > 0.
//  - Each iteration removes 3 bits from A.
//  - Each iteration outputs one value.
//  - Registers B and C are not preserved in the loop, so
//    the output value depends only on the contents of A.
//
// Combinng these allows us to solve part 2 by calculating backwards: we know
// that we end with A = 0, so we only need to try all 8 possible 3-bit patterns
// that could be in A  at the start of the final iteration, and check the
// generated output matches. Then we can try all valid values recursively
// (see SolveBackward() below).

#include <assert.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

struct State {
    uint64_t A, B, C;
    int ip;
};

int GetCombo(const struct State *s, int operand) {
    switch (operand & 7) {
        case 0: return 0;
        case 1: return 1;
        case 2: return 2;
        case 3: return 3;
        case 4: return s->A;
        case 5: return s->B;
        case 6: return s->C;
        default:
            fprintf(stderr, "Invalid combo operand\n");
            exit(1);
    }
}

int Run(const int program[16], struct State *s) {
    while (0 <= s->ip && s->ip < 16) {
        int opcode = program[s->ip];
        int operand = program[s->ip + 1];
        s->ip += 2;
        switch (opcode & 7) {
            case 0: s->A >>= GetCombo(s, operand); break;
            case 1: s->B ^= operand; break;
            case 2: s->B = GetCombo(s, operand) & 7; break;
            case 3: if (s->A != 0) s->ip = operand; break;
            case 4: s->B ^= s->C; break;
            case 5: return GetCombo(s, operand) & 7; break;
            case 6: s->B = s->A >> GetCombo(s, operand); break;
            case 7: s->C = s->A >> GetCombo(s, operand); break;
        }
    }
    return -1;
}

void Part1(const int program[16], uint64_t initial_A) {
    struct State s = {initial_A};
    for (int i = 0, value = 0; (value = Run(program, &s)) >= 0; ++i) {
        if (i > 0) putchar(',');
        printf("%d", value);
    }
    printf("\n");
}

uint64_t SolveBackward(const int program[16], uint64_t A, int pos) {
    if (pos-- == 0) return A;

    uint64_t answer = -1;
    for (unsigned bits = 0; bits < 8; ++bits) {
        uint64_t next_A = (A << 3) | bits;
        struct State s = {next_A};
        int val = Run(program, &s);
        if (val == program[pos]) {
            uint64_t next_answer = SolveBackward(program, next_A, pos);
            if (next_answer < answer) answer = next_answer;
        }
    }
    return answer;
}

void Part2(const int program[16]) {
    printf("%" PRIu64 "\n", SolveBackward(program, 0, 16));
}

int main() {
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

    Part1(program, initial_A);
    Part2(program);  
}