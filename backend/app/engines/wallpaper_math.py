"""Wallpaper rolls: strips by paste orientation, pattern repeat on drop length, strips per roll."""

from app.engines.helpers import ceil_units, floor_units

VERTICAL = "vertical"
HORIZONTAL = "horizontal"
ORIENTATIONS = (VERTICAL, HORIZONTAL)


def roll_count(
    perimeter: float,
    height: float,
    roll_width: float,
    roll_length: float,
    pattern_cm: float,
    orientation: str = VERTICAL,
) -> dict:
    if orientation not in ORIENTATIONS:
        raise ValueError("invalid orientation")
    if roll_width <= 0 or roll_length <= 0:
        raise ValueError("invalid roll size")
    pattern_m = max(0.0, float(pattern_cm) / 100.0)
    if orientation == HORIZONTAL:
        # 横贴: strips run along the perimeter, stacked to cover the height.
        drops = ceil_units(float(height) / float(roll_width))
        drop_len = float(perimeter) + pattern_m
    else:
        # 竖贴: strips run floor-to-ceiling around the perimeter.
        drops = ceil_units(float(perimeter) / float(roll_width))
        drop_len = float(height) + pattern_m
    if drop_len <= 0:
        raise ValueError("invalid drop length")
    strips_per_roll = max(1, floor_units(float(roll_length) / drop_len))
    rolls = ceil_units(drops / strips_per_roll)
    return {
        "orientation": orientation,
        "drops": drops,
        "drop_len_m": round(drop_len, 3),
        "pattern_m": round(pattern_m, 3),
        "strips_per_roll": strips_per_roll,
        "rolls": rolls,
    }
