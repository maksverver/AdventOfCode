// Variant of solve.cc that uses a custom int128 implementation instead of
// the nonstandard __int128_t builtin type.

#include <cassert>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <queue>
#include <ranges>
#include <string_view>
#include <vector>

struct File {
    size_t begin, end;
    int index;
};

struct FakeInt128 {
    constexpr static uint64_t mod = 1e18;

    uint64_t lower = 0;
    uint64_t upper = 0;

    FakeInt128 &operator+=(int64_t i) {
        assert(i >= 0);  // I'm too lazy to support this
        lower += i % mod;
        upper += i / mod;
        if (lower >= mod) {
            upper += 1;
            lower -= mod;
        }
        return *this;
    }
};

std::ostream &operator<<(std::ostream &os, const FakeInt128 &i) {
    if (i.upper == 0) {
        return os << i.lower;
    }
    return os << i.upper << std::setfill('0') << std::setw(18) << i.lower;
}

FakeInt128 SolvePart1(const std::string_view &s) {
    std::vector<File> files;
    size_t disk_size = 0;
    for (size_t i = 0; i < s.size(); ++i) {
        int size = s[i] - '0';
        assert((i % 2 == 0 ? 1 : 0) <= size && size < 10);
        if (i % 2 == 0) files.push_back(File{disk_size, disk_size + size, static_cast<int>(i / 2)});
        disk_size += size;
    }
    FakeInt128 checksum = {};
    size_t i = 0, j = files.size();
    for (size_t disk_pos = 0; i < j; ++disk_pos) {
        auto &first_file = files[i];
        auto &last_file = files[j - 1];
        if (disk_pos == first_file.begin) {
            checksum += disk_pos * first_file.index;
            if (++first_file.begin == first_file.end) ++i;
        } else {
            assert(disk_pos < first_file.begin);
            checksum += disk_pos * last_file.index;
            if (--last_file.end == last_file.begin) --j;
        }
    }
    return checksum;
}

FakeInt128 SolvePart2(const std::string_view &s) {
    // For each file: begin block index and end block index (exclusive).
    std::vector<std::pair<size_t, size_t>> files;

    // starts_by_size[s] contains the starting indices of all spaces of size s.
    // This allows us to find the leftmost space where a file of size `fs` fits
    // by checking the smallest element of starts_by_size[s] where fs <= s <= 9.
    std::priority_queue<size_t, std::vector<size_t>, std::greater<size_t>> starts_by_size[10];
    
    size_t disk_size = 0;
    for (size_t i = 0; i < s.size(); ++i) {
        size_t size = s[i] - '0';
        assert(0 <= size && size < 10);
        if (size == 0) continue;
        if (i % 2 == 0) {
            files.push_back({disk_size, size});
        } else {
            starts_by_size[size].push(disk_size);
        }
        disk_size += size;
    }

    for (auto &[file_start, file_size] : std::ranges::reverse_view(files)) {
        size_t min_start = disk_size;
        size_t space_size = 0;
        for (int size = file_size; size < 10; ++size) {
            if (starts_by_size[size].empty()) continue;
            size_t start = starts_by_size[size].top();
            if (start < min_start) {
                min_start = start;
                space_size = size;
            }
        }
        if (min_start < file_start) {
            file_start = min_start;
            starts_by_size[space_size].pop();
            if (file_size < space_size) {
                starts_by_size[space_size - file_size].push(min_start + file_size);
            }
        } else if (file_size == 1) {
            // Tiny optimization: if there is no space to move even the smallest
            // file, then no other files will be movable either, so we can stop.
            break;
        }
    }

    FakeInt128 checksum = {};
    for (size_t i = 0; i < files.size(); ++i) {
        auto [start, size] = files[i];
        for (size_t j = start; j < start + size; ++j) checksum += (__int128_t) i * j;
    }
    return checksum;
}

//
// Benchmarking plumbing follows.
//

#include <chrono>

using namespace std::chrono;

struct Timer {
    Timer(const char *what) : what(what) {}

    ~Timer() {
        auto finish = high_resolution_clock::now();
        std::cerr << what << " took " << duration_cast<milliseconds>(finish - start) << '\n';
    }

    const char *what;
    high_resolution_clock::time_point start = high_resolution_clock::now();
};

#if OPEN_WITH_MMAP
#include "sys/mman.h"
#include "sys/stat.h"
#include "unistd.h"

static size_t FileSize(int fd) {
  struct stat st;
  int res = fstat(fd, &st);
  if (res != 0) {
    perror("fstat");
    exit(1);
  }
  return st.st_size;
}

std::string_view OpenInput() {
    Timer timer("Opening input");

    size_t len = FileSize(STDIN_FILENO);
    void *data = mmap(NULL, len, PROT_READ, MAP_SHARED, STDIN_FILENO, 0);
    assert(data != MAP_FAILED);

    const char *p = reinterpret_cast<const char*>(data);
    assert(len > 0 && p[len - 1] == '\n');
    return std::string_view(p, len - 1);
}
#endif

std::string ReadInput() {
    Timer timer("Reading input");
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::string line;
    std::getline(std::cin, line);
    return line;
}

FakeInt128 SolvePart1Timed(const std::string_view &s) {
    Timer timer("Solving part 1");
    return SolvePart1(s);
}

FakeInt128 SolvePart2Timed(const std::string_view &s) {
    Timer timer("Solving part 2");
    return SolvePart2(s);
}

int main() {
#if OPEN_WITH_MMAP
    std::string_view s = OpenInput();
#else
    std::string s = ReadInput();
#endif
    std::cout << SolvePart1Timed(s) << std::endl;
    std::cout << SolvePart2Timed(s) << std::endl;
}
