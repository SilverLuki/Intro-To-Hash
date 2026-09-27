Securinets ISI Hashcat Lab - Wordlists

Add exactly these two files to this directory before the workshop:

1. rockyou.txt
2. SecLists-passwords.txt

No custom wordlist is required.

The app only uses these files for the dictionary, rule, hybrid, and salted-dictionary tasks.
If a file is missing, the app uses a tiny fallback list so the website can still be tested. For the real workshop, add the full wordlists.

Kali commonly provides RockYou compressed as rockyou.txt.gz under /usr/share/wordlists/.
SecLists is normally installed separately or can be copied into this project and renamed to SecLists-passwords.txt.
