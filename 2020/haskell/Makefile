ALL=01 02 03 04 04-alt 05 06 06-alt 07 08 09 10 11 12 12-alt 13 15
GHC=ghc -dynamic -O

all: $(ALL)

01: 01.hs; $(GHC) $<
02: 02.hs; $(GHC) $<
03: 03.hs; $(GHC) $<
04: 04.hs; $(GHC) $<
04-alt: 04-alt.hs; $(GHC) $<
05: 05.hs; $(GHC) $<
06: 06.hs; $(GHC) $<
06-alt: 06-alt.hs; $(GHC) $<
07: 07.hs; $(GHC) $<
08: 08.hs Deque.hs; $(GHC) $<
09: 09.hs Deque.hs; $(GHC) $<
10: 10.hs; $(GHC) $<
11: 11.hs; $(GHC) $<
12: 12.hs; $(GHC) $<
12-alt: 12-alt.hs; $(GHC) $<
13: 13.hs; $(GHC) $<
15: 15.hs; $(GHC) $<
15-alt: 15-alt.hs; $(GHC) $<

test: $(ALL)
	for case in $(ALL); do echo -n "Testing $${case}... "; ./$$case < ../testdata/$${case%-*}.in | diff ../testdata/$${case%-*}.ref - && echo Passed || echo FAILED; done

clean:
	rm -f $(ALL) ./*.hi ./*.o
