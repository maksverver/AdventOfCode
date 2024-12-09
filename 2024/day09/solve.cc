#include <cassert>
#include <iostream>
#include <ranges>
#include <set>
#include <string_view>
#include <vector>

struct File {
    size_t begin, end;
    int index;
};

__int128_t SolvePart1(const std::string_view &s) {
    // For each file: {{start block, end block}, file index}
    std::vector<File> files;
    size_t disk_size = 0;
    for (size_t i = 0; i < s.size(); ++i) {
        int size = s[i] - '0';
        assert((i % 2 == 0 ? 1 : 0) <= size && size < 10);
        if (i % 2 == 0) files.push_back(File{disk_size, disk_size + size, static_cast<int>(i / 2)});
        disk_size += size;
    }
    __int128_t checksum = 0;
    size_t i = 0, j = files.size();
    for (size_t disk_pos = 0; i < j; ++disk_pos) {
        auto &first_file = files[i];
        auto &last_file = files[j - 1];
        if (disk_pos == first_file.begin) {
            checksum += (__int128_t) disk_pos * first_file.index;
            if (++first_file.begin == first_file.end) ++i;
        } else {
            assert(disk_pos < first_file.begin);
            checksum += (__int128_t) disk_pos * last_file.index;
            if (--last_file.end == last_file.begin) --j;
        }
    }
    return checksum;
}

struct Span {
    size_t start, size;
};

__int128_t Checksum(const std::vector<int> &disk_layout) {
    __int128_t checksum = 0;
    for (size_t block = 0; block < disk_layout.size(); ++block) {
        int file = disk_layout[block];
        if (file >= 0) checksum += (__int128_t) block * file;
    }
    return checksum;
}

__int128_t SolvePart2(const std::string_view &s) {
    std::vector<Span> files;
    std::vector<Span> spaces;
    
    size_t disk_size = 0;
    for (size_t i = 0; i < s.size(); ++i) {
        size_t size = s[i] - '0';
        assert((i % 2 == 0 ? 1 : 0) <= size && size < 10);
        (i % 2 ? spaces : files).push_back(Span{disk_size, size});
        disk_size += size;
    }

    std::set<size_t> starts_by_size[10];
    for (auto [start, size] : spaces) {
        if (size > 0) starts_by_size[size].insert(start);
    }

    for (Span &f : std::ranges::reverse_view(files)) {
        size_t min_start = disk_size;
        size_t space_size = 0;
        for (int size = f.size; size < 10; ++size) {
            if (starts_by_size[size].empty()) continue;
            size_t start = *starts_by_size[size].begin();
            if (start < min_start) {
                min_start = start;
                space_size = size;
            }
        }
        if (min_start < f.start) {
            f.start = min_start;
            starts_by_size[space_size].erase(min_start);
            if (f.size < space_size) {
                starts_by_size[space_size - f.size].insert(min_start + f.size);
            }
        } else if (f.size == 1) {
            // Tiny optimization: if there is no space to move even the smallest
            // file, then no other files will be movable either, so we can stop.
            break;
        }
    }

    std::vector<int> disk_layout(disk_size, -1);
    for (size_t i = 0; i < files.size(); ++i) {
        auto [start, size] = files[i];
        for (size_t j = start; j < start + size; ++j) {
            disk_layout[j] = i;
        }
    }
    return Checksum(disk_layout);
}

//
// Benchmarking plumbing follows.
//

#include <chrono>

using namespace std::chrono;

// For memory map
#include "sys/mman.h"
#include "sys/stat.h"
#include "unistd.h"

struct Timer {
    Timer(const char *what) : what(what) {}

    ~Timer() {
        auto finish = high_resolution_clock::now();
        std::cerr << what << " took " << duration_cast<milliseconds>(finish - start) << '\n';
    }

    const char *what;
    high_resolution_clock::time_point start = high_resolution_clock::now();
};

static size_t FileSize(int fd) {
  struct stat st;
  int res = fstat(fd, &st);
  if (res != 0) {
    perror("fstat");
    exit(1);
  }
  return st.st_size;
}

std::string_view ReadInput() {
    Timer timer("Opening input");

    size_t len = FileSize(STDIN_FILENO);
    void *data = mmap(NULL, len, PROT_READ, MAP_SHARED, STDIN_FILENO, 0);
    assert(data != MAP_FAILED);

    const char *p = reinterpret_cast<const char*>(data);
    assert(len > 0 && p[len - 1] == '\n');
    return std::string_view(p, len - 1);
}

__int128_t SolvePart1Timed(const std::string_view &s) {
    Timer timer("Solving part 1");
    return SolvePart1(s);
}

__int128_t SolvePart2Timed(const std::string_view &s) {
    Timer timer("Solving part 2");
    return SolvePart2(s);
}

std::ostream &operator<<(std::ostream &os, __int128_t i) {
    assert(i > 0);
    char digits[40];
    size_t pos = 0;
    while (i > 0) {
        digits[pos++] = '0' + i % 10;
        i /= 10;
    }
    while (pos > 0) os << digits[--pos];
    return os;
}

int main() {
    std::string_view s = ReadInput();
    std::cout << SolvePart1Timed(s) << std::endl;
    std::cout << SolvePart2Timed(s) << std::endl;
}
