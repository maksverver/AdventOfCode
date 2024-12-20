// Advent of Code 2024 day 18 part 2 solution in linear time.
//
// Example usage:
//
//  ./solve 70 < ../testdata/18.in
//
// The size argument is the value of the maximum coordinate in the input.
//
// Solution logic: we start with all the dropped cells blocked, then solve
// backwards, removing blocked cells until there is a path from start (0, 0)
// to finish (size, size).
//
// To detect when there is a path, every cell of the grid is labeled one of
// four states: V(isited), U(nvisited), B(locked) or F(ringe). The meaning
// is as follows:
//
//  V(isited):   cell is reachable from the start.
//  U(nvisited): cell is not reachable from the start, but not itself blocked.
//  B(locked):   cell is blocked.
//  F(ringe):    cell is blocked, but it has a neighbor labeled V.
//
// We start by labeling all cells U(nvisited), then we read all drop points in
// the input and mark all of them B(locked). Do a flood fill from the start and
// change reachable U cells to V, and B cells adjacent to V cells to F.
//
// Now we have identified the maximum number of cells reachable from the start,
// as well as cells on the fringe. Typically the problem isn't solved yet, so we
// must work backwards. We remove dropped cells one by one, changing them from
// either (B)locked or (F)ringe to (U)nvisisted. If a cell was (F)ringe before,
// then we resume the flood fill starting from this cell. When the destination
// cell at (size, size) becomes labeled V then the problem is solved.

#include <cassert>
#include <ios>
#include <iostream>
#include <limits>
#include <vector>

enum State : char { U, B, F, V };

struct Point {
    int x, y;
};

const int DX[4] = { +1, 0, -1,  0};
const int DY[4] = {  0, +1, 0, -1};

int main(int argc, char *argv[]) {
    std::cin.tie(nullptr);
    std::ios_base::sync_with_stdio(false);
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <size>" << std::endl;
        return 1;
    }
    int size = std::stoi(argv[1]);
    if (size < 1 || size > std::numeric_limits<int>::max() / size) {
        std::cerr << "Invalid size\n";
        return 1;
    }

    auto grid = std::vector<std::vector<State>>(size + 1, std::vector<State>(size + 1, U));
    std::vector<Point> drops;
    for (int line = 1; ; ++line) {
        int x, y;
        char comma;
        if (!(std::cin >> x >> comma >> y) || comma != ',') {
            if (std::cin.eof()) break;
            std::cerr << "Invalid input at line " << line << std::endl;
            return 1;
        }
        if (x < 0 || x > size || y < 0 || y > size) {
            std::cerr << "Invalid coordinates on line " << line << " (wrong size specified?) " << std::endl;
            return 1;
        }
        State &s = grid[x][y];
        if (s != U) {
            // Assume coordinates are distinct. The problem statement is vague about whether
            // this is actually the case, but it is true for the official input.
            std::cerr << "Duplicate coordinates on line " << line << std::endl;
            return 1;
        }
        s = B;
        drops.push_back({x, y});
    }

    std::vector<Point> todo;
    auto explore = [&](int x, int y) {
        assert(grid[x][y] == U);
        grid[x][y] = V;
        todo.push_back({x, y});
        while (!todo.empty()) {
            auto [x, y] = todo.back();
            if (x == size && y == size) return true;
            assert(grid[x][y] == V);
            todo.pop_back();
            for (int dir = 0; dir < 4; ++dir) {
                int x2 = x + DX[dir];
                int y2 = y + DY[dir];
                if (0 <= x2 && x2 <= size && 0 <= y2 && y2 <= size) {
                    State &s = grid[x2][y2];
                    switch (s) {
                      case U: todo.push_back({x2, y2}); s = V; break;
                      case B: s = F; break;
                      case F: break;
                      case V: break;
                    }
                }
            }
        }
        return false;
    };

    if (grid[0][0] == B) {
        grid[0][0] = F;
    } else {
        if (explore(0, 0)) {
            std::cerr << "Path was never blocked!" << std::endl;
            return 1;
        }
    }

    while (!drops.empty()) {
        auto [x, y] = drops.back();
        drops.pop_back();
        State &s = grid[x][y];
        switch (s) {
            case B:
                s = U;
                break;

            case F:
                s = U;
                if (explore(x, y)) {
                    // Solution found!
                    std::cout << x << ',' << y << std::endl;
                    return 0;            
                }
                break;

            default:
                std::cerr << "Internal error" << std::endl; exit(1);
        }

        // Debug-print grid
        /*
        for (int y = 0; y <= size; ++y) {
            for (int x = 0; x <= size; ++x) {
                char ch = '?';
                switch (grid[x][y]) {
                    case U: ch = 'U'; break;
                    case B: ch = 'B'; break;
                    case F: ch = 'F'; break;                    
                    case V: ch = 'V'; break;
                }
                std::clog << ch;
            }
            std::clog << '\n';
        }
        std::clog << std::endl;
        */
    }

    std::cerr << "Internal error: path never became unblocked" << std::endl;
    exit(1);
}
