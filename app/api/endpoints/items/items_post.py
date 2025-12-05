from datetime import datetime, timedelta
from typing import Annotated, List

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, select, ForeignKey, delete
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, backref

from app.api.utils.schedule_functions import generate_schedule
from app.api.models.models import User, Player, FootballTeam, TournamentType, Tournament, Match, \
    FootballTeamToTournament
from app.api.schemas.item import FootballTeamCreate, TournamentTypeCreate, TournamentCreate, \
    FootballTeamToTournamentCreate, MatchCreate, FootballTeamInfo, TournamentTypeInfo, TournamentInfo, \
    FootballTeamToTournamentInfo, MatchInfo

from app.database import get_db, get_current_active_user


router = APIRouter()


@router.post("/football_teams/", response_model=FootballTeamInfo, status_code=status.HTTP_201_CREATED, tags=["football teams endpoints"])
def create_football_team(football_team: FootballTeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_football_team = FootballTeam(**football_team.dict())
    db.add(db_football_team)
    db.commit()
    db.refresh(db_football_team)
    return db_football_team


@router.post("/tournament_types/", response_model=TournamentTypeInfo, status_code=status.HTTP_201_CREATED, tags=["tournament types endpoints"])
def create_tournament_type(tournament_type: TournamentTypeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_tournament_type = TournamentType(**tournament_type.dict())
    db.add(db_tournament_type)
    db.commit()
    db.refresh(db_tournament_type)
    return db_tournament_type


@router.post("/tournaments/", response_model=TournamentInfo, status_code=status.HTTP_201_CREATED, tags=["tournaments endpoints"])
def create_tournament(tournament: TournamentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_tournament = Tournament(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


@router.post("/football_teams_to_tournaments/", response_model=FootballTeamToTournamentInfo, status_code=status.HTTP_201_CREATED, tags=["football team to tournament endpoints"])
def add_football_team_to_tournament(football_team_to_tournament: FootballTeamToTournamentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_football_team_to_tournament = FootballTeamToTournament(**football_team_to_tournament.dict())
    db.add(db_football_team_to_tournament)
    db.commit()
    db.refresh(db_football_team_to_tournament)
    return db_football_team_to_tournament


# @router.post("/matches/", response_model=MatchInfo, status_code=status.HTTP_201_CREATED, tags=["matches endpoints"])
# def create_match(match: MatchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
#     db_match = Match(**match.dict())
#     db.add(db_match)
#     db.commit()
#     db.refresh(db_match)
#     return db_match


@router.post("/matches/schedule/{tournament_id}", response_model=List[MatchInfo], status_code=status.HTTP_201_CREATED, tags=["matches endpoints"])
def create_tournament_schedule(tournament_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_football_teams = db.execute(
        select(FootballTeamToTournament)
        .where(FootballTeamToTournament.tournament_id == tournament_id)
    ).scalars().all()

    if not db_football_teams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Schedule not found for this tournament or tournament is not exist")

    football_teams_list = [item.football_team_id for item in db_football_teams]
    schedule = generate_schedule(football_teams_list)

    db.execute(delete(Match).where(Match.tournament_id == tournament_id))
    matches = []

    for i in range(len(schedule)):
        for match in schedule[i]:
            db_match = Match(
                tournament_id=tournament_id,
                tour_number=i+1,
                home_team_id=match[0],
                guest_team_id=match[1]
            )
            db.add(db_match)
            matches.append(db_match)

    db.commit()
    return matches
