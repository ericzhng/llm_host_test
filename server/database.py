import sqlite3
from contextlib import contextmanager
import os
import stat

DB_PATH = "api_keys.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                api_key TEXT PRIMARY KEY,
                user_id TEXT NOT NULL UNIQUE
            )
        """)
        conn.commit()
    # Secure file permissions (owner read/write only)
    os.chmod(DB_PATH, stat.S_IRUSR | stat.S_IWUSR)  # 600

def insert_api_key(api_key: str, user_id: str):
    with get_db() as conn:
        conn.execute("INSERT INTO api_keys (api_key, user_id) VALUES (?, ?)", (api_key, user_id))
        conn.commit()

def get_user_id_by_key(api_key: str) -> str | None:
    with get_db() as conn:
        result = conn.execute("SELECT user_id FROM api_keys WHERE api_key = ?", (api_key,)).fetchone()
        return result["user_id"] if result else None

def user_id_exists(user_id: str) -> bool:
    with get_db() as conn:
        result = conn.execute("SELECT 1 FROM api_keys WHERE user_id = ?", (user_id,)).fetchone()
        return bool(result)

def delete_api_key(api_key: str):
    with get_db() as conn:
        conn.execute("DELETE FROM api_keys WHERE api_key = ?", (api_key,))
        conn.commit()
