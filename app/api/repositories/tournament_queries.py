def TOURNAMENT_STANDINGS_SQL(tournament_id):
    return f"""
        WITH team_results AS (
            SELECT
                home_team_id AS team_id,
                CASE
                    WHEN home_team_score > guest_team_score THEN 1
                    ELSE 0
                END AS wins,
                CASE
                    WHEN home_team_score = guest_team_score THEN 1
                    ELSE 0
                END AS draws,
                CASE
                    WHEN home_team_score < guest_team_score THEN 1
                    ELSE 0
                END AS losses,
                home_team_score AS goals_scored_in_match,
                guest_team_score AS goals_conceded_in_match
            FROM
                matches
            WHERE
                home_team_score IS NOT NULL
                AND guest_team_score IS NOT NULL
                AND tournament_id = {tournament_id}
    
            UNION ALL
    
            SELECT
                guest_team_id AS team_id,
                CASE
                    WHEN guest_team_score > home_team_score THEN 1
                    ELSE 0
                END AS wins,
                CASE
                    WHEN guest_team_score = home_team_score THEN 1
                    ELSE 0
                END AS draws,
                CASE
                    WHEN guest_team_score < home_team_score THEN 1
                    ELSE 0
                END AS losses,
                guest_team_score AS goals_scored_in_match,
                home_team_score AS goals_conceded_in_match
            FROM
                matches
            WHERE
                home_team_score IS NOT NULL
                AND guest_team_score IS NOT NULL
                AND tournament_id = {tournament_id}
        )
        SELECT
            FT.team_name,
            COUNT(*) AS matches_played,
            (3 * SUM(TR.wins) + SUM(TR.draws)) AS score,
            SUM(TR.wins) AS wins,
            SUM(TR.draws) AS draws,
            SUM(TR.losses) AS losses,
            SUM(TR.goals_scored_in_match) AS goals_scored,
            SUM(TR.goals_conceded_in_match) AS goals_conceded,
            SUM(TR.goals_scored_in_match) - SUM(goals_conceded_in_match) AS goal_difference
        FROM
            team_results AS TR
        JOIN
            football_teams AS FT ON TR.team_id = FT.id
        GROUP BY
            FT.team_name
        ORDER BY
            score DESC,
            goal_difference DESC,
            goals_scored DESC;
    """
