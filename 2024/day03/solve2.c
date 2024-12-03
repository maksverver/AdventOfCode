#include <stdio.h>
#include <stdbool.h>

int main() {
    bool enabled = true;
    long long answer1 = 0;
    long long answer2 = 0;
    int x, y;
    char ch;

init:
    switch (getchar()) {
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
        case EOF: goto eof;
    }
d:
    switch (getchar()) {
        case 'o': goto _do;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
_do:
    switch (getchar()) {
        case '(': goto dop;
        case 'n': goto don;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
dop:
    switch (getchar()) {
        case ')': enabled = true; goto init;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
don:
    switch (getchar()) {
        case '\'': goto dono;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
dono:
    switch (getchar()) {
        case 't': goto donot;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
donot:
    switch (getchar()) {
        case '(': goto donotp;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
donotp:
    switch (getchar()) {
        case ')': enabled = false; goto init;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
m:
    switch (getchar()) {
        case 'u': goto mu;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mu:
    switch (getchar()) {
        case 'l': goto mul;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mul:
    switch (getchar()) {
        case '(': goto mulp;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulp:
    switch (ch = getchar()) {
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
            x = ch - '0';
            goto mulpd;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulpd:
    switch (ch = getchar()) {
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
            x = (10 * x) + (ch - '0');
            goto mulpdd;
        case ',': goto mulpc;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulpdd:
    switch (ch = getchar()) {
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
            x = (10 * x) + (ch - '0');
            goto mulpddd;
        case ',': goto mulpc;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulpddd:
    switch (getchar()) {
        case ',': goto mulpc;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulpc:
    switch (ch = getchar()) {
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
            y = ch - '0';
            goto mulpcd;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulpcd:
    switch (ch = getchar()) {
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
            y = (10 * y) + (ch - '0');
            goto mulpcdd;
        case ')': goto matched_mul;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulpcdd:
    switch (ch = getchar()) {
        case '0': case '1': case '2': case '3': case '4':
        case '5': case '6': case '7': case '8': case '9':
            y = (10 * y) + (ch - '0');
            goto mulpcddd;
        case ')': goto matched_mul;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
mulpcddd:
    switch (getchar()) {
        case ')': matched_mul:
            answer1 += x * y;
            if (enabled) answer2 += x * y; 
            goto init;
        case 'd': goto d;
        case 'm': goto m;
        default: goto init;
    }
eof:
    printf("%lld\n%lld\n", answer1, answer2);
}
