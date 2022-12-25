SRC=main.rs common.rs day01.rs day02.rs

all: aoc

aoc: $(SRC)
	rustc -o $@ -O main.rs

clean:
	rm -f aoc

format:
	rustfmt $(SRC)

distclean: clean

.PHONY: all clean distclean format
