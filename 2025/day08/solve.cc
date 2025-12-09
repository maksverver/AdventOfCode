#include <algorithm>
#include <cstdio>
#include <vector>

struct Point {
    int x, y, z;
};

long long Square(int x) { return (long long) x * x;}

long long DistSq(const Point &p, const Point &q) {
    return Square(p.x - q.x) + Square(p.y - q.y) + Square(p.z - q.z);
}

struct Pair {
    int i, j;
    long long dist_sq;
};

struct Node {
    int parent;
    int size;
};

// Note: may overflow the stack!
int Root(std::vector<Node> &nodes, int v) {
    return v == nodes[v].parent ? v : nodes[v].parent = Root(nodes, nodes[v].parent);
}

int Combine(std::vector<Node> &nodes, int v, int w) {
    int x = Root(nodes, v);
    int y = Root(nodes, w);
    if (x == y) return 0;
    if (nodes[x].size < nodes[y].size) std::swap(x, y);
    int s = nodes[x].size + nodes[y].size;
    nodes[x].size = s;
    nodes[y].parent = x;
    return s;
}

int main() {
    std::vector<Point> points;
    for (Point p; scanf("%d,%d,%d\n", &p.x, &p.y, &p.z) == 3; ) {
        points.push_back(p);
    }
    const int N = points.size();

    std::vector<Pair> pairs;
    pairs.reserve(N * (N - 1) / 2);
    for (int i = 0; i < N; ++i) {
        for (int j = i + 1; j < N; ++j) {
            pairs.emplace_back(i, j, DistSq(points[i], points[j]));
        }
    }
    std::ranges::sort(pairs, {}, &Pair::dist_sq);

    std::vector<Node> nodes(N);
    for (int i = 0; i < N; ++i) nodes[i] = {i, 1};

    for (size_t n = 0; n < pairs.size(); ++n) {
        if (n == 1000) {
            // Part 1: product of biggest 3 components
            int biggest[3] = {0, 0, 0};
            for (int i = 0; i < N; ++i) {
                if (nodes[i].parent == i) {
                    int s = nodes[i].size;
                    if (s > biggest[0]) {
                        if (s > biggest[1]) {
                            biggest[0] = biggest[1];
                            if (s > biggest[2]) {
                                biggest[1] = biggest[2];
                                biggest[2] = s;
                            } else {
                                biggest[1] = s;
                            }
                        } else {
                            biggest[0] = s;
                        }
                    }
                }
            }
            printf("%lld\n", (long long) biggest[0] * biggest[1] * biggest[2]);
        }

        auto [i, j, dist] = pairs[n];
        int s = Combine(nodes, i, j);
        if (s == N) {
            // Part 2: product of x coordinates of last pair connected
            printf("%lld\n", (long long) points[i].x * points[j].x);
            break;
        }
    }
}
