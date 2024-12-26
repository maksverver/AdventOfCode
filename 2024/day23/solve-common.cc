#include "solve-common.h"

#include <cctype>

std::optional<int> ParseVertex(std::string_view s) {
    if (s.size() == 2 &&
             'a' <= s[0] && s[0] <= 'z' &&
             'a' <= s[1] && s[1] <= 'z') {
        int i = s[0] - 't';
        int j = s[1] - 'a';
        return 26*(i >= 0 ? i : i + 26) + j;
    }
    return std::nullopt;
}

std::optional<std::pair<int, int>> ParseEdge(std::string_view s) {
    while (s.size()  > 0 && isspace(s.back())) {
        s = s.substr(0, s.size() - 1);
    }
    if (s.size() == 5 && s[2] == '-') {
        auto v = ParseVertex(s.substr(0, 2));
        auto w = ParseVertex(s.substr(3, 2));
        if (v && w) return std::make_pair(*v, *w);
    }
    return std::nullopt;
}

std::string VertexName(int v) {
    int c = 't' + v / 26;
    int d = 'a' + v % 26;
    if (c > 'z') c -= 26;
    return std::string{(char) c, (char) d};
}
