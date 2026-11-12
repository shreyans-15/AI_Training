from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from config.database import Base, engine, get_db
from config.logging_config import logger
from models.cricketplayer_model import CricketPlayer  # registers table with Base
from schema.cricketplayer_schema import (
    CricketPlayerCreate, CricketPlayerResponse, CricketPlayerUpdate,
)
from services import cricketplayer_service as service

app = FastAPI(title="Cricket Player Statistics API", version="1.0.0")


@app.on_event("startup")
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ready")
    except Exception:
        logger.exception("Database startup failed")
        raise


def required_player(db: Session, player_id: int):
    player = service.get_player(db, player_id)
    if player is None:
        logger.warning("Player not found: %s", player_id)
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def unexpected_error(db: Session, operation: str):
    db.rollback()
    logger.exception("Unexpected failure during %s", operation)
    raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
def home():
    return {"message": "Cricket Player Statistics API is running"}


# 1. Register a new cricket player
@app.post("/players/", response_model=CricketPlayerResponse, status_code=201)
def create_player(data: CricketPlayerCreate, db: Session = Depends(get_db)):
    try:
        player = service.create_player(db, data)
        logger.info("Created player ID %s", player.player_id)
        return player
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate player ID %s", data.player_id)
        raise HTTPException(status_code=409, detail="Player ID already exists")
    except SQLAlchemyError:
        unexpected_error(db, "player creation")


# 2. List players with pagination
@app.get("/players/", response_model=list[CricketPlayerResponse])
def list_players(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
        return service.list_players(db, skip, limit)
    except SQLAlchemyError:
        unexpected_error(db, "player listing")


# 6. Filter players by team
@app.get("/players/by-team/{team_name}", response_model=list[CricketPlayerResponse])
def players_by_team(team_name: str, db: Session = Depends(get_db)):
    try:
        return service.players_by_team(db, team_name)
    except SQLAlchemyError:
        unexpected_error(db, "team filtering")


# 7. All-rounders with at least 10 wickets
@app.get("/players/all-rounders/ten-wickets", response_model=list[CricketPlayerResponse])
def all_rounders(db: Session = Depends(get_db)):
    try:
        return service.all_rounders_with_ten_wickets(db)
    except SQLAlchemyError:
        unexpected_error(db, "all-rounder filtering")


# 8. Top five run scorers
@app.get("/players/top-five/run-scorers", response_model=list[CricketPlayerResponse])
def top_five(db: Session = Depends(get_db)):
    try:
        return service.top_five_run_scorers(db)
    except SQLAlchemyError:
        unexpected_error(db, "top five run scorers")


# 10. Total runs and wickets per team
@app.get("/players/stats/team-totals")
def team_totals(db: Session = Depends(get_db)):
    try:
        rows = service.team_totals(db)
        return [
            {"team_name": team, "total_runs": int(runs or 0), "total_wickets": int(wickets or 0)}
            for team, runs, wickets in rows
        ]
    except SQLAlchemyError:
        unexpected_error(db, "team totals")


# 3. Find a player by ID
@app.get("/players/{player_id}", response_model=CricketPlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    try:
        return required_player(db, player_id)
    except HTTPException:
        raise
    except SQLAlchemyError:
        unexpected_error(db, "player lookup")


# 4. Update player match statistics
@app.put("/players/{player_id}", response_model=CricketPlayerResponse)
def update_player(player_id: int, data: CricketPlayerUpdate, db: Session = Depends(get_db)):
    try:
        player = required_player(db, player_id)
        if not data.model_fields_set:
            logger.warning("Empty update for player ID %s", player_id)
            raise HTTPException(status_code=422, detail="Provide at least one statistic to update")
        updated = service.update_player(db, player, data)
        logger.info("Updated player ID %s", player_id)
        return updated
    except HTTPException:
        raise
    except SQLAlchemyError:
        unexpected_error(db, "player update")


# 5. Delete a player
@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    try:
        player = required_player(db, player_id)
        service.delete_player(db, player)
        logger.info("Deleted player ID %s", player_id)
        return {"message": "Player deleted successfully", "player_id": player_id}
    except HTTPException:
        raise
    except SQLAlchemyError:
        unexpected_error(db, "player deletion")


# 9. Calculate batting strike rate
@app.get("/players/{player_id}/strike-rate")
def strike_rate(player_id: int, db: Session = Depends(get_db)):
    try:
        player = required_player(db, player_id)
        if player.balls_faced == 0:
            logger.warning("Strike rate undefined: zero balls faced for player ID %s", player_id)
            return {"player_id": player_id, "strike_rate": None, "message": "Strike rate unavailable: balls faced is zero"}
        return {"player_id": player_id, "strike_rate": round(player.total_runs / player.balls_faced * 100, 2)}
    except HTTPException:
        raise
    except SQLAlchemyError:
        unexpected_error(db, "strike rate calculation")
