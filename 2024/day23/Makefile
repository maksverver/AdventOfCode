CLAGS=-O3 -Wall -march=native
CXXFLAGS=-std=c++20 -O3 -Wall -march=native

# For debugging:
#CXXFLAGS=-std=c++20 -O0 -Wall -march=native -D_GLIBCXX_DEBUG -g

SOLUTIONS=solve-part-1 solve-part-2 solve-cliquer-part-1 solve-cliquer-part-2

all: $(SOLUTIONS)

solve-part-1: solve-part-1.cc solve-common.cc
	$(CXX) $(CXXFLAGS) -o $@ $^

solve-part-2: solve-part-2.cc solve-common.cc
	$(CXX) $(CXXFLAGS) -o $@ $^

solve-cliquer-part-1: solve-cliquer-part-1.c solve-cliquer-common.c
	$(CC) $(CFLAGS) -o $@ $^ -lcliquer

solve-cliquer-part-2: solve-cliquer-part-2.c solve-cliquer-common.c
	$(CC) $(CFLAGS) -o $@ $^ -lcliquer

clean:
	rm -f $(SOLUTIONS)

.PHONY: all clean
