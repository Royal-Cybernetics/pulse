CC = gcc
CFLAGS = -Wall
PREFIX = /usr/local
BINDIR = $(PREFIX)/bin

pulse: pulse.c
	$(CC) $(CFLAGS) -o pulse pulse.c

clean:
	rm -f pulse

install: pulse
	install -d $(BINDIR)
	install -m 755 pulse $(BINDIR)/pulse
	install -m 755 collector.py $(BINDIR)/pulse-collector
	install -m 755 api.py $(BINDIR)/pulse-api

uninstall:
	rm -f $(BINDIR)/pulse $(BINDIR)/pulse-collector $(BINDIR)/pulse-api

.PHONY: clean install uninstall