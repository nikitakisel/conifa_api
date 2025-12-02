from datetime import datetime, timedelta
from typing import Annotated, List

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, select, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, backref

from app.api.schemas.item import ScheduleTour
from app.api.schemas.user import UserResponse, UserCreate
from app.config import DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, engine, SessionLocal
from app.api.models.models import User, Player, FootballTeam, TournamentType, Tournament, Match, \
    FootballTeamToTournament
from app.api.schemas.item import FootballTeamCreate, TournamentTypeCreate, TournamentCreate, \
    FootballTeamToTournamentCreate, MatchCreate, FootballTeamInfo, TournamentTypeInfo, TournamentInfo, \
    FootballTeamToTournamentInfo, MatchInfo

from app.database import get_db, get_current_active_user
from app.api.services.item_service import get_formatted_schedule

router = APIRouter()


@router.get("/matches/schedule/{tournament_id}", response_model=List[ScheduleTour], tags=["matches panel"])
def generate_matches_schedule(tournament_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_football_teams = db.execute(
        select(FootballTeam)
        .join(FootballTeamToTournament, FootballTeamToTournament.football_team_id == FootballTeam.id)
        .where(FootballTeamToTournament.tournament_id == tournament_id)
    ).scalars().all()

    if not db_football_teams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found for this tournament or tournament is not exist")

    football_teams_list = [item.team_name for item in db_football_teams]
    schedule = get_formatted_schedule(football_teams_list)
    return schedule
