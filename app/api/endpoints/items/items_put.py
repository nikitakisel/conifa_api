from datetime import datetime, timedelta
from typing import Annotated, List

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, select, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, backref

from app.api.models.models import User, Player, FootballTeam, TournamentType, Tournament, Match, \
    FootballTeamToTournament
from app.api.schemas.item import FootballTeamCreate, TournamentTypeCreate, TournamentCreate, \
    FootballTeamToTournamentCreate, MatchCreate, FootballTeamInfo, TournamentTypeInfo, TournamentInfo, \
    FootballTeamToTournamentInfo, MatchInfo, MatchUpdate, FootballTeamUpdate, TournamentUpdate, TournamentTypeUpdate

from app.database import get_db, get_current_active_user


router = APIRouter()


@router.put("/matches/{match_id}", response_model=MatchInfo, tags=["matches endpoints"])
def update_match_info(
    match_id: int,
    match_update: MatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Updates a match's information.
    """
    db_match = db.execute(select(Match).where(Match.id == match_id)).scalars().first()
    if db_match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current match not found")

    # Update fields if they are provided in the request
    if match_update.date is not None:
        db_match.date = match_update.date
    if match_update.home_team_score is not None:
        db_match.home_team_score = match_update.home_team_score
    if match_update.guest_team_score is not None:
        db_match.guest_team_score = match_update.guest_team_score

    db.commit()
    db.refresh(db_match)
    return db_match


@router.put("/football_team/{team_id}", response_model=FootballTeamInfo, tags=["football teams endpoints"])
def update_football_team_info(
    team_id: int,
    football_team_update: FootballTeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Updates a football team's information.
    """
    db_football_team = db.execute(select(FootballTeam).where(FootballTeam.id == team_id)).scalars().first()
    if db_football_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current football team not found")

    # Update fields if they are provided in the request
    if football_team_update.team_name is not None:
        db_football_team.team_name = football_team_update.team_name
    if football_team_update.team_code is not None:
        db_football_team.team_code = football_team_update.team_code
    if football_team_update.team_logo is not None:
        db_football_team.team_logo = football_team_update.team_logo
    if football_team_update.country is not None:
        db_football_team.country = football_team_update.country
    if football_team_update.city is not None:
        db_football_team.city = football_team_update.city
    if football_team_update.achievements is not None:
        db_football_team.achievements = football_team_update.achievements

    db.commit()
    db.refresh(db_football_team)
    return db_football_team


@router.put("/tournaments/{tournament_id}", response_model=TournamentInfo, tags=["tournaments endpoints"])
def update_tournament_info(
    tournament_id: int,
    tournament_update: TournamentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Updates a tournament's information.
    """
    db_tournament = db.execute(select(Tournament).where(Tournament.id == tournament_id)).scalars().first()
    if db_tournament is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current tournament not found")

    # Update fields if they are provided in the request
    if tournament_update.tournament_name is not None:
        db_tournament.tournament_name = tournament_update.tournament_name
    if tournament_update.tournament_type_id is not None:
        db_tournament.tournament_type_id = tournament_update.tournament_type_id
    if tournament_update.season is not None:
        db_tournament.season = tournament_update.season
    if tournament_update.region is not None:
        db_tournament.region = tournament_update.region

    db.commit()
    db.refresh(db_tournament)
    return db_tournament


@router.put("/tournament_types/{tournament_type_id}", response_model=TournamentTypeInfo, tags=["tournament types endpoints"])
def update_tournament_type_info(
    tournament_type_id: int,
    tournament_type_update: TournamentTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Updates a tournament type's information.
    """
    db_tournament_type = db.execute(select(TournamentType).where(TournamentType.id == tournament_type_id)).scalars().first()
    if db_tournament_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current tournament type not found")

    # Update fields if they are provided in the request
    if tournament_type_update.tournament_type_name is not None:
        db_tournament_type.tournament_type_name = tournament_type_update.tournament_type_name
    if tournament_type_update.description is not None:
        db_tournament_type.description = tournament_type_update.description

    db.commit()
    db.refresh(db_tournament_type)
    return db_tournament_type
