import sqlite3
import os
import hashlib
import secrets
import time

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cloudscale.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            avatar_color TEXT DEFAULT '#3b82f6',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

init_db()

AVATAR_COLORS = ['#3b82f6', '#22c55e', '#a855f7', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#14b8a6']

def _hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{h.hex()}"

def _verify_password(password, stored):
    salt, _ = stored.split(':')
    return _hash_password(password, salt) == stored

def signup(full_name, email, password):
    if not full_name or not email or not password:
        return None, "All fields are required."
    if len(password) < 6:
        return None, "Password must be at least 6 characters."
    if '@' not in email or '.' not in email:
        return None, "Please enter a valid email."

    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email.lower(),)).fetchone()
    if existing:
        conn.close()
        return None, "An account with this email already exists."

    pw_hash = _hash_password(password)
    color = secrets.choice(AVATAR_COLORS)
    cur = conn.execute(
        "INSERT INTO users (full_name, email, password_hash, avatar_color) VALUES (?, ?, ?, ?)",
        (full_name.strip(), email.lower().strip(), pw_hash, color)
    )
    conn.commit()
    user = conn.execute("SELECT id, full_name, email, avatar_color, created_at FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()
    conn.close()
    return dict(user), None

def login(email, password):
    if not email or not password:
        return None, "Email and password are required."

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),)).fetchone()
    conn.close()

    if not user:
        return None, "Invalid email or password."

    if not _verify_password(password, user['password_hash']):
        return None, "Invalid email or password."

    return {
        'id': user['id'],
        'full_name': user['full_name'],
        'email': user['email'],
        'avatar_color': user['avatar_color'],
        'created_at': user['created_at'],
    }, None
