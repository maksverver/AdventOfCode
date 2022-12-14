GHC=ghc -dynamic -O2

ALL=solve-part-1

all: $(ALL)

solve-part-1: solve-part-1.hs; $(GHC) $<

clean:
	rm -f solve-part-1 ./*.hi ./*.o
