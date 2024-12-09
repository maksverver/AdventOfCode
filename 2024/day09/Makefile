CXXFLAGS=-O3 -g -Wall -march=native -std=c++20 -DNDEBUG -DOPEN_WITH_MMAP=0

# For debugging:
#CXXFLAGS=-O0 -g -Wall -march=native -std=c++20 -D_GLIBCXX_DEBUG

SOLUTIONS=solve solve-fakeint128

all: $(SOLUTIONS)

clean:
	rm -f $(SOLUTIONS)

.PHONY: all clean
