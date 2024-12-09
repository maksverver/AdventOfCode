// Further optimized verison of solve.cc
//
//  - Runs part 1 in O(n) instead of O(nm) where m is the maximum length
//    (since m is 5 on average this is only a small improvement, but it still
//    runs about twice as fast).
//
//  - Runs part 2 in O(nm) instead of O(n(m + logn)).
//
//  - Emulates 128-bit operations instead of using nonstandard __int128_t
//    (not sure if that improves performance or not)
//

#include <cassert>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <string_view>
#include <vector>

struct File {
    size_t start, size;
};

struct FakeInt128 {
    constexpr static uint64_t mod = 1e18;

    uint64_t lower = 0;
    uint64_t upper = 0;

    FakeInt128 &operator+=(int64_t i) {
        assert(0 <= i && (uint64_t) i < mod);
        lower += i;
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

int64_t RangeSum(size_t start, size_t len) {
    return start * len + (len * (len - 1) / 2);
}

FakeInt128 SolvePart1(const std::vector<File> &files) {
    // Simulate moving blocks from the files at the end into the gaps in front.
    // For efficiency, we are not going to actually move blocks, but we will
    // loop through the block indices starting from 0, and calculate which file
    // index would be copied there, by keeping two pointers: one to the first
    // file with start >= block, and one to the last file we have not yet
    // (entirely) moved into empty gaps.
    FakeInt128 checksum = {};
    if (files.empty()) return checksum;
    size_t block = 0;
    size_t i = 0;
    size_t j = files.size() - 1;
    size_t last_file_size = files[j].size;
    while (i < j) {
        auto &first_file = files[i];
        if (block == first_file.start) {
            // Current disk block is at the start of the file, so keep the file.
        in_file:
            checksum += RangeSum(block, first_file.size) * i;
            block += first_file.size;
            ++i;
        } else {
            // Current disk block is at the start of the space. See how much of the last
            // file we can fit in there.
            assert(block < first_file.start);
            size_t space = first_file.start - block;
            if (space < last_file_size) {
                // Last file does not fit entirely into the gap; only copy part of it.
                checksum += RangeSum(block, space) * j;
                block += space;
                last_file_size -= space;
                // Tiny performance optimization: we know we must be at the start of
                // a file right now, so skip the if-statement at the top of the loop.
                assert(block == first_file.start);
                goto in_file;
            } else {
                // Last file fits entirely into the gap.
                checksum += RangeSum(block, last_file_size) * j;
                block += last_file_size;
                last_file_size = files[--j].size;
            }
        }
    }
    checksum += RangeSum(block, last_file_size) * j;
    return checksum;
}

FakeInt128 SolvePart2(const std::vector<File> &files) {
    // Tracks whether a file has been moved (so deleted from its original position)
    std::vector<char> deleted(files.size(), false);

    // Group file indices by size.
    std::vector<size_t> files_by_size[10];
    for (size_t i = 0; i < files.size(); ++i) {
        files_by_size[files[i].size].push_back(i);
    }

    // Now we will run through the blocks from left to right, greedily filling gaps
    // with the rightmost file that will fit in there. We can find those files in
    // O(m) time using the files_by_size arrays.
    FakeInt128 checksum = {};
    for (size_t block = 0, i = 0; i < files.size(); ) {
        auto [start, size] = files[i];
        if (block < start) {
            size_t space = start - block;
            size_t j = i, best_size = 0;
            for (size_t size = 1; size <= space; ++size) {
                if (!files_by_size[size].empty() && files_by_size[size].back() >= j) {
                    j = files_by_size[size].back();
                    best_size = size;
                }
            }
            if (best_size == 0) {
                // No file fits in this space. Skip it.
                block = start;
            } else {
                // Copy block j - 1
                assert(files_by_size[best_size].back() == j);
                files_by_size[best_size].pop_back();
                checksum += RangeSum(block, best_size) * j;
                block += best_size;
                assert(!deleted[j]);
                deleted[j] = true;
            }
        } else {
            assert(block == start);
            if (!deleted[i]) checksum += RangeSum(block, size) * i;
            block += size;
            ++i;
        }
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

FakeInt128 SolvePart1Timed(const std::vector<File> &files) {
    Timer timer("Solving part 1");
    return SolvePart1(files);
}

FakeInt128 SolvePart2Timed(const std::vector<File> &files) {
    Timer timer("Solving part 2");
    return SolvePart2(files);
}

std::vector<File> Preprocess(const std::string_view &s) {
    Timer timer("Preprocessing");
    std::vector<File> files;
    files.reserve((s.size() + 1) / 2);
    size_t disk_size = 0;
    for (size_t i = 0; i < s.size(); ++i) {
        size_t size = s[i] - '0';
        assert((i % 2 == 0 ? 1 : 0) <= size && size < 10);
        if (i % 2 == 0) files.push_back(File{disk_size, size});
        disk_size += size;
    }
    return files;
}

int main() {
#if OPEN_WITH_MMAP
    std::string_view s = OpenInput();
#else
    std::string s = ReadInput();
#endif
    std::vector<File> files = Preprocess(s);
    std::cout << SolvePart1Timed(files) << std::endl;
    std::cout << SolvePart2Timed(files) << std::endl;
}
