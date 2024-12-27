// Advent of Code 2024 Day 23: LAN Party
// https://adventofcode.com/2024/day/23
//
// The problem asks us to find the maximum clique in a graph. This solution
// implements the algorithm from Patric R.J. Östergård
// “A fast algorithm for the maximum clique problem” (2002)
// https://www.sciencedirect.com/science/article/pii/S0166218X01002906
//
// It is similar to the implementation in Cliquer:
// https://users.aalto.fi/~pat/cliquer.html
//

#include <algorithm>
#include <bitset>
#include <cassert>
#include <iostream>
#include <string>
#include <vector>

#include "solve-common.h"

namespace {

// adjacent[v] == bitset of vertices w such that there is an edge (v, w)
std::vector<std::bitset<V>> adjacent(V);

// Calculates a vertex ordering based on a greedy coloring of the graph.
std::array<int, V> GreedyColoringOrder() {
    std::vector<int> degree(V);
    for (int v = 0; v < V; ++v) degree[v] = adjacent[v].count();

    std::bitset<V> uncolored;
    uncolored.set();

    std::bitset<V> avail = uncolored;
    std::array<int, V> order;
    for (int colored = 0; colored < V; ) {
        int max_degree = -1;
        int best_v = -1;
        for (int v = avail._Find_first(); v < V; v = avail._Find_next(v)) {
            if (degree[v] > max_degree) {
                max_degree = degree[v];
                best_v = v;
            }
        }
        if (best_v >= 0) {
            // Color best_v and mark neighbors unavailable.
            order[colored++] = best_v;
            uncolored.reset(best_v);
            avail.reset(best_v);

            // Remove `best_v` from graph and update degree accordingly.
            for (int w = 0; w < V; ++w) {
                if (adjacent[best_v][w]) {
                    avail.reset(w);
                    degree[w]--;
                }
            }
        } else {
            // Move on to next color, and mark all uncolored vertices available again.
            avail = uncolored;
        }
    }
    return order;
}

// Reorders the adjacency matrix according to the given vertex order.
//
// order[0] becomes the first vertex, order[1] becomes the second, and so on.
void Reorder(const std::array<int, V> &order) {
    std::vector<std::bitset<V>> a(V);
    for (size_t i = 0; i < V; ++i) {
        for (size_t j = 0; j < V; ++j) {
            if (adjacent[order[i]][order[j]]) a[i][j] = true;
        }
    }
    adjacent = std::move(a);
}

// subgraph_max_clique_size[N] is the size of the maximum clique in the subgraph
// of size N with vertices 0, 1, .., N-1.
std::vector<int> subgraph_max_clique_size;

// new_clique holds the clique found by Search() (if it returns `true`).
std::vector<int> new_clique;

// Searches for a clique of size `size` in the subgraph induced by the vertex
// set P, which includes only vertices between 0 and N (exclusive).
//
// Returns `true` if a clique of the requested size is found; in that case, the
// vertices that form the clique are added to `new_clique`.
bool Search(std::bitset<V> P, int N, int size) {
    if (size == 0) return true;
    if (size > (int) P.count()) return false;
    for (int v = N - 1; v >= 0; --v) {
        if (!P[v]) continue;
        if (size - 1 > subgraph_max_clique_size[v]) break;  // prune
        if (Search(P & adjacent[v], v, size - 1)) {
            new_clique.push_back(v);
            return true;
        }
        P.reset(v);
    }
    return false;
}

}  // namespace

int main() {
    // Parse input.
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::string line;
    for (int lineno = 1; std::cin >> line; ++lineno) {
        if (auto res = ParseEdge(line)) {
            auto [v, w] = *res;
            if (v != w) {
                adjacent[v][w] = true;
                adjacent[w][v] = true;
            } else {
                std::cerr << "Loop on line " << lineno << " (ignored)\n";
            }
        } else {
            std::cerr << "Invalid input on line " << lineno << std::endl;
            return 1;
        }
    }

    // Reorder vertices according to a greedy coloring.
    auto order = GreedyColoringOrder();
    Reorder(order);

    // Search for the maximum clique. This uses Östergård's algorithm: we
    // calculate the maximum clique in the subgraph of vertices 0..v for
    // increasing values of v; the sizes of cliques are necessarily increasing,
    // and values found earlier allow us to prune in Search().
    std::vector<int> max_clique;
    subgraph_max_clique_size.push_back(max_clique.size());
    for (int v = 0; v < V; ++v) {
        std::bitset<V> P;
        for (int w = 0; w < v; ++w) if (adjacent[v][w]) P.set(w);
        new_clique.clear();
        if (Search(P, v, max_clique.size())) {
            new_clique.push_back(v);
            max_clique = new_clique;
        }
        subgraph_max_clique_size.push_back(max_clique.size());
    }

    // Print the answer: recover the original vertex names (before reordering),
    // sort them alphabetically, and print them as a comma-separated string.
    std::vector<std::string> names;
    for (int v : max_clique) names.push_back(VertexName(order[v]));
    std::ranges::sort(names);
    for (size_t i = 0; i < names.size(); ++i) {
        if (i > 0) std::cout << ',';
        std::cout << names[i];
    }
    std::cout << std::endl;
}
