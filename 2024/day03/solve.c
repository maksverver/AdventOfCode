#include <stdio.h>
#include <stdbool.h>

enum State {
    STATE_INIT,
    STATE_D,
    STATE_DO,
    STATE_DOP,
    STATE_DON,
    STATE_DONO,
    STATE_DONOT,
    STATE_DONOTP,
    STATE_M,
    STATE_MU,
    STATE_MUL,
    STATE_MULP,
    STATE_MULPD,
    STATE_MULPDD,
    STATE_MULPDDD,
    STATE_MULPC,
    STATE_MULPCD,
    STATE_MULPCDD,
    STATE_MULPCDDD,
};

int main() {
    bool enabled = true;
    long long answer1 = 0;
    long long answer2 = 0;
    int state = STATE_INIT;
    int x = 0, y = 0;  /* prevent spurious warnings about uninitialized variables */

    for (int ch; (ch = getchar()) != EOF; ) {
        switch (state) {
            case STATE_INIT:
                switch (ch) {
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                } break;
            case STATE_D:
                switch (ch) {
                    case 'o': state = STATE_DO; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_DO:
                switch (ch) {
                    case '(': state = STATE_DOP; break;
                    case 'n': state = STATE_DON; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_DOP:
                switch (ch) {
                    case ')': enabled = true; state = STATE_INIT; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_DON:
                switch (ch) {
                    case '\'': state = STATE_DONO; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_DONO:
                switch (ch) {
                    case 't': state = STATE_DONOT; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_DONOT:
                switch (ch) {
                    case '(': state = STATE_DONOTP; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_DONOTP:
                switch (ch) {
                    case ')': enabled = false; state = STATE_INIT; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_M:
                switch (ch) {
                    case 'u': state = STATE_MU; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MU:
                switch (ch) {
                    case 'l': state = STATE_MUL; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MUL:
                switch (ch) {
                    case '(': state = STATE_MULP; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULP:
                switch (ch) {
                    case '0': case '1': case '2': case '3': case '4':
                    case '5': case '6': case '7': case '8': case '9':
                        x = ch - '0';
                        state = STATE_MULPD;
                        break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULPD:
                switch (ch) {
                    case '0': case '1': case '2': case '3': case '4':
                    case '5': case '6': case '7': case '8': case '9':
                        x = (10 * x) + (ch - '0');
                        state = STATE_MULPDD;
                        break;
                    case ',': state = STATE_MULPC; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULPDD:
                switch (ch) {
                    case '0': case '1': case '2': case '3': case '4':
                    case '5': case '6': case '7': case '8': case '9':
                        x = (10 * x) + (ch - '0');
                        state = STATE_MULPDDD;
                        break;
                    case ',': state = STATE_MULPC; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULPDDD:
                switch (ch) {
                    case ',': state = STATE_MULPC; break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULPC:
                switch (ch) {
                    case '0': case '1': case '2': case '3': case '4':
                    case '5': case '6': case '7': case '8': case '9':
                        y = ch - '0';
                        state = STATE_MULPCD;
                        break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULPCD:
                switch (ch) {
                    case '0': case '1': case '2': case '3': case '4':
                    case '5': case '6': case '7': case '8': case '9':
                        y = (10 * y) + (ch - '0');
                        state = STATE_MULPCDD;
                        break;
                    case ')': goto matched_mul;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULPCDD:
                switch (ch) {
                    case '0': case '1': case '2': case '3': case '4':
                    case '5': case '6': case '7': case '8': case '9':
                        y = (10 * y) + (ch - '0');
                        state = STATE_MULPCDDD;
                        break;
                    case ')': goto matched_mul;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
            case STATE_MULPCDDD:
                switch (ch) {
                    case ')': matched_mul:
                        answer1 += x * y;
                        if (enabled) answer2 += x * y; 
                        state = STATE_INIT;
                        break;
                    case 'd': state = STATE_D; break;
                    case 'm': state = STATE_M; break;
                    default: state = STATE_INIT; break;
                } break;
        }
    }

    printf("%lld\n%lld\n", answer1, answer2);
}
