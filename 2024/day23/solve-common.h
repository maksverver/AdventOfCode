#ifndef SOLVE_COMMON_H_INCLUDED
#define SOLVE_COMMON_H_INCLUDED

#include <iostream>
#include <optional>
#include <ranges>
#include <span>
#include <string_view>
#include <utility>

const int V = 26*26;  // 676

// Parses a vertex into an integer such that the result value is between 0 and
// 26 (exclusive) when `s` starts with 't', and between 26 and V otherwise.
std::optional<int> ParseVertex(std::string_view s);

// Parses an edge into a pair of vertex ids.
std::optional<std::pair<int, int>> ParseEdge(std::string_view s);

// Returns the alphabetic name of the given vertex.
std::string VertexName(int v);

#endif  // ndef SOLVE_COMMON_H_INCLUDED
