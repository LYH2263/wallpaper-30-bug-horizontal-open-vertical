from typing import Optional

from fastapi import HTTPException

from app.engines.wallpaper_math import ORIENTATIONS, roll_count
from app.repositories import history, rolls, settings_repo, walls


def run_estimate(wall_id: int, roll_id: int, save: bool, note: str, orientation: Optional[str] = None):
    wall = walls.get_wall(wall_id)
    if not wall:
        raise HTTPException(404, "wall not found")
    roll = rolls.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    if wall.get("data_quality") == "dirty" or roll.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty seed entity")

    if orientation is None:
        orientation = settings_repo.get_all().get("default_orientation", "vertical")
    if orientation not in ORIENTATIONS:
        raise HTTPException(422, "invalid orientation")

    try:
        calc = roll_count(
            wall["perimeter"],
            wall["height"],
            roll["width"],
            roll["length"],
            roll["pattern_cm"],
            orientation=orientation,
        )
    except ValueError as exc:
        # 幅宽/卷长非正等非法输入:拒绝试算,且不落库、不增行。
        raise HTTPException(422, str(exc))
    run_id = None
    if save:
        # 落库钉住当次贴向与卷数,之后改系统默认贴向不影响该 run。
        run_id = history.insert_run(wall_id, roll_id, {**calc, "wall_id": wall_id, "roll_id": roll_id}, note)
    return {"wall": wall, "roll": roll, "run_id": run_id, **calc}
