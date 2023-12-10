#include <algorithm>
#include <cstdio>
#include <cstdint>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

static int MOD = 1e9;

static std::vector<std::vector<int>> rows;

bool AllZeros(const std::vector<int> &row) {
  for (int i : row) if (i != 0) return false;
  return true;
}

int Solve(const std::vector<int> &row) {
  if (AllZeros(row)) return 0;

  std::vector<int> next_row(row.size() - 1);
  for (size_t i = 0; i < row.size() - 1; ++i) {
    next_row[i] = (row[i + 1] - row[i]) % MOD;
  }
  return (row.back() + Solve(next_row)) % MOD;
}

int Solve(const std::vector<std::vector<int>> rows) {
  int64_t sum = 0;
  for (const auto &row : rows) sum += Solve(row);
  sum %= MOD;
  if (sum < 0) sum += MOD;
  return sum;
}

std::vector<std::vector<int>> ParseInput(std::istream &is) {
  std::vector<std::vector<int>> rows;
  std::string line;
  while (std::getline(is, line)) {
    std::vector<int> row;
    std::istringstream iss(line);
    int i;
    while (iss >> i) row.push_back(i);
    rows.push_back(row);
  }
  return rows;
}

int main() {
  std::vector<std::vector<int>> rows = ParseInput(std::cin);

  std::cout << Solve(rows) << std::endl;

  for (std::vector<int> &row : rows) {
    std::ranges::reverse(row);
  }

  std::cout << Solve(rows) << std::endl;
}
