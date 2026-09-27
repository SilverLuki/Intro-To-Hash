import os
import hashlib
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-in-render")

# Instructor-only reveal key. Set INSTRUCTOR_KEY in Render.
INSTRUCTOR_KEY = os.environ.get("INSTRUCTOR_KEY", "change-me")

WORDLISTS = {
    "rockyou": "wordlists/rockyou.txt",
    "seclists": "wordlists/SecLists-passwords.txt",
}


def load_words(kind):
    path = WORDLISTS[kind]
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            words = [x.strip() for x in f if x.strip() and len(x.strip()) <= 64]
        if words:
            return words
    except FileNotFoundError:
        pass
    # Safe fallback so the app can be tested before the real wordlists are added.
    return ["password", "admin", "letmein", "qwerty", "Securinets", "Securinets2026"]


def pick(kind):
    return secrets.choice(load_words(kind))


def digest(algorithm, value):
    return hashlib.new(algorithm, value.encode()).hexdigest()


TASKS = [
    {
        "id": 1, "title": "Hello, Hashcat", "level": "01",
        "story": "Your first target is intentionally simple. Learn the basic Hashcat workflow.",
        "algo": "MD5", "mode": 0, "attack": "Dictionary / straight",
        "wordlist": "rockyou", "generator": lambda: pick("rockyou"),
        "salted": False,
        "hint": "Start with a dictionary attack. Your first goal is simply to make Hashcat compare candidates against an MD5 hash.",
        "new": "Basic Hashcat command: -m for hash type and -a 0 for a wordlist.",
        "check": lambda p, salt=None: digest("md5", p),
        "command": "hashcat -m 0 -a 0 hash.txt rockyou.txt",
    },
    {
        "id": 2, "title": "Choose Your Wordlist", "level": "02",
        "story": "The same attack can produce different results depending on the wordlist. This time, use a curated security password list.",
        "algo": "MD5", "mode": 0, "attack": "Dictionary / straight",
        "wordlist": "seclists", "generator": lambda: pick("seclists"),
        "salted": False,
        "hint": "Use the SecLists password list supplied for the workshop.",
        "new": "Wordlist selection is part of the attack strategy.",
        "check": lambda p, salt=None: digest("md5", p),
        "command": "hashcat -m 0 -a 0 hash.txt SecLists-passwords.txt",
    },
    {
        "id": 3, "title": "New Algorithm", "level": "03",
        "story": "Same cracking idea, different digest algorithm. Learn to recognize the format and change the Hashcat mode.",
        "algo": "SHA-1", "mode": 100, "attack": "Dictionary / straight",
        "wordlist": "rockyou", "generator": lambda: pick("rockyou"),
        "salted": False,
        "hint": "The hash is 40 hexadecimal characters. Do not assume every hexadecimal hash is MD5.",
        "new": "Recognizing SHA-1 and changing Hashcat mode.",
        "check": lambda p, salt=None: digest("sha1", p),
        "command": "hashcat -m 100 -a 0 hash.txt rockyou.txt",
    },
    {
        "id": 4, "title": "SHA-256", "level": "04",
        "story": "A longer digest does not automatically mean the password is stronger. Identify SHA-256 and crack it with a dictionary.",
        "algo": "SHA-256", "mode": 1400, "attack": "Dictionary / straight",
        "wordlist": "rockyou", "generator": lambda: pick("rockyou"),
        "salted": False,
        "hint": "SHA-256 produces 64 hexadecimal characters. Hashcat mode 1400 is the key clue.",
        "new": "Recognizing SHA-256.",
        "check": lambda p, salt=None: digest("sha256", p),
        "command": "hashcat -m 1400 -a 0 hash.txt rockyou.txt",
    },
    {
        "id": 5, "title": "Humans Make Patterns", "level": "05",
        "story": "The password is a familiar word with a predictable mutation. A plain dictionary attack may miss it.",
        "algo": "MD5", "mode": 0, "attack": "Dictionary + rules",
        "wordlist": "rockyou", "generator": lambda: pick("rockyou").capitalize() + "1",
        "salted": False,
        "hint": "Humans often capitalize words and append digits. Use a rule file to generate mutations from RockYou candidates.",
        "new": "Rule-based attacks with -r.",
        "check": lambda p, salt=None: digest("md5", p),
        "command": "hashcat -m 0 -a 0 hash.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule",
    },
    {
        "id": 6, "title": "Mask the Search", "level": "06",
        "story": "The challenge tells you the password is exactly six digits. Do not waste time searching letters.",
        "algo": "MD5", "mode": 0, "attack": "Mask / brute force",
        "wordlist": None, "generator": lambda: f"{secrets.randbelow(1000000):06d}",
        "salted": False,
        "hint": "The clue is the attack strategy: exactly six digits. Use ?d for each digit position.",
        "new": "Mask attacks (-a 3) exactly six digits. Use ?d for each digit position.",
        "check": lambda p, salt=None: digest("md5", p),
        "command": "hashcat -m 0 -a 3 hash.txt '?d?d?d?d?d?d'",
    },
    {
        "id": 7, "title": "Hybrid Thinking", "level": "07",
        "story": "You know the password starts with a word from RockYou and ends with four digits. Combine both ideas.",
        "algo": "MD5", "mode": 0, "attack": "Hybrid / word + mask",
        "wordlist": "rockyou", "generator": lambda: pick("rockyou") + f"{secrets.randbelow(10000):04d}",
        "salted": False,
        "hint": "Do not brute-force the whole password. Use a wordlist for the known word part and a mask for the four digits.",
        "new": "Hybrid attacks (-a 6) combine a dictionary with a mask. Use a wordlist for the known word part and a mask for the four digits.",
        "check": lambda p, salt=None: digest("md5", p),
        "command": "hashcat -m 0 -a 6 hash.txt rockyou.txt '?d?d?d?d'",
    },
    {
        "id": 8, "title": "The Salt Appears", "level": "08",
        "story": "The database stores a salt next to the hash. The salt is not secret, but it changes what you must compute.",
        "algo": "SHA-256(password + salt)", "mode": 1410, "attack": "Salted dictionary",
        "wordlist": "seclists", "generator": lambda: pick("seclists"),
        "salted": True,
        "salt": lambda: secrets.token_hex(4),
        "hint": "Use SecLists and Hashcat mode 1410. The target format is hash:salt because the construction is SHA-256($pass.$salt).",
        "new": "Salted hashes and why the exact hash construction matters.",
        "check": lambda p, salt=None: digest("sha256", p + salt),
        "command": "hashcat -m 1410 -a 0 hash_and_salt.txt SecLists-passwords.txt",
    },
    {
        "id": 9, "title": "The Wall Gets Higher", "level": "09",
        "story": "The server now uses Argon2id, a deliberately expensive password hashing function. The password is also high-entropy.",
        "algo": "Argon2id", "mode": 3400, "attack": "Password recovery / KDF",
        "wordlist": None, "generator": lambda: "ThisIsARealisticallyStrongPassword!2026#" + secrets.token_hex(8),
        "salted": True,
        "salt": "generated-by-argon2",
        "hint": "This is the final demonstration. The target is intentionally high-entropy and Argon2id is deliberately expensive. The lesson is computational impracticality, not mathematical impossibility.",
        "new": "Modern password hashing, unique salts, cost, and why password entropy changes the economics of guessing.",
        "check": None,
        "final": True,
        "command": "hashcat -m 3400 -a 0 hash.txt wordlist.txt",
    },
]


