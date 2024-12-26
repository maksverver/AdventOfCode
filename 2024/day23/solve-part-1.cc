#include <bitset>
#include <cassert>
#include <iostream>
#include <string>
#include <string_view>

#include "solve-common.h"

// adjacent[v] == bitset of vertices w such that v < w and there is an edge (v, w)
static std::bitset<V> adjacent[V];

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    for (int lineno = 1; std::cin >> line; ++lineno) {
        if (auto res = ParseEdge(line)) {
            auto [v, w] = *res;
            assert(v != w);
            if (v > w) std::swap(v, w);
            adjacent[v][w] = true;
        } else {
            std::cerr << "Invalid input on line " << lineno << std::endl;
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
