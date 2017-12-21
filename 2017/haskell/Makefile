GHC=ghc -dynamic -O2

BIN=01 02 09-1 09-2 18

all: $(BIN)

%: %.hs
	$(GHC) -o $@ $<

clean:
	rm -f $(BIN) ./*.hi ./*.o
