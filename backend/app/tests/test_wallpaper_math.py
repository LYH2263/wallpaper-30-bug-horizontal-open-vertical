import pytest

from app.engines.wallpaper_math import roll_count


def test_plain_master_bed():
    r = roll_count(16.0, 2.7, 0.53, 10.0, 0)
    assert r["orientation"] == "vertical"
    assert r["drops"] == 31
    assert r["drop_len_m"] == 2.7
    assert r["strips_per_roll"] == 3
    assert r["rolls"] == 11


def test_pattern_wall():
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64)
    assert r["drops"] == 38
    assert r["drop_len_m"] == 3.44
    assert r["strips_per_roll"] == 2
    assert r["rolls"] == 19


def test_horizontal_plain():
    # 横贴: 层高÷幅宽得条数, 周长加花高得条长
    r = roll_count(16.0, 2.7, 0.53, 10.0, 0, orientation="horizontal")
    assert r["orientation"] == "horizontal"
    assert r["drops"] == 6
    assert r["drop_len_m"] == 16.0
    assert r["strips_per_roll"] == 1
    assert r["rolls"] == 6


def test_horizontal_pattern():
    r = roll_count(20.0, 2.8, 0.53, 10.0, 64, orientation="horizontal")
    assert r["drops"] == 6
    assert r["drop_len_m"] == 20.64
    assert r["strips_per_roll"] == 1
    assert r["rolls"] == 6


def test_invalid_roll_size_rejected_both_orientations():
    with pytest.raises(ValueError):
        roll_count(16.0, 2.7, 0.0, 10.0, 0)
    with pytest.raises(ValueError):
        roll_count(16.0, 2.7, 0.53, 0.0, 0, orientation="horizontal")


def test_invalid_orientation_rejected():
    with pytest.raises(ValueError):
        roll_count(16.0, 2.7, 0.53, 10.0, 0, orientation="diagonal")
