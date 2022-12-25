CXXFLAGS=-Wall -Wextra -O3 -march=native -std=c++20 -Wno-sign-compare
#CXXFLAGS=-Wall -Wextra -Og -march=native -std=c++20 -Wno-sign-compare -g

CXXFLAGS+=$(shell pkg-config absl_flat_hash_set --cflags) -DWITH_ABSL_HASH_SET
LDLIBS+=$(shell pkg-config absl_flat_hash_set --libs)

all: solve

clean:
	rm -f solve
