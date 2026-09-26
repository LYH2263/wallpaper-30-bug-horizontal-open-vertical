from app.db import connect


def get_all() -> dict:
    conn = connect()
    try:
        return {r["key"]: r["value"] for r in conn.execute("SELECT key,value FROM settings").fetchall()}
    finally:
        conn.close()


def set_all(values: dict) -> dict:
    conn = connect()
    try:
        conn.executemany(
            "INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            [(str(k), str(v)) for k, v in values.items()],
        )
        conn.commit()
    finally:
        conn.close()
    return get_all()
