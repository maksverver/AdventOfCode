GHC=ghc -dynamic -O2

TODO=20
FAST=01 02 03 04 04-alt 05 06 06-alt 07 08 09 10 11 12 12-alt 13 14 16 17 18 19 21 22 23 24 25
SLOW=15
ALL=$(FAST) $(SLOW)

all: $(ALL)

CA.o: CA.hs SortedList.o; $(GHC) $<
Deque.o: Deque.hs; $(GHC) $<
PairWiseAssociation.o: PairWiseAssociation.hs; $(GHC) $<
SortedList.o: SortedList.hs; $(GHC) $<

01: 01.hs; $(GHC) $<
02: 02.hs; $(GHC) $<
03: 03.hs; $(GHC) $<
04: 04.hs; $(GHC) $<
04-alt: 04-alt.hs; $(GHC) $<
05: 05.hs; $(GHC) $<
06: 06.hs; $(GHC) $<
06-alt: 06-alt.hs SortedList.o; $(GHC) $<
07: 07.hs; $(GHC) $<
08: 08.hs Deque.o; $(GHC) $<
09: 09.hs Deque.o; $(GHC) $<
10: 10.hs; $(GHC) $<
11: 11.hs; $(GHC) $<
12: 12.hs; $(GHC) $<
12-alt: 12-alt.hs; $(GHC) $<
13: 13.hs; $(GHC) $<
14: 14.hs; $(GHC) $<
15: 15.hs; $(GHC) $<
15-alt: 15-alt.hs; $(GHC) $<
16: 16.hs PairWiseAssociation.o; $(GHC) $<
17: 17.hs CA.o; $(GHC) $<
18: 18.hs; $(GHC) $<
19: 19.hs; $(GHC) $<
21: 21.hs PairWiseAssociation.o SortedList.o; $(GHC) $<
22: 22.hs Deque.o; $(GHC) $<
23: 23.hs; $(GHC) $<
24: 24.hs CA.o; $(GHC) $<
25: 25.hs; $(GHC) $<

test: $(FAST)
	@for case in $(FAST); do echo -n "Testing $${case}... "; ./$$case < ../testdata/$${case%-*}.in | diff ../testdata/$${case%-*}.ref* - && echo Passed || echo FAILED; done

test-slow: $(SLOW)
	@for case in $(SLOW); do echo -n "Testing $${case}... "; ./$$case < ../testdata/$${case%-*}.in | diff ../testdata/$${case%-*}.ref* - && echo Passed || echo FAILED; done

clean:
	rm -f $(ALL) ./*.hi ./*.o
