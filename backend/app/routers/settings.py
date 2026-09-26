from fastapi import APIRouter, Body, HTTPException
from app.engines.wallpaper_math import ORIENTATIONS
from app.repositories import settings_repo

router = APIRouter()


@router.get("/settings")
def settings():
    return settings_repo.get_all()


@router.put("/settings")
def settings_update(values: dict = Body(...)):
    # 改系统默认贴向只影响之后未指定贴向的测算;已落库的 run 钉住写入时贴向,不回改。
    if "default_orientation" in values and values["default_orientation"] not in ORIENTATIONS:
        raise HTTPException(422, "invalid orientation")
    return settings_repo.set_all(values)
