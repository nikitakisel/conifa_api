from datetime import datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, select, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, backref

from app.api.models.models import User, Player, FootballTeam, TournamentType, Tournament, Match, \
    FootballTeamToTournament

from app.database import get_db, get_current_active_user


router = APIRouter()


@router.delete("/football_team/{team_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["football teams endpoints"])
def remove_football_team(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Removes a football team.
    """
    football_team = db.execute(
        select(FootballTeam).where(FootballTeam.id == team_id)
    ).scalars().first()

    if football_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such football team is not exist")

    db.delete(football_team)
    db.commit()
    return


@router.delete("/tournament/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tournaments endpoints"])
def remove_tournament(
    tournament_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Removes a tournament.
    """
    tournament = db.execute(
        select(Tournament).where(Tournament.id == tournament_id)
    ).scalars().first()

    if tournament is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such tournament does not exist")

    db.delete(tournament)
    db.commit()
    return


@router.delete("/tournament_type/{tournament_type_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tournament types endpoints"])
def remove_tournament_type(
    tournament_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Removes a tournament type.
    """
    tournament_type = db.execute(
        select(TournamentType).where(TournamentType.id == tournament_type_id)
    ).scalars().first()

    if tournament_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such tournament type does not exist")

    db.delete(tournament_type)
    db.commit()
    return


@router.delete("/match/{match_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["matches endpoints"])
def remove_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Removes a match.
    """
    match = db.execute(
        select(Match).where(Match.id == match_id)
    ).scalars().first()

    if match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such match does not exist")

    db.delete(match)
    db.commit()
    return


@router.delete("/football_team_to_tournament/{mapping_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["football team to tournament endpoints"])
def remove_football_team_to_tournament(
    mapping_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Removes a football team to tournament mapping.
    """
    mapping = db.execute(
        select(FootballTeamToTournament).where(FootballTeamToTournament.id == mapping_id)
    ).scalars().first()

    if mapping is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such football team to tournament mapping does not exist")

    db.delete(mapping)
    db.commit()
    return
