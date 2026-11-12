from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Role = Literal["Batter", "Bowler", "All-Rounder", "Wicketkeeper"]


class CricketPlayerBase(BaseModel):
    player_name: str = Field(min_length=1, max_length=100)
    team_name: str = Field(min_length=1, max_length=100)
    role: Role
    matches_played: int = Field(ge=0)
    total_runs: int = Field(ge=0)
    wickets_taken: int = Field(ge=0)
    balls_faced: int = Field(ge=0)
    catches: int = Field(ge=0)


class CricketPlayerCreate(CricketPlayerBase):
    player_id: int = Field(gt=0)


class CricketPlayerUpdate(BaseModel):
    matches_played: int | None = Field(default=None, ge=0)
    total_runs: int | None = Field(default=None, ge=0)
    wickets_taken: int | None = Field(default=None, ge=0)
    balls_faced: int | None = Field(default=None, ge=0)
    catches: int | None = Field(default=None, ge=0)


class CricketPlayerResponse(CricketPlayerBase):
    player_id: int
    model_config = ConfigDict(from_attributes=True)
