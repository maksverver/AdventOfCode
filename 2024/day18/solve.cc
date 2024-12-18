// Advent of Code 2024 day 18 part 2 solution in nearly linear time (and sometimes
// sublinear time).
//
// Example usage:
//
//  ./solve 70 < ../testdata/18.in
//
// The size argument is the value of the maximum coordinate in the input.
//
// The idea behind the algorithm is to frame it as a graph connectivity problem,
// where we consider the corners of grid cells as vertices of the graph, and the
// horizontal/vertical connections between them as potential edges.
//
// For example, if we have a grid with coordinates ranging from 0 to 2,
// inclusive, then we have 3x3 = 9 grid cells and 4x4 = 16 corner vertices:
//
//  +-+-+-+
//  |o|o|o|    here, 'o' are grid cells,
//  +-+-+-+    and '+' are corners of grid cells (the vertices of our graph)
//  |o|o|o|
//  +-+-+-+
//  |o|o|o|
//  +-+-+-+
//
// There is a path in the grid from the topleft cell to bottomright cell if and
// only if there is no path in the corner graph from the bottomleft corner to
// the topright corner excluding the topleftmost and bottomrightmost corners.
// (Proof is left as exercise to the reader)
//
// To simplify the implemntation, we combine all vertices on the bottom/left
// into one vertex, and all vertices on the top/right into another vertex.
//
// Now instead of detecting when the grid becomes disconnected, we can detect
// when the corner graph becomes connected. The second problem is easy to solve
// efficiently using a disjoint-set data structure.
//
// We read all cell coordinates one by one, and connect up to four pairs of
// corner vertices corresponding to the four sides of the cell, until the topleft
// and bottomright become connected.

#include <cassert>
#include <cstdio>
#include <ios>
#include <iostream>
#include <limits>
#include <utility>
#include <vector>

// UNION-FIND DATASTRUCTURE
//
// Keeps track of a partition of elements (identified by integers in the range
// 0 to count) into disjoint sets.
//
// combine() and find() run in almost constant amortized time.
class UnionFind {
  std::vector<std::pair<int, int>> pr; // list of {parent node, rank (subtree size)} pairs

public:
  // Constructs a union-find datastructure with 'nodes' distinct sets
  UnionFind(int nodes) {
    pr.resize(nodes);
    for (int i = 0; i < nodes; ++i) pr[i] = {i, 1};
  }

  // Combines the distinct sets to which u and v belong and returns true,
  // or returns false if u and v were already in the same set.
  bool combine(int u, int v) {
    if ((u = find(u)) == (v = find(v))) return false;
    if(pr[u].second < pr[v].second) std::swap(u, v);
    pr[u].second += pr[v].second;  // update rank of set of u
    pr[v].first  = u;		           // add v to set of u
    return true;
  }

  // Returns a set identifier for v, so that find(u) == find(v) if
  // u and v are in the same set.
  int find(int v) {
    assert(v >= 0 && v < pr.size());
    if (pr[v].first == v) return v;
    return pr[v].first = find(pr[v].first);
  }
};

int main(int argc, char *argv[]) {
    std::cin.tie(nullptr);
    std::ios_base::sync_with_stdio(false);
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <size>" << std::endl;
        return 1;
    }
    int s = std::stoi(argv[1]);
    if (s < 1 || s > std::numeric_limits<int>::max() / s) {
        std::cerr << "Invalid size\n";
        return 1;
    }
    const int bl = s*s + 0;  // bottom/left side
    const int tr = s*s + 1;  // top/right side
    UnionFind uf(s*s + 2);
    for (int t = 0; ; ++t) {
        int x, y;
        char comma;
        if (!(std::cin >> x >> comma >> y) || comma != ',') {
            if (std::cin.eof()) {
                std::cerr << "No solution found! (size argument may be wrong?)" << std::endl;
            } else {
                std::cerr << "Unexpected input at line " << t + 1 << std::endl;
            }
            return 1;
        }
        if (x < 0 || x > s || y < 0 || y > s) {
            std::cerr << "Invalid coordinates on line " << (t + 1) << std::endl;
            return 1;
        }
        if (y != 0) uf.combine(x==0 ? bl : (x-1)+(y-1)*s, x==s ? tr : (x-0)+(y-1)*s);  // top
        if (y != s) uf.combine(x==0 ? bl : (x-1)+(y-0)*s, x==s ? tr : (x-0)+(y-0)*s);  // bottom
        if (x != 0) uf.combine(y==0 ? tr : (x-1)+(y-1)*s, y==s ? bl : (x-1)+(y-0)*s);  // left
        if (x != s) uf.combine(y==0 ? tr : (x-0)+(y-1)*s, y==s ? bl : (x-0)+(y-0)*s);  // right
        if (uf.find(bl) == uf.find(tr)) {
            printf("%d,%d\n", x, y);
            return 0;
        }
    }
}