def task_for(tid):
    return next((t for t in TASKS if t["id"] == tid), None)


def get_instance(tid):
    key = f"task_{tid}"
    if key not in session:
        t = task_for(tid)
        password = t["generator"]()
        salt = t.get("salt")
        if callable(salt):
            salt = salt()

        if t.get("final"):
            from argon2 import PasswordHasher
            ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)
            h = ph.hash(password)
        elif t.get("salted"):
            h = t["check"](password, salt)
        else:
            h = t["check"](password)

        session[key] = {"password": password, "salt": salt, "hash": h}
    return session[key]


@app.route("/")
def index():
    solved = session.get("solved", [])
    return render_template("index.html", tasks=TASKS, solved=solved)


@app.route("/task/<int:tid>", methods=["GET", "POST"])
def task(tid):
    t = task_for(tid)
    if not t:
        abort(404)
    inst = get_instance(tid)
    message = None
    success = False

    if request.method == "POST":
        answer = request.form.get("answer", "").strip()
        if t.get("final"):
            from argon2 import PasswordHasher
            ph = PasswordHasher()
            try:
                ph.verify(inst["hash"], answer)
                success = True
            except Exception:
                success = False
        else:
            success = answer == inst["password"]

        message = "Correct! Great work." if success else "Not quite. Re-check the hash mode, attack strategy, and clues."
        if success:
            solved = set(session.get("solved", []))
            solved.add(tid)
            session["solved"] = sorted(solved)

    return render_template("task.html", task=t, instance=inst, message=message, success=success, tasks=TASKS)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


@app.route("/instructor")
def instructor():
    if request.args.get("key") != INSTRUCTOR_KEY:
        abort(403)
    rows = []
    for t in TASKS:
        inst = get_instance(t["id"])
        rows.append((t, inst))
    return render_template("instructor.html", rows=rows)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
