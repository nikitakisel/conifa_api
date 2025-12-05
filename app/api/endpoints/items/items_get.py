from datetime import datetime, timedelta
from typing import Annotated, List

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, select, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, backref

from app.api.repositories.tournament_queries import TOURNAMENT_STANDINGS_SQL
from app.api.schemas.user import UserResponse, UserCreate
from app.config import DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, engine, SessionLocal
from app.api.models.models import User, Player, FootballTeam, TournamentType, Tournament, Match, \
    FootballTeamToTournament
from app.api.schemas.item import FootballTeamCreate, TournamentTypeCreate, TournamentCreate, \
    FootballTeamToTournamentCreate, MatchCreate, FootballTeamInfo, TournamentTypeInfo, TournamentInfo, \
    FootballTeamToTournamentInfo, MatchInfo, FootballTeamTournamentStatistics, MatchFullInfo, TournamentFullInfo

from app.database import get_db, get_current_active_user

router = APIRouter()


def parse_full_matches_info(db_matches, db):
    matches = []
    for match in db_matches:
        home_team_info = db.execute(
            select(FootballTeam)
            .where(FootballTeam.id == match.home_team_id)
        ).scalars().first()
        guest_team_info = db.execute(
            select(FootballTeam)
            .where(FootballTeam.id == match.guest_team_id)
        ).scalars().first()
        matches.append(
            MatchFullInfo(
                id=match.id,
                tournament_id=match.tournament_id,
                tour_number=match.tour_number,
                date=match.date,
                home_team_info=FootballTeamInfo(
                    id=home_team_info.id,
                    player_id=home_team_info.player_id,
                    team_name=home_team_info.team_name,
                    team_code=home_team_info.team_code,
                    team_logo=home_team_info.team_logo,
                    country=home_team_info.country,
                    city=home_team_info.city,
                    achievements=home_team_info.achievements
                ),
                guest_team_info=FootballTeamInfo(
                    id=guest_team_info.id,
                    player_id=guest_team_info.player_id,
                    team_name=guest_team_info.team_name,
                    team_code=guest_team_info.team_code,
                    team_logo=guest_team_info.team_logo,
                    country=guest_team_info.country,
                    city=guest_team_info.city,
                    achievements=guest_team_info.achievements
                ),
                home_team_score=match.home_team_score,
                guest_team_score=match.guest_team_score
            )
        )

    return matches


@router.get("/tournament/schedule/all/{tournament_id}", response_model=List[MatchFullInfo], tags=["matches endpoints"])
def get_tournament_schedule(tournament_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_matches = db.execute(
        select(Match)
        .where(Match.tournament_id == tournament_id)
    ).scalars().all()

    return parse_full_matches_info(db_matches, db)


@router.get("/tournament/schedule/tour/{tournament_id}/{tour_number}", response_model=List[MatchFullInfo], tags=["matches endpoints"])
def get_tournament_schedule(tournament_id: int, tour_number: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_matches = db.execute(
        select(Match)
        .where(Match.tournament_id == tournament_id, Match.tour_number == tour_number)
    ).scalars().all()

    return parse_full_matches_info(db_matches, db)


@router.get("/tournament/statistics/{tournament_id}", response_model=List[FootballTeamTournamentStatistics], tags=["matches endpoints"])
def get_tournament_statistics(tournament_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    teams_results = db.execute(text(TOURNAMENT_STANDINGS_SQL(tournament_id))).fetchall()
    return teams_results


@router.get("/football_teams/all", response_model=List[FootballTeamInfo], tags=["football teams endpoints"])
def read_all_football_teams(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    football_teams = db.execute(select(FootballTeam)).scalars().all()
    return football_teams


@router.get("/football_teams/{football_team_id}", response_model=FootballTeamInfo, tags=["football teams endpoints"])
def read_football_team(football_team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    football_team = db.execute(select(FootballTeam).where(FootballTeam.id == football_team_id)).scalars().first()

    if football_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such football team not found")

    return football_team


def parse_tournament_full_info(tournament):
    return TournamentFullInfo(
        id=tournament.id,
        player_id=tournament.player_id,
        tournament_name=tournament.tournament_name,
        tournament_type=tournament.tournament_type.tournament_type_name,
        season=tournament.season,
        region=tournament.region
    )


@router.get("/tournaments/all", response_model=List[TournamentFullInfo], tags=["tournaments endpoints"])
def read_all_tournaments(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    tournaments = db.execute(select(Tournament)).scalars().all()
    tournaments_info = [
        parse_tournament_full_info(tournament)
        for tournament in tournaments
    ]
    return tournaments_info


@router.get("/tournaments/{tournament_id}", response_model=TournamentFullInfo, tags=["tournaments endpoints"])
def read_tournament(tournament_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    tournament = db.execute(select(Tournament).where(Tournament.id == tournament_id)).scalars().first()

    if tournament is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such tournament not found")

    return parse_tournament_full_info(tournament)


@router.get("/tournament_types/all", response_model=List[TournamentTypeInfo], tags=["tournament types endpoints"])
def read_all_tournament_types(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    tournament_types = db.execute(select(TournamentType)).scalars().all()
    return tournament_types


@router.get("/tournament_types/{type_id}", response_model=TournamentTypeInfo, tags=["tournament types endpoints"])
def read_tournament_type(type_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    tournament_type = db.execute(select(TournamentType).where(TournamentType.id == type_id)).scalars().first()

    if tournament_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Such tournament not found")

    return tournament_type


@router.get("/football_teams_to_tournaments/football_teams/{tournament_id}", response_model=List[FootballTeamInfo], tags=["football team to tournament endpoints"])
def read_football_teams_by_tournament_id(tournament_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    football_teams_to_tournaments = db.execute(
        select(FootballTeamToTournament)
        .where(FootballTeamToTournament.tournament_id == tournament_id)
    ).scalars().all()

    football_teams = [
        football_team_to_tournament.football_team for football_team_to_tournament in football_teams_to_tournaments
    ]
    return football_teams


@router.get("/football_teams_to_tournaments/tournaments/{team_id}", response_model=List[TournamentFullInfo], tags=["football team to tournament endpoints"])
def read_tournaments_by_football_team_id(team_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    football_teams_to_tournaments = db.execute(
        select(FootballTeamToTournament)
        .where(FootballTeamToTournament.football_team_id == team_id)
    ).scalars().all()

    tournaments = [
        parse_tournament_full_info(football_team_to_tournament.tournament)
        for football_team_to_tournament in football_teams_to_tournaments
    ]
    return tournaments
