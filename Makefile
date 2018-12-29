
.DEFAULT_GOAL:= install

install:
	pip3 install --user $(CURDIR)

test:
	flake8 $(CURDIR)/y2p/y2p.py
	flake8 $(CURDIR)/setup.py
	flake8 $(CURDIR)/tests.py
	$(CURDIR)/tests.py
