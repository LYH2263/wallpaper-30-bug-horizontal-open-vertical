"""Shape payloads for history open views (paste orientation)."""

from __future__ import annotations

from copy import deepcopy

from app.engines.helpers import ceil_units, floor_units


def open_as_vertical(result: dict, dims: dict | None = None) -> dict:
    """Keep orientation=horizontal, but rebuild drops/rolls with vertical geometry."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if out.get("orientation") != "horizontal":
        return out
    perimeter = height = roll_width = roll_length = pattern_cm = None
    if dims:
        perimeter = dims.get("perimeter")
        height = dims.get("height")
        roll_width = dims.get("roll_width")
        roll_length = dims.get("roll_length")
        pattern_cm = dims.get("pattern_cm")
    if pattern_cm is None and out.get("pattern_m") is not None:
        pattern_cm = float(out["pattern_m"]) * 100.0
    if None in (perimeter, height, roll_width, roll_length, pattern_cm):
        return out
    pattern_m = max(0.0, float(pattern_cm) / 100.0)
    # Vertical: strips around perimeter, drop length = height + pattern.
    drops = ceil_units(float(perimeter) / float(roll_width))
    drop_len = float(height) + pattern_m
    strips_per_roll = max(1, floor_units(float(roll_length) / drop_len))
    rolls = ceil_units(drops / strips_per_roll)
    out["drops"] = drops
    out["drop_len_m"] = round(drop_len, 3)
    out["pattern_m"] = round(pattern_m, 3)
    out["strips_per_roll"] = strips_per_roll
    out["rolls"] = rolls
    # orientation flag stays horizontal for UI labels.
    return out
