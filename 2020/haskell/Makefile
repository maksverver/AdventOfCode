ALL=01 02 03 04 04-alt
GHC=ghc -dynamic -O

all: $(ALL)

01: 01.hs; $(GHC) $<
02: 02.hs; $(GHC) $<
03: 03.hs; $(GHC) $<
04: 04.hs; $(GHC) $<
04-alt: 04-alt.hs; $(GHC) $<

test: $(ALL)
	for case in $(ALL); do ./$$case < testdata/$${case%-*}.in | diff testdata/$${case%-*}.ref - ; done

clean:
	rm -f $(ALL) ./*.hi ./*.o
