from sqlalchemy import func
from sqlalchemy.orm import Session
from models.cricketplayer_model import CricketPlayer
from schema.cricketplayer_schema import CricketPlayerCreate, CricketPlayerUpdate


def create_player(db: Session, data: CricketPlayerCreate):
    player = CricketPlayer(**data.model_dump())
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def list_players(db: Session, skip: int = 0, limit: int = 10):
    return db.query(CricketPlayer).order_by(CricketPlayer.player_id).offset(skip).limit(limit).all()


def get_player(db: Session, player_id: int):
    return db.query(CricketPlayer).filter(CricketPlayer.player_id == player_id).first()


def update_player(db: Session, player: CricketPlayer, data: CricketPlayerUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(player, field, value)
    db.commit()
    db.refresh(player)
    return player


def delete_player(db: Session, player: CricketPlayer):
    db.delete(player)
    db.commit()


def players_by_team(db: Session, team: str):
    return db.query(CricketPlayer).filter(CricketPlayer.team_name == team).all()


def all_rounders_with_ten_wickets(db: Session):
    return db.query(CricketPlayer).filter(
        CricketPlayer.role == "All-Rounder", CricketPlayer.wickets_taken >= 10
    ).all()


def top_five_run_scorers(db: Session):
    return db.query(CricketPlayer).order_by(
        CricketPlayer.total_runs.desc(), CricketPlayer.player_id.asc()
    ).limit(5).all()


def team_totals(db: Session):
    return db.query(
        CricketPlayer.team_name,
        func.sum(CricketPlayer.total_runs).label("total_runs"),
        func.sum(CricketPlayer.wickets_taken).label("total_wickets"),
    ).group_by(CricketPlayer.team_name).order_by(CricketPlayer.team_name).all()
