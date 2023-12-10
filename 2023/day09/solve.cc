#include <algorithm>
#include <cstdio>
#include <cstdint>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

static int MOD = 1e9;
static int pascal[1000][1000];

static std::vector<std::vector<int>> rows;

int Solve(const std::vector<int> &row) {
  int64_t result = 0;
  const int *coefficients = pascal[row.size()];
  int sign = row.size() % 2 == 0 ? -1 : +1;
  for (int i = 0; i < row.size(); ++i) {
    result += (int64_t) row[i] * coefficients[i] * sign % MOD;
    sign = -sign;
  }
  return result % MOD;
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
  for (int i = 0; i < 1000; ++i) {
    pascal[i][0] = 1;
    for (int j = 1; j < i; ++j) pascal[i][j] = (pascal[i - 1][j - 1] + pascal[i - 1][j]) % MOD;
    pascal[i][i] = 1;
  }

  std::vector<std::vector<int>> rows = ParseInput(std::cin);

  std::cout << Solve(rows) << std::endl;

  for (std::vector<int> &row : rows) {
    std::ranges::reverse(row);
  }

  std::cout << Solve(rows) << std::endl;
}
