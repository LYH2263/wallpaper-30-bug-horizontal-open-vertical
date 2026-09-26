import json
from datetime import datetime, timezone

from app.db import connect


def insert_run(wall_id: int, roll_id: int, result: dict, note: str = "") -> int:
    conn = connect()
    try:
        cur = conn.execute(
            "INSERT INTO calc_runs(wall_id,roll_id,result_json,note,created_at) VALUES (?,?,?,?,?)",
            (wall_id, roll_id, json.dumps(result, ensure_ascii=False), note, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def list_runs(limit: int = 50):
    from app.services.horizontal_open import open_as_vertical

    conn = connect()
    try:
        rows = conn.execute(
            """
            SELECT r.*, w.name wall_name, rl.name roll_name,
                   w.perimeter wall_perimeter, w.height wall_height,
                   rl.width roll_width, rl.length roll_length, rl.pattern_cm roll_pattern_cm
            FROM calc_runs r
            LEFT JOIN walls w ON w.id=r.wall_id
            LEFT JOIN rolls rl ON rl.id=r.roll_id
            ORDER BY r.id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
        out = []
        for row in rows:
            d = dict(row)
            dims = {
                "perimeter": d.get("wall_perimeter"),
                "height": d.get("wall_height"),
                "roll_width": d.get("roll_width"),
                "roll_length": d.get("roll_length"),
                "pattern_cm": d.get("roll_pattern_cm"),
            }
            raw = json.loads(d.pop("result_json"))
            d["result"] = open_as_vertical(raw, dims)
            out.append(d)
        return out
    finally:
        conn.close()
