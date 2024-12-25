#include <bitset>
#include <cassert>
#include <iostream>
#include <string>
#include <string_view>

namespace {

const int V = 26*26;  // 676

// Parses a vertex into an integer such that the result value is between 0 and
// 26 (exclusive) when `s` starts with 't', and between 26 and V otherwise.
int ParseVertex(std::string_view s) {
    int i = s[0] - 't';
    int j = s[1] - 'a';

    return 26*(i >= 0 ? i : i + 26) + j;
}

// Formatting wrapper. Useful for debugging.
struct F { int v; };

std::ostream &operator<<(std::ostream &os, F f) {
    char c = 't' + f.v / 26;
    char d = 'a' + f.v % 26;
    if (c > 'z') c -= 26;
    return os << c << d;
}

// adjacent[v] == bitset of vertices w such that v < w and there is an edge (v, w)
static std::bitset<V> adjacent[V];

}  // namespace

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    while (std::cin >> line) {
        if (line.size() == 5 &&
                'a' <= line[0] && line[0] <= 'z' && 
                'a' <= line[1] && line[1] <= 'z' && 
                line[2] == '-' &&
                'a' <= line[3] && line[3] <= 'z' &&
                'a' <= line[4] && line[4] <= 'z') [[likely]] {
            int v = ParseVertex(std::string_view(line).substr(0, 2));
            int w = ParseVertex(std::string_view(line).substr(3, 5));
            assert(v != w);
            if (v > w) std::swap(v, w);
            adjacent[v][w] = true;
        } else {
            std::cerr << "Invalid input line: " << line << '\n';
            return 1;
        }
    }

    // Count all ordered triples that include at least one 't'.
    //
    // This relies on the fact that the virst 26 vertices are the t-vertices,
    // and that the bitmasks contain only neighbors with greater indexes to
    // avoid double-counting.
    //
    // Time complexity is 26 × V × (V / wordsize), which is approximately
    // 26**5 / wordsize or about 185647 operations with 64-bit words, though
    // they are pretty fast in practice.
    long long total = 0;
    for (int v = 0; v < 26; ++v) {
        for (int w = v + 1; w < V; ++w) {
            if (adjacent[v][w]) total += (adjacent[v] & adjacent[w]).count();
        }
    }
    std::cout << total << '\n';
}
