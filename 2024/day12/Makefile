all: challenge-1-and-2.zip

WIDTH1=729
WIDTH2=2187
INPUTS1=random-regions-1.txt sierpinsky-1.txt many-regions-1.txt circles-1.txt
INPUTS2=random-regions-2.txt sierpinsky-2.txt many-regions-2.txt circles-2.txt
IMAGES1=random-regions-1.png sierpinsky-1.png many-regions-1.png circles-1.png
IMAGES2=random-regions-2.png sierpinsky-2.png many-regions-2.png circles-2.png
FILES1=combined-1.txt $(INPUTS1) $(IMAGES1) solutions-1.txt
FILES2=combined-2.txt $(INPUTS2) $(IMAGES2) solutions-2.txt

%.png: %.txt; python3 visualize.py $< $@

clean:
	rm -f $(FILES1) $(FILES2) challenge-1.zip challenge-2.zip challenge-1-and-2.zip

random-regions-1.txt: gen-random-regions.py; pypy3 gen-random-regions.py $(WIDTH1) > $@
random-regions-2.txt: gen-random-regions.py; pypy3 gen-random-regions.py $(WIDTH2) > $@

sierpinsky-1.txt: gen-sierpinsky.py; pypy3 gen-sierpinsky.py $(WIDTH1) > $@
sierpinsky-2.txt: gen-sierpinsky.py; pypy3 gen-sierpinsky.py $(WIDTH2) > $@

many-regions-1.txt: gen-many-regions.py; pypy3 gen-many-regions.py $(WIDTH1) > $@
many-regions-2.txt: gen-many-regions.py; pypy3 gen-many-regions.py $(WIDTH2) > $@

circles-1.txt: gen-circles.py; pypy3 gen-circles.py $(WIDTH1) > $@
circles-2.txt: gen-circles.py; pypy3 gen-circles.py $(WIDTH2) > $@

combined-1.txt: $(INPUTS1); cat $^ > $@
combined-2.txt: $(INPUTS2); cat $^ > $@

solutions-1.txt: $(INPUTS1) combined-1.txt; for file in $^; do answers=$$(pypy3 solve.py < $$file); echo $$file: $$answers; done > $@
solutions-2.txt: $(INPUTS1) combined-2.txt; for file in $^; do answers=$$(pypy3 solve.py < $$file); echo $$file: $$answers; done > $@

challenge-1.zip: $(FILES1); rm -f $@; zip -9 $@ $^
challenge-2.zip: $(FILES2); rm -f $@; zip -9 $@ $^
challenge-1-and-2.zip: $(FILES1) $(FILES2); rm -f $@; zip -9 $@ $^
