# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: config.py
@time: 2024/6/1 下午9:13
@author SuperLazyDog
"""
from pydantic import BaseModel, Field
import yaml
import os
from enum import Enum
from datetime import datetime


class Config(BaseModel):
    MaxFightTime: int = Field(120, title="最大战斗时间")
    MaxIdleTime: int = Field(10, title="最大空闲时间", ge=5)
    TargetBoss: list[str] = Field([], title="目标关键字")
    SelectRoleInterval: int = Field(2, title="选择角色间隔时间", ge=2)
    FightTactics: list[str] = Field(
        [
            "e,q,r,a,0.1,a,0.1,a,0.1,a,0.1,a,0.1",
            "e,q,r,a~0.5,0.1,a,0.1,a,0.1,a,0.1,a,0.1",
            "e~0.5,q,r,a,0.1,a,0.1,a,0.1,a,0.1,a,0.1",
        ],
        title="战斗策略, 逗号分隔, e,q,r为技能, a为普攻, 数字为间隔时间,a~0.5为普工按下0.5秒",
    )


# 判断是否存在配置文件
if os.path.exists("config.yaml"):
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = Config(**yaml.safe_load(f))
else:
    config = Config()
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(config.dict(), f)

if len(config.TargetBoss) == 0:
    print("请在config.yaml中填写目标BOSS全名")
    exit(1)


class Status(Enum):
    idle = "空闲"
    fight = "战斗"


class Role(BaseModel):
    index: int = Field(0, title="角色索引")
    bossIndex: int = Field(0, title="boss索引")
    status: Status = Field(Status.idle, title="状态")
    fightTime: datetime = Field(datetime.now(), title="战斗开始时间")
    lastFightTime: datetime = Field(datetime.now(), title="最近检测到战斗时间")
    idleTime: datetime = Field(datetime.now(), title="空闲时间")
    startTime: datetime = Field(datetime.now(), title="开始时间")


role = Role()
