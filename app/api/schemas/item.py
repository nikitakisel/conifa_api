from datetime import datetime, timedelta
from decimal import Decimal
from typing import Annotated, List, Dict
from pydantic import BaseModel, Field, validator, field_validator


# Create models
class FootballTeamCreate(BaseModel):
    player_id: int
    team_name: str = Field(..., min_length=2)
    team_code: str = Field(..., min_length=2, max_length=4)
    team_logo: str
    country: str
    city: str
    achievements: str


class TournamentCreate(BaseModel):
    player_id: int
    tournament_name: str
    tournament_type_id: int
    season: str
    region: str


class TournamentTypeCreate(BaseModel):
    tournament_type_name: str
    description: str


class FootballTeamToTournamentCreate(BaseModel):
    football_team_id: int
    tournament_id: int


class MatchCreate(BaseModel):
    tournament_id: int
    tour_number: int
    date: datetime
    home_team_id: int
    guest_team_id: int
    home_team_score: int | None = None
    guest_team_score: int | None = None


# Info models
class FootballTeamInfo(BaseModel):
    id: int
    player_id: int
    team_name: str
    team_code: str
    team_logo: str
    country: str
    city: str
    achievements: str


class TournamentInfo(BaseModel):
    id: int
    player_id: int
    tournament_name: str
    tournament_type_id: int
    season: str
    region: str


class TournamentTypeInfo(BaseModel):
    id: int
    tournament_type_name: str
    description: str


class FootballTeamToTournamentInfo(BaseModel):
    id: int
    football_team_id: int
    tournament_id: int


class MatchInfo(BaseModel):
    id: int
    tournament_id: int
    tour_number: int
    date: datetime
    home_team_id: int
    guest_team_id: int
    home_team_score: int | None = None
    guest_team_score: int | None = None


# Full info models
class TournamentFullInfo(BaseModel):
    id: int
    player_id: int
    tournament_name: str
    tournament_type: str
    season: str
    region: str


class MatchFullInfo(BaseModel):
    id: int
    tournament_id: int
    tour_number: int
    date: datetime
    home_team_info: FootballTeamInfo
    guest_team_info: FootballTeamInfo
    home_team_score: int | None = None
    guest_team_score: int | None = None


class FootballTeamTournamentStatistics(BaseModel):
    team_name: str
    team_logo: str | None = None
    matches_played: int
    score: int
    wins: int
    draws: int
    losses: int
    goals_scored: int
    goals_conceded: int
    goal_difference: int


# Update models
class FootballTeamUpdate(BaseModel):
    team_name: str | None = None
    team_code: str | None = None
    team_logo: str | None = None
    country: str | None = None
    city: str | None = None
    achievements: str | None = None


class TournamentUpdate(BaseModel):
    tournament_name: str | None = None
    tournament_type_id: int | None = None
    season: str | None = None
    region: str | None = None


class TournamentTypeUpdate(BaseModel):
    tournament_type_name: str | None = None
    description: str | None = None


class MatchUpdate(BaseModel):
    date: datetime | None = None
    home_team_score: int | None = None
    guest_team_score: int | None = None
