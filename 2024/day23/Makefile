CLAGS=-O3 -Wall -march=native
CXXFLAGS=-O3 -Wall -march=native

SOLUTIONS=solve-part-1 solve-cliquer-part-1 solve-cliquer-part-2

all: $(SOLUTIONS)

solve-cliquer-part-1: solve-cliquer-part-1.c solve-cliquer-common.c
	$(CC) $(CFLAGS) -o $@ $^ -lcliquer

solve-cliquer-part-2: solve-cliquer-part-2.c solve-cliquer-common.c
	$(CC) $(CFLAGS) -o $@ $^ -lcliquer

clean:
	rm -f $(SOLUTIONS)

.PHONY: all clean
