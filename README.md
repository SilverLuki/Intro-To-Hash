# Securinets ISI — Hashcat CTF Lab

A beginner-friendly, Render-ready web lab for a Securinets ISI Hashcat workshop.

## 9-task progression

1. MD5 + RockYou — basic dictionary attack
2. MD5 + SecLists — wordlist selection
3. SHA-1 + RockYou — new hash algorithm
4. SHA-256 + RockYou — new hash algorithm
5. MD5 + RockYou + rules — password mutations
6. MD5 + mask — six-digit search
7. MD5 + RockYou + hybrid — word + four digits
8. Salted SHA-256 + SecLists — salts and exact constructions
9. Argon2id — computationally impractical final demonstration

There is **no custom wordlist** and no double-MD5 task.

## Important architecture

The Flask website generates the target hashes and checks submissions. **Hashcat itself runs on the student's local machine** (for example Kali Linux). Render is only hosting the training website; it is not expected to provide a GPU for cracking.

Each browser session gets its own randomly selected password for applicable tasks. The selected password comes from the wordlist assigned to that task, so students can receive different targets.

## Add the wordlists

Put these two files in `wordlists/`:

```text
wordlists/
├── rockyou.txt
└── SecLists-passwords.txt
```

No custom wordlist is needed.

For the real workshop, use the full versions of the wordlists. The app has a tiny fallback list only so the website can be tested before the files are added.

## Run locally

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\\Scripts\\activate
```

Kali/Linux:
```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Render deployment

The repository already contains:

- `render.yaml`
- `Procfile`
- `requirements.txt`
- Flask application

Set these environment variables/secrets in Render:

- `SECRET_KEY` — a long random value
- `INSTRUCTOR_KEY` — a private key for the instructor correction page

The Render start command is:

```text
 gunicorn app:app
```

The included `render.yaml` configures this automatically.

## Instructor page

After deployment, open:

```text
/instructor?key=YOUR_INSTRUCTOR_KEY
```

This reveals the generated target values for the current browser session. Keep the instructor key private.

## Student workflow

Students should:

1. Open a task.
2. Copy the target hash.
3. Identify the algorithm/mode from the task clues.
4. Create the required hash input file locally.
5. Run Hashcat on Kali or another authorized machine.
6. Submit the recovered password to the website.

For Task 8, the target is SHA-256(password + salt), Hashcat mode `1410`. Students should put the target into `hash:salt` format before running Hashcat.

## Workshop safety

Use this lab only with the provided challenge data and systems you are authorized to test. The lab is designed for CTF/workshop training.
