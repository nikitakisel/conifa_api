from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    player = relationship("Player", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    surname = Column(String)
    name = Column(String)
    birthdate = Column(DateTime)
    enter_date = Column(DateTime, default=datetime.utcnow)
    email = Column(String)
    phone = Column(String)

    user = relationship("User", back_populates="player")
    football_teams = relationship("FootballTeam", back_populates="player", cascade="all, delete-orphan")
    tournaments = relationship("Tournament", back_populates="player", cascade="all, delete-orphan")
    # matches = relationship("Match", back_populates="player", cascade="all, delete-orphan")


class FootballTeam(Base):
    __tablename__ = "football_teams"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), index=True)
    team_name = Column(String)
    team_code = Column(String)
    team_logo = Column(Text)
    country = Column(String)
    city = Column(String)
    achievements = Column(Text)

    player = relationship(
        "Player",
        back_populates="football_teams"
    )
    home_matches = relationship(
        "Match",
        foreign_keys="[Match.home_team_id]",
        back_populates="home_team",
        cascade="all, delete"
    )
    guest_matches = relationship(
        "Match",
        foreign_keys="[Match.guest_team_id]",
        back_populates="guest_team",
        cascade="all, delete"
    )
    tournaments = relationship(
        "FootballTeamToTournament",
        back_populates="football_team"
    )


class TournamentType(Base):
    __tablename__ = "tournament_types"

    id = Column(Integer, primary_key=True, index=True)
    tournament_type_name = Column(String)
    description = Column(String)

    tournaments = relationship(
        "Tournament",
        back_populates="tournament_type",
        cascade="all, delete"
    )


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), index=True)
    tournament_type_id = Column(Integer, ForeignKey("tournament_types.id", ondelete="CASCADE"), index=True)
    tournament_name = Column(String)
    season = Column(String)
    region = Column(String)

    player = relationship("Player", back_populates="tournaments")
    tournament_type = relationship("TournamentType", back_populates="tournaments")
    matches = relationship("Match", back_populates="tournament", cascade="all, delete")
    football_teams = relationship("FootballTeamToTournament", back_populates="tournament")


class FootballTeamToTournament(Base):
    __tablename__ = "football_teams_to_tournaments"
    id = Column(Integer, primary_key=True, index=True)
    football_team_id = Column(Integer, ForeignKey("football_teams.id", ondelete="CASCADE"), index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), index=True)

    football_team = relationship("FootballTeam", back_populates="tournaments")
    tournament = relationship("Tournament", back_populates="football_teams")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    # player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"), index=True)
    tour_number = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    home_team_id = Column(Integer, ForeignKey("football_teams.id", ondelete="CASCADE"), index=True)
    guest_team_id = Column(Integer, ForeignKey("football_teams.id", ondelete="CASCADE"), index=True)
    home_team_score = Column(Integer)
    guest_team_score = Column(Integer)

    # player = relationship("Player", back_populates="matches")
    tournament = relationship("Tournament", back_populates="matches")

    home_team = relationship(
        "FootballTeam",
        foreign_keys=[home_team_id],
        back_populates="home_matches"
    )
    guest_team = relationship(
        "FootballTeam",
        foreign_keys=[guest_team_id],
        back_populates="guest_matches"
    )
