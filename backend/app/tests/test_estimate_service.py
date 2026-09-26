import pytest
from fastapi import HTTPException

import app.db as db
from app import seed
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture()
def fresh_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    return tmp_path / "test.db"


def _add_clean_roll(name, width, length, pattern_cm=0):
    conn = db.connect()
    try:
        cur = conn.execute(
            "INSERT INTO rolls(name,width,length,pattern_cm,data_quality,note) VALUES (?,?,?,?, 'clean', '')",
            (name, width, length, pattern_cm),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def test_invalid_roll_size_rejected_and_no_row_added(fresh_db):
    bad_roll_id = _add_clean_roll("零宽-clean", 0.0, 10.0)
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(1, bad_roll_id, True, "", orientation="horizontal")
    assert exc.value.status_code == 422
    assert history.list_runs() == []


def test_saved_run_pins_orientation_and_rolls(fresh_db):
    out = estimate_service.run_estimate(1, 1, True, "", orientation="horizontal")
    assert out["run_id"]
    run = [r for r in history.list_runs() if r["id"] == out["run_id"]][0]
    assert run["result"]["orientation"] == "horizontal"
    assert run["result"]["rolls"] == 6

    # 只改系统默认贴向,不得改写旧 run
    settings_repo.set_all({"default_orientation": "vertical"})
    run_after = [r for r in history.list_runs() if r["id"] == out["run_id"]][0]
    assert run_after["result"]["orientation"] == "horizontal"
    assert run_after["result"]["rolls"] == 6


def test_default_orientation_comes_from_settings(fresh_db):
    settings_repo.set_all({"default_orientation": "horizontal"})
    out = estimate_service.run_estimate(1, 1, False, "")
    assert out["orientation"] == "horizontal"
    assert out["run_id"] is None
    assert history.list_runs() == []


def test_invalid_orientation_rejected(fresh_db):
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(1, 1, False, "", orientation="diagonal")
    assert exc.value.status_code == 422
