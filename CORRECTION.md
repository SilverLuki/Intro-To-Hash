# Securinets ISI — Hashcat Workshop Corrections

This is the instructor correction guide. Do not give it to students.

## Task 1 — Hello, Hashcat
- Algorithm: MD5
- Hashcat mode: `0`
- Attack: dictionary / straight (`-a 0`)
- Wordlist: `rockyou.txt`
- Command:
  ```bash
  hashcat -m 0 -a 0 hash.txt rockyou.txt
  ```
- Main lesson: candidates are hashed and compared with the target; hashes are not decrypted.

## Task 2 — Choose Your Wordlist
- Algorithm: MD5
- Hashcat mode: `0`
- Attack: dictionary / straight
- Wordlist: `SecLists-passwords.txt`
- Command:
  ```bash
  hashcat -m 0 -a 0 hash.txt SecLists-passwords.txt
  ```
- Main lesson: wordlist choice is part of the attack strategy.

## Task 3 — New Algorithm
- Algorithm: SHA-1
- Hashcat mode: `100`
- Attack: dictionary / straight
- Wordlist: `rockyou.txt`
- Command:
  ```bash
  hashcat -m 100 -a 0 hash.txt rockyou.txt
  ```
- Main lesson: recognize the hash format and change the Hashcat mode.

## Task 4 — SHA-256
- Algorithm: SHA-256
- Hashcat mode: `1400`
- Attack: dictionary / straight
- Wordlist: `rockyou.txt`
- Command:
  ```bash
  hashcat -m 1400 -a 0 hash.txt rockyou.txt
  ```
- Main lesson: a longer digest is not the same thing as a password KDF.

## Task 5 — Humans Make Patterns
- Algorithm: MD5
- Hashcat mode: `0`
- Attack: dictionary + rules
- Wordlist: `rockyou.txt`
- Password construction: capitalized RockYou word + `1`
- Example command:
  ```bash
  hashcat -m 0 -a 0 hash.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule
  ```
- Main lesson: rules generate mutations of dictionary candidates.

## Task 6 — Mask the Search
- Algorithm: MD5
- Hashcat mode: `0`
- Attack: mask / brute force (`-a 3`)
- Password construction: exactly six digits
- Command:
  ```bash
  hashcat -m 0 -a 3 hash.txt '?d?d?d?d?d?d'
  ```
- Main lesson: use known structure to shrink the search space.

## Task 7 — Hybrid Thinking
- Algorithm: MD5
- Hashcat mode: `0`
- Attack: hybrid word + mask (`-a 6`)
- Password construction: RockYou word + exactly four digits
- Wordlist: `rockyou.txt`
- Command:
  ```bash
  hashcat -m 0 -a 6 hash.txt rockyou.txt '?d?d?d?d'
  ```
- Main lesson: combine a known word pattern with a mask instead of brute-forcing the whole password.

## Task 8 — The Salt Appears
- Algorithm: SHA-256(password + salt)
- Hashcat mode: `1410`
- Attack: salted dictionary
- Wordlist: `SecLists-passwords.txt`
- Target display: `hash` and `salt`; students should create a file containing `hash:salt`.
- Command:
  ```bash
  hashcat -m 1410 -a 0 hash_and_salt.txt SecLists-passwords.txt
  ```
- Main lesson: the salt is not a secret. The exact construction matters.

## Task 9 — The Wall Gets Higher
- Algorithm: Argon2id
- Hashcat mode: `3400`
- Password: deliberately high-entropy and randomly generated
- Salt: generated internally by Argon2id
- Command pattern:
  ```bash
  hashcat -m 3400 -a 0 hash.txt wordlist.txt
  ```
- Main lesson: modern password KDFs are deliberately expensive, and high-entropy passwords make guessing computationally impractical.
- Important: do **not** describe this as mathematically impossible or absolutely uncrackable. It is a demonstration of computational cost and entropy.

## Final workshop takeaway

1. Identify the hash construction.
2. Choose the correct Hashcat mode.
3. Look for information that reduces the candidate space.
4. Choose the right wordlist.
5. Choose dictionary, rules, mask, hybrid, or another appropriate attack.
6. Understand salts and the exact construction.
7. Remember that modern password KDFs plus strong passwords can make offline guessing impractical.
