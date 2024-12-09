#include <cassert>
#include <iostream>
#include <ranges>
#include <vector>

long long Checksum(const std::vector<int> &disk_layout) {
    long long checksum = 0;
    for (size_t block = 0; block < disk_layout.size(); ++block) {
        int file = disk_layout[block];
        if (file >= 0) checksum += block * file;
    }
    return checksum;
}

long long Part1(const std::string &s) {
    std::vector<size_t> occupied;
    std::vector<int> disk_layout;
    for (size_t i = 0; i < s.size(); ++i) {
        int size = s[i] - '0';
        assert(0 <= size && size < 10);
        if (i % 2 == 0) {
            while (size-- > 0) {
                occupied.push_back(disk_layout.size());
                disk_layout.push_back(i / 2);
            }
        } else {
            while (size-- > 0) {
                disk_layout.push_back(-1);
            }
        }
    }
    for (size_t i = 0; i < disk_layout.size() && !occupied.empty(); ++i) {
        if (disk_layout[i] < 0) {
            size_t j = occupied.back();
            occupied.pop_back();
            if (j <= i) break;
            disk_layout[i] = disk_layout[j];
            disk_layout[j] = -1;
        }
    }
    return Checksum(disk_layout);
}

struct Span {
    size_t start, size;
};

long long Part2(const std::string &s) {
    std::vector<Span> files;
    std::vector<Span> spaces;
    
    size_t disk_size = 0;
    for (size_t i = 0; i < s.size(); ++i) {
        size_t size = s[i] - '0';
        assert(0 <= size && size < 10);
        (i % 2 ? spaces : files).push_back(Span{disk_size, size});
        disk_size += size;
    }

    for (Span &f : std::ranges::reverse_view(files)) {
        for (Span &s : spaces) {
            if (s.start > f.start) {
                break;
            }
            if (f.size <= s.size) {
                f.start = s.start;
                s.start += f.size;
                s.size -= f.size;
                break;
            }
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

int main() {
    std::string s;
    std::getline(std::cin, s);

    std::cout << Part1(s) << std::endl;
    std::cout << Part2(s) << std::endl;
}