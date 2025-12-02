from app.api.schemas.item import ScheduleMatch, ScheduleTour


def get_formatted_schedule(team_names):
    schedule = generate_schedule(team_names)
    formatted_schedule = []

    for i in range(len(schedule)):
        matches = [
            ScheduleMatch(
                home_team_name=item[0],
                guest_team_name=item[1]
            ) for item in schedule[i]
        ]

        formatted_schedule.append(
            ScheduleTour(
                tour_number=i+1,
                matches=matches
            )
        )

    return formatted_schedule


def generate_schedule(team_names):
    teams = list(team_names)
    n = len(teams)

    has_bye = False
    if n % 2 != 0:
        teams.append("BYE")
        n += 1
        has_bye = True

    schedule = []

    fixed_team = teams[0]
    rotating_teams = teams[1:]

    for _ in range(n - 1):
        current_round_matches = []

        match_fixed = (fixed_team, rotating_teams[-1])
        current_round_matches.append(match_fixed)

        for i in range((n - 2) // 2):
            match_pair = (rotating_teams[i], rotating_teams[n - 2 - 1 - i])
            current_round_matches.append(match_pair)

        filtered_round = []
        for home, away in current_round_matches:
            if home != "BYE" and away != "BYE":
                filtered_round.append((home, away))

        if filtered_round:
            schedule.append(filtered_round)

        last_rotating_team = rotating_teams.pop()
        rotating_teams.insert(0, last_rotating_team)

    final_schedule = []

    for round_idx in range(len(schedule)):
        home_round = schedule[round_idx]
        away_round = []
        for home_team, away_team in home_round:
            away_round.append((away_team, home_team))

        final_schedule.append(home_round)
        final_schedule.append(away_round)

    return final_schedule
