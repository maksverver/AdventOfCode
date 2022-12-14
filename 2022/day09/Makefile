CXXFLAGS=$(shell pkg-config absl_flat_hash_set --cflags) -O3 -std=c++20 -Wall -Wextra  -Wno-sign-compare -mavx -funroll-loops
LDLIBS=$(shell pkg-config absl_flat_hash_set --libs)

all: 09

clean:
	rm -f 09
