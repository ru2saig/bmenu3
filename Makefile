PREFIX=/usr/local/bin

install:
	cp main.py $(PREFIX)/bmenu
	chmod 755 $(PREFIX)/bmenu
	cp genthumbs.py $(PREFIX)/genthumbs
	chmod 755 $(PREFIX)/genthumbs

uninstall:
	rm $(PREFIX)/bmenu
	rm $(PREFIX)/genthumbs
